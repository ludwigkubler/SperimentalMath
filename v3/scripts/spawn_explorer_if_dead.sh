#!/bin/bash
# Spawn pvsnp_explorer if not running.
#
# Replaces the old cron line:
#   */5 * * * * pgrep -f "pvsnp_explorer.*--loop" || (cd ... && nohup ...)
# which had a self-match bug: the cron's own bash -c command line
# contains the substring "pvsnp_explorer.*--loop", so pgrep -f matches
# itself and the spawn never fires.
#
# This wrapper scans /proc/<pid>/cmdline directly, filters to processes
# whose argv[0] is a python interpreter (so bash invocations are
# excluded), and checks for the explorer module spec.
#
# Sentinel: sec_explorer_respawn_wrapper_v1 — 2026-05-18

set -u

SEC=/home/ludo/Scrivania/SEC
LOG="$SEC/research/pvsnp_explorer.log"

is_running() {
    local cmdfile cmdline
    for cmdfile in /proc/[0-9]*/cmdline; do
        [ -r "$cmdfile" ] || continue
        # cmdline is NUL-separated argv; replace NULs with spaces for matching
        cmdline=$(tr '\0' ' ' < "$cmdfile" 2>/dev/null) || continue
        # argv[0] is everything up to the first space
        local argv0="${cmdline%% *}"
        # argv[0] must end with /python or /python3 or be relative .venv/bin/python.
        # This excludes the bash -c wrapper that has argv[0] = /bin/bash.
        case "$argv0" in
            */python|*/python3|*/python3.12|.venv/bin/python|python|python3)
                ;;
            *)
                continue
                ;;
        esac
        # Now check the full argv for the explorer module + --loop flag
        if [[ "$cmdline" == *"src.research.pvsnp_explorer"* ]] && [[ "$cmdline" == *"--loop"* ]]; then
            return 0
        fi
    done
    return 1
}

if is_running; then
    exit 0
fi

# Not running — spawn fresh
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
