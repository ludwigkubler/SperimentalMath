#!/usr/bin/env python3
"""SEC comprehensive watchdog.

Runs every 5 min via cron. Catches multi-level failures that the existing
pvsnp_monitor missed during the 2026-05-13 3-day silent outage caused
by a NameError in monitor itself.

Design principles:
- Each check is independent. One failing does not skip others.
- Output is multi-channel: machine-readable state JSON, human-readable
  STATUS.md committed to the SperimentalMath repo, structured alerts.
- The watchdog must not depend on the things it watches. No imports
  of sec source code. No LLM calls. Stdlib + subprocess only.
- It is fail-loud: any unexpected exception in this script itself is
  written to stderr (cron captures it).

Outputs:
- ~/Scrivania/SEC/research/watchdog_state.json (full machine-readable)
- ~/Scrivania/SEC/research/git_mirrors/SperimentalMath/STATUS.md (human badge)
- Append to ~/Scrivania/SEC/research/git_mirrors/SperimentalMath/monitor_alerts.jsonl on transition

Exit codes:
- 0 = OK (all checks green)
- 1 = DEGRADED (non-critical check failed)
- 2 = CRITICAL (explorer/service/disk failed)
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HOME = Path("/home/ludo")
SEC = HOME / "Scrivania" / "SEC"
RESEARCH = SEC / "research"
MIRROR = RESEARCH / "git_mirrors" / "SperimentalMath"
STATE_FILE = RESEARCH / "watchdog_state.json"
STATUS_FILE = MIRROR / "STATUS.md"
ALERTS_FILE = MIRROR / "monitor_alerts.jsonl"
PREV_STATUS_FILE = RESEARCH / "watchdog_prev_status.txt"

NOW = datetime.now(timezone.utc)
NOW_EPOCH = NOW.timestamp()


def sh(cmd, timeout=10):
    """Run shell command, return (returncode, stdout_stripped, stderr_stripped)."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


# ── Individual checks ────────────────────────────────────────────────────────

def check_explorer_process():
    """Match by reading /proc/<pid>/cmdline directly. Avoids pgrep matching
    ssh/tailscaled processes that mention the pattern in their argv.

    Filter rule:
      - argv[0] must end with `/python` or `/python3` (or be the bare
        relative `.venv/bin/python` form, because the cron auto-restart
        invokes the explorer with a relative interpreter path).
      - argv joined must contain `src.research.pvsnp_explorer` and `--loop`.
    Excludes bash-c invocations (argv[0] = /bin/bash) and tailscaled ssh
    children (argv[0] = /usr/sbin/tailscaled).
    """
    needle_mod = "src.research.pvsnp_explorer"
    pids = []
    try:
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue
            try:
                raw = (entry / "cmdline").read_bytes()
            except (FileNotFoundError, PermissionError):
                continue
            argv = raw.split(b"\x00")
            if len(argv) < 3:
                continue
            try:
                argv0 = argv[0].decode("utf-8", "replace")
            except Exception:
                continue
            # Accept any python interpreter invocation: absolute, relative,
            # bare. Reject anything that isn't python.
            argv0_base = argv0.rsplit("/", 1)[-1]
            if argv0_base not in {"python", "python3", "python3.12"}:
                continue
            joined = b" ".join(argv).decode("utf-8", "replace")
            if needle_mod in joined and "--loop" in joined:
                pids.append(entry.name)
    except Exception as e:
        return False, f"proc scan failed: {e}"
    if len(pids) == 0:
        return False, "no explorer process"
    # Note: duplicate detection is now a separate check
    # (check_explorer_singleton, DEGRADED severity) — see below.
    return True, f"pid {pids[0]}" if len(pids) == 1 else f"pids {','.join(pids)}"


def check_explorer_singleton():
    """Verify exactly ONE explorer process is running. More than one =
    DEGRADED (waste of GPU + race conditions on shared files). Caught
    2026-05-21: the wrapper inherited fd 9 to the explorer process,
    leaking the flock and preventing dedup-kill on future ticks."""
    needle_mod = "src.research.pvsnp_explorer"
    pids = []
    try:
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue
            try:
                raw = (entry / "cmdline").read_bytes()
            except (FileNotFoundError, PermissionError):
                continue
            argv = raw.split(b"\x00")
            if len(argv) < 3:
                continue
            try:
                argv0 = argv[0].decode("utf-8", "replace")
            except Exception:
                continue
            argv0_base = argv0.rsplit("/", 1)[-1]
            if argv0_base not in {"python", "python3", "python3.12"}:
                continue
            joined = b" ".join(argv).decode("utf-8", "replace")
            if needle_mod in joined and "--loop" in joined:
                pids.append(entry.name)
    except Exception as e:
        return False, f"proc scan failed: {e}"
    if len(pids) <= 1:
        return True, f"{len(pids)} explorer process(es)"
    return False, f"DUPLICATE: {len(pids)} explorer processes ({','.join(pids)})"


