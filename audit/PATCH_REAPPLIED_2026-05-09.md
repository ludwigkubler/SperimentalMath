# Patch re-applied — 2026-05-09 (root cause of auto-revert identified)

**Author**: L. K.

## Summary

The proposer-prompt and reporter patches landed on 2026-05-08 (commit
`856872e`) were silently reverted within ~1 hour of being applied,
because they were applied to the wrong copy of the source files. This
note documents the root cause and the corrected re-application.

## Root cause

There are TWO copies of every `pvsnp_*.py` file on `ludo@sec`:

* **MASTER** — `/home/ludo/Scrivania/SEC/src/research/pvsnp_*.py`. This
  is the live source. The autonomous engine reads from here.
* **MIRROR** — `/home/ludo/kissat/pvnp_lab/system_v2/src/pvsnp_*.py`.
  This is a downstream copy, refreshed every hour at minute :17 by the
  cron job `~/kissat/pvnp_lab/system_v2/scripts/sync_from_sec.sh`.

The 2026-05-08 patches were applied to the **mirror** (pvnp_lab).
Within an hour the cron `sync_from_sec.sh` overwrote the mirror with
the un-patched master — so no commit was ever made to pvnp_lab's git
log for those files (last commit affecting `pvsnp_explorer.py`:
2026-05-01), and the running engine kept using the un-patched master.

This explains the symptom observed on 2026-05-09 17:08 UTC:

```
=== PATCH STATE ===
PROPOSER patch: REVERTED   (grep -c 'calibration trap' on mirror = 0)
REPORT patch:   REVERTED
WALL_ATLAS fix: REVERTED
```

## Re-application

On 2026-05-09 ~17:17 UTC the same three patches were re-applied directly
to the MASTER files in `/home/ludo/Scrivania/SEC/src/research/` (not to
the mirror). The master copies now contain:

* `pvsnp_explorer.py`: `Calibration traps` block in `PROPOSER_SYSTEM`
  (line 398), `Recently observed failure modes` block in
  `TESTER_SYSTEM` (line 783) — `random.sample(d)` warning, log domain
  guard, division-by-zero guard, recursion-depth cap, index-bound
  warning, `ast.parse` pre-flight, plus three semantic-failure
  warnings.
* `pvsnp_report.py`: `_load_retractions()` reading
  `~/Scrivania/SEC/research/retractions.json`, `_AUDIT_BANNER`, modified
  `build_supported` and `build_falsified` that filter retracted
  entries, modified `build_wall_atlas` that uses the same
  `cat_raw` normalization as `build_summary`.

After upload, `sync_from_sec.sh` was triggered manually; the patches
propagated to the mirror, and the next pvnp_lab auto-sync at 17:17 UTC
committed `fe1125b` with the changes. The reports were regenerated and
now contain the AUDIT banner and the retractions section as expected.

## How to detect future reverts

Any verification of patch persistence MUST grep the **master** path:

```
ssh ludo@sec "grep -ic 'calibration traps' /home/ludo/Scrivania/SEC/src/research/pvsnp_explorer.py"
ssh ludo@sec "grep -c '_load_retractions' /home/ludo/Scrivania/SEC/src/research/pvsnp_report.py"
```

A `0` from either of these means the patch is gone again.

## Effective timestamp for crash-rate comparison

Cycles produced under the patched proposer are those with
`ts >= 1778349600` (= 2026-05-09T17:00:00Z). Earlier cycles, including
the bulk of the audit corpus, were under the un-patched proposer.

The 2026-05-10 routine has been updated with this new cutoff and
with the case-insensitive grep marker `Calibration traps`.

— L. K., 2026-05-09
