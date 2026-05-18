# Fix — explorer respawn race + watchdog argv[0] filter (2026-05-18)

**Author:** Ludovico Kubler (with Claude)
**Sentinel:** `sec_explorer_respawn_wrapper_v1`
**Files touched:**
- `~/Scrivania/SEC/scripts/sec_watchdog.py` — relaxed argv[0] filter
- `~/Scrivania/SEC/scripts/spawn_explorer_if_dead.sh` — NEW; replaces inline cron pgrep
- crontab — replaced old self-matching pgrep line with wrapper

## Two bugs found post-reboot 2026-05-18

### Bug 1: watchdog argv[0] too strict

The watchdog filtered explorer processes by requiring `argv[0]` to equal the absolute path `/home/ludo/Scrivania/SEC/.venv/bin/python`. But when the cron auto-restart cd-then-runs `.venv/bin/python`, argv[0] is the *relative* path, not the absolute one. Watchdog therefore missed live explorer processes and reported CRITICAL false positives.

**Fix:** filter is now: argv[0] basename must be in `{python, python3, python3.12}`. The bash-c invocation is still excluded (argv[0] = `/bin/bash`), and tailscaled ssh children too (`/usr/sbin/tailscaled`).

### Bug 2: cron auto-restart self-match

The cron line was:
```
*/5 * * * * pgrep -f "pvsnp_explorer.*--loop" > /dev/null || (cd ... && nohup ...)
```

`pgrep -f` matches against `/proc/<pid>/cmdline`. The cron-invoked bash subprocess has cmdline `bash -c '... pgrep -f "pvsnp_explorer.*--loop" ...'` — which CONTAINS the pattern. pgrep matches itself, returns non-empty, the OR short-circuits, no spawn.

Result: after the explorer died at 21:41 UTC, every 5-min cron tick failed to respawn. Watchdog (separately broken — Bug 1) didn't alert. Server was dark for ~50 minutes until I noticed.

**Fix:** new wrapper `spawn_explorer_if_dead.sh` that inspects `/proc/<pid>/cmdline` directly, filters argv[0] to python interpreters only (excludes the wrapper's own bash). Cron now invokes the wrapper instead of inline pgrep.

## Verification

- Wrapper: no-op when explorer alive (tested manually with PID 6186).
- Watchdog: detected PID 6186 correctly after fix; STATUS.md is OK.
- Spawn-on-dead path verified via bash -n syntax check; full kill-test deferred to avoid downtime.

## Lesson

Two systems independently watching the same process is fragile when both have bugs. Long-term: the watchdog should own restarts (single source of truth). For now: both fixed, both running.