def check_explorer_cycle_fresh(max_age_h=2.0):
    """Most recent timestamped line in pvsnp_explorer.log is recent."""
    log = RESEARCH / "pvsnp_explorer.log"
    if not log.exists():
        return False, "log file missing"
    rc, out, _ = sh(f"tail -n 2000 '{log}' | grep -E '^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}' | tail -1")
    if not out:
        return False, "no timestamped lines in tail"
    m = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", out)
    if not m:
        return False, "could not parse timestamp"
    try:
        last = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        age_h = (NOW - last).total_seconds() / 3600
        return age_h < max_age_h, f"last activity {age_h:.2f}h ago"
    except Exception as e:
        return False, f"parse error: {e}"


def check_sec_entity_service():
    rc, out, _ = sh("systemctl is-active sec-entity")
    return rc == 0 and out == "active", out or "inactive"


def check_cron_service():
    rc, out, _ = sh("systemctl is-active cron")
    return rc == 0 and out == "active", out or "inactive"


def check_gpu():
    rc, out, err = sh("nvidia-smi --query-gpu=name --format=csv,noheader", timeout=5)
    return rc == 0 and bool(out), (out or err or "no output")[:120]


def check_disk(threshold_pct=90):
    rc, out, _ = sh("df -P /home | awk 'NR==2 {gsub(\"%\",\"\",$5); print $5}'")
    try:
        pct = int(out)
        return pct < threshold_pct, f"{pct}% used"
    except Exception:
        return False, f"parse fail: out={out!r}"


def check_ram(min_avail_mb=1024):
    rc, out, _ = sh("free -m | awk 'NR==2 {print $7}'")
    try:
        mb = int(out)
        return mb > min_avail_mb, f"{mb} MB available"
    except Exception:
        return False, f"parse fail: out={out!r}"


def check_mirror_git_fresh(max_age_h=4.0):
    rc, out, _ = sh(f"cd '{MIRROR}' && git log -1 --format='%ct'", timeout=5)
    try:
        ts = int(out)
        age_h = (NOW_EPOCH - ts) / 3600
        return age_h < max_age_h, f"last commit {age_h:.2f}h ago"
    except Exception:
        return False, f"parse fail: out={out!r}"


def check_mirror_git_pushed(max_unpushed: int = 3):
    """The mirror's local main is in sync with origin/main (modulo a small
    grace for very recent commits that the hourly sync will push).

    This catches the class of silent failure observed 2026-05-19: hourly
    sync_output.sh committed 14 hours of changes successfully, but the
    git push was rejected by GitHub for an oversized file. The script
    logged 'push deferred' to sync.log but no other alert. The watchdog
    didn't know to look.

    Rule: more than `max_unpushed` commits between origin/main and local
    main is DEGRADED. Default 3 = up to ~3 hours of unpushed work is OK
    (typical between cron ticks), 4+ means something is stuck.
    """
    # First refresh remote refs (cheap, only fetches refs not objects)
    rc, _, _ = sh(f"cd '{MIRROR}' && git fetch --quiet origin main", timeout=15)
    if rc != 0:
        return False, "git fetch failed (network?)"
    rc, out, _ = sh(
        f"cd '{MIRROR}' && git rev-list --count origin/main..HEAD",
        timeout=5,
    )
    try:
        unpushed = int(out)
    except Exception:
        return False, f"parse fail: {out!r}"
    if unpushed > max_unpushed:
        return False, f"{unpushed} commits ahead of origin/main (max {max_unpushed})"
    return True, f"{unpushed} unpushed (within tolerance)"


def check_notebook_growth(max_age_h=4.0):
    """The latest entry in the current-month notebook is recent.

    Tolerated: at end of month the file rolls over to next month;
    we look at both current and previous months.
    """
    candidates = []
    for delta in (0, 32):  # current month, previous month
        t = NOW - timedelta(days=delta)
        nb = MIRROR / "notebook" / f"{t.strftime('%Y-%m')}.jsonl"
        if nb.exists():
            candidates.append(nb)
    if not candidates:
        return False, "no notebook file found"
    best_age = float("inf")
    for nb in candidates:
        try:
            # Last line only — efficient via tail
            rc, out, _ = sh(f"tail -n 1 '{nb}'", timeout=5)
            if not out:
                continue
            e = json.loads(out)
            ts = e.get("ts", 0)
            age_h = (NOW_EPOCH - ts) / 3600
            best_age = min(best_age, age_h)
        except Exception:
            pass
    if best_age == float("inf"):
        return False, "could not read any entries"
    return best_age < max_age_h, f"newest entry {best_age:.2f}h ago"


