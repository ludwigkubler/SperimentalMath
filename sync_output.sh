#!/bin/bash
# SperimentalMath sync — copies auto-generated outputs from SEC research/
# into the SperimentalMath repo, organized by artifact type, then commits & pushes.
#
# Runs hourly via cron. Non-destructive. Skips commit if nothing changed.
set -e

REPO=/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath
SRC=/home/ludo/Scrivania/SEC/research

cd "$REPO"

# --- 1. Notebook: split JSONL by month
if [ -f "$SRC/pvsnp_notebook.jsonl" ]; then
    # Parse each line, append to monthly file
    python3 << 'PY'
import json, time, os
from pathlib import Path
src = Path("/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl")
dst = Path("/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/notebook")
dst.mkdir(parents=True, exist_ok=True)
by_month = {}
for line in src.read_text().splitlines():
    try:
        e = json.loads(line)
    except Exception:
        continue
    ts = e.get("ts", time.time())
    ym = time.strftime("%Y-%m", time.gmtime(ts))
    by_month.setdefault(ym, []).append(line)
for ym, lines in by_month.items():
    (dst / f"{ym}.jsonl").write_text("\n".join(lines) + "\n")
PY
fi

# --- 2. Frameworks (once F4 is live)
if [ -f "$SRC/pvsnp_frameworks.jsonl" ]; then
    python3 << 'PY'
import json
from pathlib import Path
src = Path("/home/ludo/Scrivania/SEC/research/pvsnp_frameworks.jsonl")
root = Path("/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/frameworks")
for line in src.read_text().splitlines():
    try:
        f = json.loads(line)
    except Exception:
        continue
    status = f.get("status", "PROPOSED").lower()
    # map status to subdir
    sub = {"promoted": "promoted", "published": "published", "dead": "dead"}.get(status, "proposed")
    (root / sub).mkdir(parents=True, exist_ok=True)
    (root / sub / f"{f['framework_id']}.json").write_text(json.dumps(f, indent=2, ensure_ascii=False))
PY
fi

if [ -f "$SRC/pvsnp_dead_frameworks.jsonl" ]; then
    cp "$SRC/pvsnp_dead_frameworks.jsonl" "$REPO/frameworks/dead/_compendium.jsonl"
fi

# --- 3. Papers: copy .tex AND .pdf for each SUPPORTED+CONFIRM
if [ -d "$SRC/pvsnp_papers" ]; then
    mkdir -p papers
    rsync -a --include='*.tex' --include='*.pdf' --exclude='*' "$SRC/pvsnp_papers/" papers/
fi

# --- 4. Lean stubs (un-verified autoformalizations)
if [ -d "$SRC/pvsnp_lean_stubs" ]; then
    mkdir -p lean_stubs
    rsync -a --include='*.lean' --exclude='*' "$SRC/pvsnp_lean_stubs/" lean_stubs/
fi

# --- 5. Lean verified (FORMAL_VERIFIED — the gold tier)
if [ -d "$SRC/pvsnp_verified" ]; then
    mkdir -p lean_verified
    rsync -a --include='*.lean' --include='lakefile.toml' --exclude='.lake/' --exclude='*.olean' "$SRC/pvsnp_verified/" lean_verified/
fi

# --- 6. Barriers: split by which barrier
if [ -f "$SRC/pvsnp_barriers_rejected.jsonl" ]; then
    mkdir -p barriers
    python3 << 'PY'
import json
from pathlib import Path
src = Path("/home/ludo/Scrivania/SEC/research/pvsnp_barriers_rejected.jsonl")
dst = Path("/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath/barriers")
by_b = {}
for line in src.read_text().splitlines():
    try:
        e = json.loads(line)
    except Exception:
        continue
    b = (e.get("barrier", "unknown") or "unknown").lower()
    by_b.setdefault(b, []).append(line)
for b, lines in by_b.items():
    (dst / f"{b}.jsonl").write_text("\n".join(lines) + "\n")
PY
fi

