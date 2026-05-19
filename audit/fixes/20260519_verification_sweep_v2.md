# Verification sweep #2 — post-pass tests (2026-05-19)

After the user asked again "sei assolutamente certo che funzioni tutto?", 8 follow-up tests were run:

| # | Test | Result |
|--:|:---|:---|
| 1 | Watchdog push-on-transition: kill explorer → expect CRITICAL push to origin | PASS — pushed commit 7616b406 within 5s |
| 2 | sync_output.sh audit: looking for new landmines | rsync still copies audit/_global.jsonl from source to repo (line 137), but it is now gitignored so it does not get committed/pushed |
| 3 | pvsnp_audit.py rotation | **FAIL** — no rotation. TODO comment at line 137 was never implemented. **FIXED** with sec_audit_rotation_v1 (90 MB threshold). |
| 4 | Lean Float.abs exists in stdlib | PASS — Float.abs (-3.14) evaluates to 3.14 |
| 5 | .bak files in src/ as import targets | PASS — Python rejects names with extra dots (ModuleNotFoundError). 23 .bak files exist but cannot be imported. Hygiene-only concern. |
| 6 | Watchdog filter covers all recent logs | PASS — current watchdog state is OK across 7 recent log files |
| 7 | kirousis SICI DOI with special chars resolves via CrossRef | PASS — HTTP 200, special chars handled |
| 8 | Wrapper flock release on early exit | PASS — wrapper rc=0 when lock is held by external process, exits silently without spawning |

**Fixes applied as a result:**
- sec_audit_rotation_v1: rotation of _global.jsonl at 90 MB threshold (writes via _atomic_append now check size first)
- New watchdog check mirror_git_pushed: alerts if more than 3 commits in mirror are unpushed (would have caught the 14h silent failure)
- OPERATIONAL_STATUS.md sync to current state with sentinel list

**Honest residual:**
- 23 .bak files in src/ remain (no risk, hygiene only)
- pvsnp_audit.py rotation does not delete archived files (manual cleanup may eventually be needed)
- The watchdog mirror_git_pushed check requires network access (git fetch) — adds ~1-2s latency per tick

Watchdog now has 13 independent checks. STATUS.md is 🟢 OK.