def check_audit_log_infrastructure():
    """The ENTITY audit_log writes only on chat-driven _execute_action calls.
    During fully idle days the file may not appear. So instead we verify the
    INFRASTRUCTURE: the audit directory exists and is writable. Content is
    a soft signal."""
    d = HOME / "data" / "entity" / "audit"
    if not d.exists():
        return False, f"dir missing: {d}"
    if not d.is_dir():
        return False, f"not a dir: {d}"
    # Probe writability
    probe = d / ".watchdog_probe"
    try:
        probe.write_text("ok")
        probe.unlink()
    except Exception as e:
        return False, f"not writable: {e}"
    today = NOW.strftime("%Y-%m-%d")
    f = d / f"actions-{today}.jsonl"
    if f.exists():
        return True, f"today {f.stat().st_size}B"
    return True, "dir ok, no entries today (chat-idle)"


def check_recent_traceback_in_cron_logs(max_age_h=1.0):
    """Scan recent .log files for UNHANDLED tracebacks.

    A traceback is considered handled (and thus benign) if the next 10
    log lines contain ANY of the following recovery markers:
      - 'cycle failed:'           (pvsnp_explorer's caught-and-continue)
      - 'fail-open'               (skeptic gate graceful degradation)
      - 'retrying'                (any retry logic)
      - 'WARNING'                 (warning-level recovery)
      - 'Routing to'              (LLM provider fallback)
      - 'INFO sec.'               (resumed normal logging)
    Only tracebacks NOT followed by a recovery marker in 10 lines are
    flagged as unhandled.

    The earlier version flagged every traceback as bad, producing
    false-positives from httpx timeouts in pvsnp_explorer.log
    (observed 2026-05-19).
    """
    cutoff = NOW_EPOCH - max_age_h * 3600
    recovery_markers = (
        "cycle failed:", "fail-open", "retrying",
        "WARNING", "Routing to", "INFO sec.",
    )
    offenders = []
    for logfile in RESEARCH.glob("*.log"):
        try:
            st = logfile.stat()
            if st.st_mtime < cutoff:
                continue
            with logfile.open("rb") as f:
                f.seek(0, 2)
                size = f.tell()
                f.seek(max(0, size - 65536))
                tail = f.read().decode("utf-8", errors="replace")
            # Find all "Traceback (most recent call last)" positions in the last 8KB
            end = tail[-8192:]
            if not (
                "Traceback (most recent call last)" in end
                or "NameError" in end
            ):
                continue
            # Check if each traceback has a recovery marker within ~10 lines after it
            lines = end.split("\n")
            unhandled = False
            for i, line in enumerate(lines):
                if "Traceback (most recent call last)" in line or "NameError" in line:
                    # Look at the next 30 lines (a traceback is up to ~20 lines,
                    # plus the recovery message after).
                    after = "\n".join(lines[i:i + 30])
                    if not any(m in after for m in recovery_markers):
                        unhandled = True
                        break
            if unhandled:
                offenders.append(logfile.name)
        except Exception:
            pass
    return len(offenders) == 0, ",".join(offenders) if offenders else "all clean"


def check_watchdog_self_heartbeat(max_age_min: int = 10):
    """Verify the watchdog itself ran recently.

    The watchdog is the canonical health-reporter; if IT stops firing,
    the rest of the checks are moot. This check reads its own previous
    state file's mtime: if older than `max_age_min` minutes, the
    watchdog (or its cron) has stopped.

    First run: state file doesn't exist yet — accepted as OK.
    """
    state = STATE_FILE
    if not state.exists():
        return True, "first run, no previous state"
    age_sec = NOW_EPOCH - state.stat().st_mtime
    age_min = age_sec / 60
    if age_min > max_age_min:
        return False, f"watchdog last ran {age_min:.1f} min ago (max {max_age_min})"
    return True, f"{age_min:.1f} min ago"


# ── Driver ────────────────────────────────────────────────────────────────────

CHECKS = [
    # (name, fn, severity_if_fails)
    ("explorer_process",       check_explorer_process,           "CRITICAL"),
    ("explorer_singleton",     check_explorer_singleton,         "DEGRADED"),
    ("explorer_cycle_fresh",   check_explorer_cycle_fresh,       "DEGRADED"),
    ("sec_entity_service",     check_sec_entity_service,         "CRITICAL"),
    ("cron_service",           check_cron_service,               "CRITICAL"),
    ("gpu",                    check_gpu,                        "DEGRADED"),
    ("disk_under_90pct",       check_disk,                       "CRITICAL"),
    ("ram_above_1g",           check_ram,                        "DEGRADED"),
    ("mirror_git_fresh",       check_mirror_git_fresh,           "DEGRADED"),
    ("mirror_git_pushed",      check_mirror_git_pushed,          "DEGRADED"),
    ("notebook_growing",       check_notebook_growth,            "DEGRADED"),
    ("entity_audit_log",       check_audit_log_infrastructure,   "DEGRADED"),
    ("cron_logs_no_trace",     check_recent_traceback_in_cron_logs, "DEGRADED"),
    ("watchdog_self_heartbeat", check_watchdog_self_heartbeat,    "DEGRADED"),
]