# --- 7. Reports: copy all .md and .pdf from the markdown reports dir
if [ -d "$SRC/reports" ]; then
    mkdir -p reports
    rsync -a --include='*.md' --include='*.pdf' --exclude='*' "$SRC/reports/" reports/
fi

# --- 8. stats.json: cumulative counters
python3 << 'PY'
import json, time
from pathlib import Path
src = Path("/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl")
repo = Path("/home/ludo/Scrivania/SEC/research/git_mirrors/SperimentalMath")
entries = []
if src.exists():
    for line in src.read_text().splitlines():
        try:
            entries.append(json.loads(line))
        except Exception:
            continue
from collections import Counter
verdicts = Counter(e.get("final_verdict") or e.get("phase") or "unknown" for e in entries)
def _fa(e):
    v = e.get("field_A", "unknown")
    return v if isinstance(v, str) else str(v)[:120]
fields_A = Counter(_fa(e) for e in entries)
stats = {
    "last_update_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "total_cycles": len(entries),
    "verdict_counts": dict(verdicts),
    "unique_field_A": len(fields_A),
    "top_fields_A": fields_A.most_common(15),
}
(repo / "stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False))
PY

# --- 9. Audit logs (every LLM call per entry — full prompts + responses)
if [ -d "$SRC/audit" ]; then
    mkdir -p audit
    rsync -a --include='*.jsonl' --exclude='*' "$SRC/audit/" audit/
fi

# --- 10. Reviewer packs (PDF + MD per entry — Royal Society defensible)
if [ -d "$SRC/reviewer_packs" ]; then
    mkdir -p reviewer_packs
    rsync -a --include='*.md' --include='*.pdf' --exclude='*' "$SRC/reviewer_packs/" reviewer_packs/
fi

# --- 11. Replay tarballs (everything needed to reproduce a cycle)
if [ -d "$SRC/replay" ]; then
    mkdir -p replay
    rsync -a --include='*.tar.gz' --exclude='*' "$SRC/replay/" replay/
fi

# --- 11b. Lean counterexample formalizations (Fase B)
if [ -d "$SRC/lean_counterexamples" ]; then
    mkdir -p lean_counterexamples
    rsync -a --include='*.lean' --exclude='*' "$SRC/lean_counterexamples/" lean_counterexamples/
fi
if [ -f "$SRC/pvsnp_lean_counterexample_log.jsonl" ]; then
    cp "$SRC/pvsnp_lean_counterexample_log.jsonl" lean_counterexamples/_build_log.jsonl
fi

# --- 11c. Citation rigor verdicts (Fase C — per-entry independent judge)
if [ -d "$SRC/citations" ]; then
    mkdir -p citations
    rsync -a --include='*.json' --exclude='*' "$SRC/citations/" citations/
fi

# --- 12. Sandbox test sources (the actual Python that ran)
if [ -d "$SRC/pvsnp_sandbox" ]; then
    mkdir -p sandbox_archive
    rsync -a --include='test_*.py' --exclude='*' "$SRC/pvsnp_sandbox/" sandbox_archive/
fi

# --- 13. Operational logs (Claude Max budget + monitor alerts)
if [ -f "$SRC/claude_max_call_log.jsonl" ]; then
    cp "$SRC/claude_max_call_log.jsonl" claude_max_call_log.jsonl
fi
if [ -f "$SRC/monitor_alerts.jsonl" ]; then
    cp "$SRC/monitor_alerts.jsonl" monitor_alerts.jsonl
fi

# --- 14. Commit & push if changes
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    TS=$(date '+%Y-%m-%d %H:%M')
    NEW_CYCLES=$(git diff --cached --stat notebook/ 2>/dev/null | tail -1)
    git commit -m "auto: hourly sync $TS

$NEW_CYCLES

Co-Authored-By: SEC Explorer <noreply@sec>"

    # push (rate limited)
    N_AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 999)
    if [ "$N_AHEAD" -lt 24 ]; then
        git push origin main 2>&1 || git push origin HEAD:main 2>&1 || echo "push deferred"
    else
        echo "too many unpushed commits ($N_AHEAD)"
    fi
else
    echo "no changes"
fi
