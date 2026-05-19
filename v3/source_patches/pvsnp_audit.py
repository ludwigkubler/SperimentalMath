"""SEC P vs NP Audit Trail (Fase A).

Records EVERY LLM call (prompt + system + response + provider + model +
latency + tokens + cost) to per-entry append-only JSONL files. Goal:
provide a Royal Society-defensible audit trail for every research cycle.

Storage layout:
  research/audit/{entry_id}.jsonl     — one record per LLM call
  research/audit/_global.jsonl        — chronological log of all calls
  research/audit/_index.jsonl         — entry_id → call counts + cost summary

A "call record" is:
    {
      "ts": float,
      "entry_id": "abcd1234",
      "session_id": "uuid",
      "phase": "propose|novelty_q|novelty_judge|prereg|test_gen|critic|judge|paper|lean|...",
      "provider": "claude_max",
      "model": "claude-opus-4-7",
      "system_prompt": "...",
      "user_prompt": "...",
      "response": "...",
      "latency_ms": 1234.5,
      "tokens_in": 0,
      "tokens_out": 0,
      "cost_usd": 0.0,
      "error": ""
    }

Audit is append-only. Lines are <PIPE_BUF (4KB) atomic on Linux ext4.
Larger payloads (long prompts) are written via fcntl.flock for safety.
"""
from __future__ import annotations

import contextvars
import fcntl
import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Optional

log = logging.getLogger("sec.research.pvsnp_audit")

SEC_ROOT = Path(os.environ.get("SEC_ROOT", "/home/ludo/Scrivania/SEC"))
AUDIT_DIR = SEC_ROOT / "research" / "audit"

# Context vars: thread-local-ish storage of current entry_id and phase
# so we don't have to thread these through every function.
_current_entry_id: contextvars.ContextVar[Optional[str]] = \
    contextvars.ContextVar("current_entry_id", default=None)
_current_phase: contextvars.ContextVar[Optional[str]] = \
    contextvars.ContextVar("current_phase", default=None)
_current_session: contextvars.ContextVar[Optional[str]] = \
    contextvars.ContextVar("current_session", default=None)


def set_entry(entry_id: str) -> None:
    _current_entry_id.set(entry_id)
    _current_session.set(uuid.uuid4().hex[:12])


def get_entry() -> Optional[str]:
    return _current_entry_id.get()


def set_phase(phase: str) -> None:
    _current_phase.set(phase)


def get_phase() -> Optional[str]:
    return _current_phase.get()


def _ensure_dirs() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)


# Rotation: keep _global.jsonl below this size (GitHub hard-limits files to
# 100 MB and rejects pushes). When exceeded, rotate to a dated archive.
# sec_audit_rotation_v1 — 2026-05-19
_GLOBAL_MAX_BYTES = 90 * 1024 * 1024  # 90 MB; leaves headroom below 100 MB hard cap


def _rotate_if_oversized(path: Path) -> None:
    """If `path` is the global audit log and exceeds size, rotate to a
    timestamped archive (`<stem>-YYYY-MM-DD.jsonl`). Best-effort, never
    raises. Only the `_global.jsonl` filename triggers rotation."""
    try:
        if path.name != "_global.jsonl":
            return
        if not path.exists():
            return
        if path.stat().st_size < _GLOBAL_MAX_BYTES:
            return
        from datetime import datetime, timezone
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        archive = path.with_name(f"_global-{stamp}.jsonl")
        # If archive already exists, append a counter to avoid clobber.
        if archive.exists():
            n = 1
            while True:
                cand = path.with_name(f"_global-{stamp}-{n}.jsonl")
                if not cand.exists():
                    archive = cand
                    break
                n += 1
        path.rename(archive)
    except Exception:
        # Audit log rotation must not break the caller. Silent.
        pass


def _atomic_append(path: Path, payload: dict) -> None:
    """Append a JSON line with file lock. Resilient to concurrent writers."""
    _ensure_dirs()
    _rotate_if_oversized(path)
    line = json.dumps(payload, ensure_ascii=False)
    with path.open("a") as f:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(line + "\n")
            f.flush()
        finally:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass


def record_llm_call(
    *,
    provider: str,
    model: str,
    user_prompt: str,
    system_prompt: str = "",
    response: str = "",
    latency_ms: float = 0.0,
    tokens_in: int = 0,
    tokens_out: int = 0,
    cost_usd: float = 0.0,
    error: str = "",
    phase_override: Optional[str] = None,
    entry_override: Optional[str] = None,
) -> None:
    """Record a single LLM call to the audit trail. Failures here are
    swallowed (the research pipeline must not crash on audit issues)."""
    try:
        entry_id = entry_override or _current_entry_id.get() or "no_entry"
        phase = phase_override or _current_phase.get() or "unknown"
        session_id = _current_session.get() or "no_session"
        rec = {
            "ts": time.time(),
            "entry_id": entry_id,
            "session_id": session_id,
            "phase": phase,
            "provider": provider,
            "model": model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "response": response,
            "latency_ms": float(latency_ms or 0),
            "tokens_in": int(tokens_in or 0),
            "tokens_out": int(tokens_out or 0),
            "cost_usd": float(cost_usd or 0),
            "error": (error or "")[:500],
        }
        # Per-entry log
        if entry_id != "no_entry":
            _atomic_append(AUDIT_DIR / f"{entry_id}.jsonl", rec)
        # Global chronological log (rotated daily would be nice, future)
        _atomic_append(AUDIT_DIR / "_global.jsonl", rec)
    except Exception as e:
        log.debug("audit record failed silently: %s", e)


def entry_summary(entry_id: str) -> dict:
    """Return a summary of all LLM calls for one entry_id."""
    p = AUDIT_DIR / f"{entry_id}.jsonl"
    if not p.exists():
        return {"entry_id": entry_id, "calls": 0}
    calls = []
    for line in p.read_text().splitlines():
        try:
            calls.append(json.loads(line))
        except Exception:
            continue
    if not calls:
        return {"entry_id": entry_id, "calls": 0}
    by_provider = {}
    by_phase = {}
    total_cost = 0.0
    total_tokens_in = 0
    total_tokens_out = 0
    total_latency = 0.0
    for c in calls:
        p = c.get("provider", "?")
        ph = c.get("phase", "?")
        by_provider[p] = by_provider.get(p, 0) + 1
        by_phase[ph] = by_phase.get(ph, 0) + 1
        total_cost += float(c.get("cost_usd", 0) or 0)
        total_tokens_in += int(c.get("tokens_in", 0) or 0)
        total_tokens_out += int(c.get("tokens_out", 0) or 0)
        total_latency += float(c.get("latency_ms", 0) or 0)
    return {
        "entry_id": entry_id,
        "calls": len(calls),
        "first_ts": min(c.get("ts", 0) for c in calls),
        "last_ts": max(c.get("ts", 0) for c in calls),
        "by_provider": by_provider,
        "by_phase": by_phase,
        "total_cost_usd": round(total_cost, 4),
        "total_tokens_in": total_tokens_in,
        "total_tokens_out": total_tokens_out,
        "total_latency_ms": round(total_latency, 0),
    }


def load_entry_log(entry_id: str) -> list[dict]:
    """Return the full list of audit records for an entry."""
    p = AUDIT_DIR / f"{entry_id}.jsonl"
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out