def main():
    results = []
    n_critical_fail = 0
    n_degraded_fail = 0
    for name, fn, severity in CHECKS:
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"check raised: {type(e).__name__}: {e}"
        results.append({
            "name": name,
            "ok": bool(ok),
            "severity": severity,
            "detail": str(detail)[:240],
        })
        if not ok:
            if severity == "CRITICAL":
                n_critical_fail += 1
            else:
                n_degraded_fail += 1

    if n_critical_fail > 0:
        status, exit_code = "CRITICAL", 2
    elif n_degraded_fail > 0:
        status, exit_code = "DEGRADED", 1
    else:
        status, exit_code = "OK", 0

    state = {
        "ts": NOW.isoformat(),
        "ts_epoch": NOW_EPOCH,
        "status": status,
        "critical_fail": n_critical_fail,
        "degraded_fail": n_degraded_fail,
        "checks": results,
    }

    # Write state atomically
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(STATE_FILE)

    # Write STATUS.md badge for git mirror
    badge = {"OK": "🟢 OK", "DEGRADED": "🟡 DEGRADED", "CRITICAL": "🔴 CRITICAL"}[status]
    md = [
        f"# SEC P-vs-NP — System Status: **{badge}**",
        "",
        f"_Updated: {NOW.isoformat()} (auto-refresh every 5 min)_",
        "",
        f"- CRITICAL failures: **{n_critical_fail}**",
        f"- DEGRADED failures: **{n_degraded_fail}**",
        "",
        "## Checks",
        "",
        "| Check | Result | Detail |",
        "|:------|:-------|:-------|",
    ]
    for r in results:
        emoji = "✅" if r["ok"] else ("🔴" if r["severity"] == "CRITICAL" else "🟡")
        md.append(f"| `{r['name']}` | {emoji} | {r['detail']} |")
    md.append("")
    md.append("---")
    md.append("Auto-generated by `~/Scrivania/SEC/scripts/sec_watchdog.py` every 5 min.")
    md.append("Raw machine-readable data: `research/watchdog_state.json` (not committed).")
    try:
        STATUS_FILE.write_text("\n".join(md) + "\n")
    except Exception as e:
        print(f"WARN: could not write STATUS.md: {e}", file=sys.stderr)

    # Alert on transition
    prev = PREV_STATUS_FILE.read_text().strip() if PREV_STATUS_FILE.exists() else "UNKNOWN"
    if status != prev:
        alert = {
            "ts": NOW_EPOCH,
            "ts_iso": NOW.isoformat(),
            "kind": "WATCHDOG_TRANSITION",
            "from_status": prev,
            "to_status": status,
            "failing_checks": [r["name"] for r in results if not r["ok"]],
            "auto_fixed": False,
        }
        try:
            with ALERTS_FILE.open("a") as f:
                f.write(json.dumps(alert) + "\n")
        except Exception as e:
            print(f"WARN: could not append to alerts: {e}", file=sys.stderr)
        PREV_STATUS_FILE.write_text(status)

        # Push STATUS.md to git on transition. Best-effort, hard timeout.
        # This makes the GitHub-side STATUS.md visible within ~minutes
        # rather than waiting for the hourly sync_output cron.
        try:
            push_cmd = (
                f"cd '{MIRROR}' && "
                "git add STATUS.md monitor_alerts.jsonl 2>/dev/null && "
                "( git diff --cached --quiet || ("
                f"git commit -m 'watchdog: {prev} -> {status}' --no-verify --quiet && "
                "git push --quiet 2>&1 | tail -3))"
            )
            sh(push_cmd, timeout=45)
        except Exception as e:
            print(f"WARN: could not push status: {e}", file=sys.stderr)

    # Print short summary for cron log
    print(f"{NOW.isoformat()} watchdog: {status} crit={n_critical_fail} deg={n_degraded_fail}")
    for r in results:
        if not r["ok"]:
            print(f"  FAIL [{r['severity']}] {r['name']}: {r['detail']}")
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        # Catastrophic failure of the watchdog itself.
        # Write to stderr (cron captures) and try to write an alert.
        print(f"WATCHDOG CRASHED: {type(e).__name__}: {e}", file=sys.stderr)
        try:
            with ALERTS_FILE.open("a") as f:
                f.write(json.dumps({
                    "ts": NOW_EPOCH,
                    "ts_iso": NOW.isoformat(),
                    "kind": "WATCHDOG_CRASH",
                    "exc": f"{type(e).__name__}: {e}",
                }) + "\n")
        except Exception:
            pass
        sys.exit(3)
