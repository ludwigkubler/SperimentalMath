# Fix — pvsnp_monitor.py NameError 'log' (2026-05-16)

**Author:** Ludovico Kubler (with Claude)
**File touched:** `~/Scrivania/SEC/src/research/pvsnp_monitor.py`
**Backup:** `pvsnp_monitor.py.bak.20260516_194544`

## Problem

After the 2026-05-13 NVIDIA reboot, the explorer never came back up. Cron runs `pvsnp_monitor` every 30 min, which is responsible for re-spawning the explorer when SERVICE_STALL is detected. But the monitor itself was crashing on every invocation:

```
File "/home/ludo/Scrivania/SEC/src/research/pvsnp_monitor.py", line 545, in fix_restart_explorer
    log.info("killed %d explorers before respawn", n_killed)
    ^^^
NameError: name 'log' is not defined
```

Root cause: line 32 declares `logger = logging.getLogger("sec.research.pvsnp_monitor")`. All 23 call sites in the file use `log.info(...)`, `log.warning(...)` — the wrong name. The variable `log` was never defined.

This presumably worked at some point and got broken by a partial edit (the `logger`/`log` divergence may date to a copy-paste between the `~/SEC/` and `~/Scrivania/SEC/` trees — see audit/code_integrity/00_DISCOVERIES.md D2).

## Impact

3-day silent outage of the entire P-vs-NP exploration loop:
- 2026-05-13 12:17 — last explorer cycle (just before NVIDIA reboot)
- 2026-05-16 19:44 — outage discovered while checking post-fix metrics
- 0 new notebook entries in 79 hours
- Monitor itself failed silently on every cron tick (130+ failed invocations)
- The `test-gen retry bump` fix from 2026-05-15 (commit c02e87b) was deployed on-disk but never exercised because nothing was running

## Fix

One-line rename: `logger = ...` → `log = ...`.

```diff
-logger = logging.getLogger("sec.research.pvsnp_monitor")
+log = logging.getLogger("sec.research.pvsnp_monitor")
```

No call sites use `logger.`, so there is nothing else to update.

After the fix, running `python -m src.research.pvsnp_monitor` once succeeded and auto-applied 3 fixes: `EXPLORER_RESTART`, `REGEN_REPORTS`, `TAXONOMY_REWEIGHT`. The explorer is now running (PID 95860 at 19:45 UTC) on cycle #1.

## Lesson for the audit

This is exactly the class of bug that the 2026-05-13 code-integrity audit's `02_static_python.md` (Phase 2, ruff F821 "undefined name") could have flagged — but I deferred those findings to "later" because the volume (2,810 across the corpus) seemed too noisy to triage. **At least the SEC subset of F821 deserves immediate triage**: this is the second NameError I've personally seen in production SEC code in 3 days (the first was the ENTITY runtime which I haven't dug into).

Action item: `ruff check --select=F821 ~/Scrivania/SEC/src/` and walk the results manually. A 3-day silent outage costs more than 30 min of triage.

## Rollback

```bash
cp /home/ludo/Scrivania/SEC/src/research/pvsnp_monitor.py.bak.20260516_194544 \
   /home/ludo/Scrivania/SEC/src/research/pvsnp_monitor.py
```
