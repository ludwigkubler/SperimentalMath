#!/bin/bash
# Spawn pvsnp_explorer if not running.
#
# Replaces the old cron line that had a self-match bug (pgrep -f matched
# its own bash -c invocation).
#
# This wrapper:
#  1. Acquires a flock to serialize concurrent invocations (e.g. two cron
#     ticks racing, or test scripts firing in parallel — discovered to
#     cause N explorers on 2026-05-19).
#  2. Scans /proc/<pid>/cmdline directly, filtering to python interpreters
#     (so bash invocations are excluded).
#  3. Spawns the explorer with the .env loaded (if present); if .env is
#     missing the explorer still starts but with degraded provider set
#     (verified 2026-05-19).
#  4. Post-spawn: kills any duplicate explorer it finds (older PID kept,
#     others terminated). Belt-and-suspenders to the flock.
#
# Sentinel: sec_explorer_respawn_wrapper_v2 — 2026-05-19

set -u

SEC=/home/ludo/Scrivania/SEC
LOG="$SEC/research/pvsnp_explorer.log"
LOCK_FILE="/tmp/sec_spawn_explorer.lock"

# ── Acquire exclusive lock (non-blocking — if another instance holds it,
#    we exit silently rather than wait, because the other instance will
#    spawn if needed).
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    # Another wrapper is currently running. Exit 0 silently; the other
    # one will handle the spawn. Race avoidance.
    exit 0
fi

# ── Find all real explorer PIDs (python -m src.research.pvsnp_explorer --loop)
list_explorer_pids() {
    local cmdfile cmdline argv0 pid
    for cmdfile in /proc/[0-9]*/cmdline; do
        [ -r "$cmdfile" ] || continue
        cmdline=$(tr '\0' ' ' < "$cmdfile" 2>/dev/null) || continue
        argv0="${cmdline%% *}"
        case "$argv0" in
            */python|*/python3|*/python3.12|.venv/bin/python|python|python3)
                ;;
            *)
                continue
                ;;
        esac
        if [[ "$cmdline" == *"src.research.pvsnp_explorer"* ]] && \
           [[ "$cmdline" == *"--loop"* ]]; then
            pid=$(basename "$(dirname "$cmdfile")")
            echo "$pid"
        fi
    done
}

EXISTING_PIDS=$(list_explorer_pids)

if [ -n "$EXISTING_PIDS" ]; then
    # Already running. Check for duplicates and kill the newer ones.
    COUNT=$(echo "$EXISTING_PIDS" | wc -l)
    if [ "$COUNT" -gt 1 ]; then
        # Sort by start time (older first), keep PID with smallest start time
        OLDEST=$(echo "$EXISTING_PIDS" | while read pid; do
            stime=$(stat -c '%Y' "/proc/$pid" 2>/dev/null || echo "9999999999")
            echo "$stime $pid"
        done | sort -n | head -1 | awk '{print $2}')
        echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] DUPLICATE detected: keeping oldest $OLDEST, killing $(echo "$EXISTING_PIDS" | grep -v "^$OLDEST$" | tr '\n' ' ')" >> "$LOG"
        for pid in $EXISTING_PIDS; do
            if [ "$pid" != "$OLDEST" ]; then
                kill "$pid" 2>/dev/null
            fi
        done
    fi
    exit 0
fi

# ── Not running — spawn fresh
cd "$SEC" || {
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] cannot cd to $SEC" >&2
    exit 2
}

if [ -f .env ]; then
    set -a
    # shellcheck disable=SC1091
    . ./.env
    set +a
fi

nohup .venv/bin/python -m src.research.pvsnp_explorer --loop --interval 60 \
    >> "$LOG" 2>&1 &
spawned_pid=$!
echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] spawned explorer PID $spawned_pid" >> "$LOG"
exit 0
