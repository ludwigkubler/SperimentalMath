# Fix — flock fd inheritance leak (2026-05-21)

**Sentinel:** `sec_explorer_respawn_wrapper_v3`

## Bug

The wrapper used `exec 9>"$LOCK_FILE"` + `flock -n 9` to serialize
concurrent invocations. But `nohup .venv/bin/python ... &` spawns the
explorer with all open fds inherited — including fd 9.

So the explorer process (which lives for hours) ended up holding the
flock. Every subsequent wrapper invocation hit:

```
exec 9>"$LOCK_FILE"
flock -n 9   # FAILS — explorer has the lock
exit 0       # silently
```

Result: the wrapper's dedup-kill logic could NEVER fire. Duplicate
explorers spawned via test/manual bypass accumulated forever.

Observed 2026-05-21 with 2 explorers running for ~3 minutes each.
Verified by `ls -la /proc/$EXPLORER_PID/fd/9 → /tmp/sec_spawn_explorer.lock`.

## Fix

In the wrapper, close fd 9 in the child process before nohup:

```diff
-nohup .venv/bin/python -m src.research.pvsnp_explorer --loop --interval 60 \
-    >> "$LOG" 2>&1 &
+nohup .venv/bin/python -m src.research.pvsnp_explorer --loop --interval 60 \
+    9<&- >> "$LOG" 2>&1 &
```

`9<&-` closes fd 9 in the redirection context (which the child inherits).

## Verification

```
new explorer PID=8121
fd 9 on explorer: ls: cannot access '/proc/8121/fd/9': No such file or directory  ✓
wrapper re-invocation: 1 explorer (was 2 before fix)  ✓
```

## Plus: new watchdog check `explorer_singleton`

Adds a separate DEGRADED-severity check that fires when more than one
explorer is running, even if the wrapper somehow misses the dedup.
Belt-and-suspenders to the wrapper-side fix.

Watchdog now has 14 checks.
