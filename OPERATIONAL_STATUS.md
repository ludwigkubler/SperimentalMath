# SEC P-vs-NP — Operational Status

**Maintained by:** Claude (with Ludovico Kubler)
**Last full audit:** 2026-05-18
**Refresh policy:** update on every change to operational state; readers should also check `STATUS.md` (live, refreshed every 5 min by the watchdog).

This document captures the things `STATUS.md` cannot show: known tech debt, supervised-execution procedures, decisions made, and the why.

---

## Current state — 2026-05-18 17:30 UTC

**Health:** 🟢 OK (see `STATUS.md` for live data)

**Running components:**

| Component | PID family | Lifecycle | Notes |
|:---|:---|:---|:---|
| `sec-entity.service` (GUI daemon) | systemd | 24/7 | API on Tailscale `100.65.109.125:8420` |
| `pvsnp_explorer --loop --interval 60` | cron-spawned, respawned by */5min watchdog | 24/7 | new P-vs-NP exploration loop |
| `src research --config research_gpu.yaml --max-cycles 200` | manual? | until cycles exhausted | OLD C-001 research loop, still active despite memory claiming "STOPPED". Coexists OK with pvsnp_explorer (different log files, different notebook). |

**Cron jobs (verified rc=0 on 2026-05-18 17:11):**

- Every 5 min: `sec_watchdog.py` (NEW), explorer auto-restart, solar_schedule
- Every 30 min: `pvsnp_monitor` (FIXED 2026-05-16 — see audit/fixes/20260516_monitor_log_alias.md)
- Hourly: `sec_diary`, `sync_from_sec.sh`, `sync_output.sh`
- Every 4h: `pvsnp_linkage_graph --refresh`
- Every 6h: `pvsnp_taxonomy --reweight`, `sec_healthcheck.sh`, `self_improve --tick`
- Every 12h: `pvsnp_compute --sweep`
- 3x daily: `pvsnp_arxiv_mirror`
- Daily: `pvsnp_reflection`, `cleanup_videos.py` (monetization, idle effect)
- Weekly Sun: `pvsnp_weekly_replay`, `pvsnp_compendium`, `pvsnp_few_shot --regenerate`
- Weekly Mon: `pvsnp_review_alert`
- Legacy C-001: watchdog, daily_report, c003b_counterexample, literature_scan, git_sync, security_monitor (all pass smoke test)

---

## Recent fix history

| Date | Commit | What broke / What changed |
|:---|:---|:---|
| 2026-05-13 | (no commit, see Audit 1 SUMMARY) | NVIDIA driver/library mismatch fix (caused 3-day silent outage from autoremove that took 595 with it) |
| 2026-05-13 | (live patch) | ENTITY sandbox `python -c` AST validator (`sec_python_payload_v1`) + audit log JSONL |
| 2026-05-15 | `c02e87b` | Test-gen retry-bump 1→3 + always-record pitfalls + n>=5 prompt (`sec_test_gen_retry_bump_v1`) |
| 2026-05-16 | `66121e6` | `pvsnp_monitor.py` rename `logger`→`log` (3-day silent outage F821) |
| 2026-05-18 | `29cb071d` | Watchdog + F821 fix in `pvsnp_framework.py`/`pvsnp_benchmark.py` + compendium retraction filter |
| 2026-05-19 | `4141b406` | v3 Phase 0: Problem Portfolio (6 problems × TOML+Lean, schema doc) |
| 2026-05-19 | `fd3a4c5b` | Wrapper v1 (argv filter + cron self-match fix) |
| 2026-05-19 | `977a781e`, `cc7db2fe` | **Verification sweep #1**: 5 broken DOIs fixed + 1 misattribution + 3 True-Prop Lean bugs + wrapper v2 with flock + watchdog v3 (false-positive filter + self-heartbeat + push-on-transition) + .gitignore `audit/_global.jsonl` (root-cause of 14h silent push failure) |
| 2026-05-19 | (post-this-commit) | **Verification sweep #2**: 8-test follow-up. **Audit log rotation** (`sec_audit_rotation_v1`) — `_global.jsonl` now auto-rotates at 90 MB; existing 114 MB file moved to `_global-2026-05-19.jsonl`. **`mirror_git_pushed` watchdog check** — catches the same silent-push class of failure that broke us for 14h on 2026-05-19. Total: **13 watchdog checks**. |

**Currently active sentinels** (find in source by grep):
- `sec_python_payload_v1` — ENTITY sandbox python -c AST validator
- `sec_test_gen_retry_bump_v1` — test-gen retry policy 1→3 + pitfall-on-failure
- `sec_compendium_retraction_filter_v1` — compendium skips retracted entries
- `sec_explorer_respawn_wrapper_v2` — flock-protected spawn + duplicate-kill
- `sec_audit_rotation_v1` — audit `_global.jsonl` rotates at 90 MB

---

## Known tech debt (supervised execution required)

These items are **diagnosed and have ready procedures** but were not auto-executed because the risk of error is non-trivial and "no errors from you" was explicit. Run with explicit user approval.

### TD-1 — Reconcile `~/SEC` vs `~/Scrivania/SEC`  *(est. 30 min)*

**Problem:** Two parallel SEC trees on the server, both 12 GB. `~/Scrivania/SEC/` is canonical (has `.git`, `.env`, drives `sec-entity.service`). `~/SEC/` is a partial fork with 3 unique files and many divergent copies — invisible drift. Memory used to say `~/SEC` was "stale"; the 2026-05-13 audit corrected this.

**Procedure (verified safe):**

```bash
# 1. Migrate the 3 unique files into the canonical tree
cp ~/SEC/src/monetization/sec_face_animator.py  ~/Scrivania/SEC/src/monetization/
cp ~/SEC/src/monetization/sec_talking_head.py   ~/Scrivania/SEC/src/monetization/
cp ~/SEC/src/monetization/youtube.py            ~/Scrivania/SEC/src/monetization/

# 2. Update the only active cron entry that points at ~/SEC
crontab -l | sed 's|cd /home/ludo/SEC |cd /home/ludo/Scrivania/SEC |g' | crontab -

# 3. Smoke-test the updated cron
cd ~/Scrivania/SEC && .venv/bin/activate && python3 src/monetization/cleanup_videos.py

# 4. Rename ~/SEC to make it invisible (do NOT delete — preserves 30-day rescue window)
mv ~/SEC ~/SEC.archived_20260518

# 5. Verify no tool still references the old path
grep -rln "/home/ludo/SEC[^a-zA-Z]" /home/ludo/Scrivania/SEC/src /home/ludo/kissat 2>/dev/null
# expected: empty output

# 6. After 30 days of green watchdog, free the disk:
# rm -rf ~/SEC.archived_20260518
```

**Verification artefacts pre-collected:**
- ~/SEC unique-files list: 3 entries (`sec_face_animator.py`, `sec_talking_head.py`, `youtube.py`)
- Source-code references to `/home/ludo/SEC/`: only 2 cron lines (1 commented, 1 `cleanup_videos.py`)
- No live process has `~/SEC` as cwd
- No systemd unit references `~/SEC`

### TD-2 — Consolidate duplicate framework files  *(est. 60–90 min refactor)*

**Problem:** `pvsnp_explorer.py`, `pvsnp_monitor.py`, `pvsnp_report.py`, `pvsnp_framework.py` exist as duplicate copies in `~/Scrivania/SEC/src/research/` AND `~/kissat/pvnp_lab/system_v2/src/`. Pre-2026-05-15 they were byte-identical (Audit 1 D4). After the test-gen fix they are still kept in-sync manually. Every patch must be applied twice.

**Proposed solution:** make `~/kissat/pvnp_lab/system_v2/src/` a hard-symlinked subset of `~/Scrivania/SEC/src/research/`, OR set up the kissat copy to be auto-generated from the canonical SEC source via `sync_from_sec.sh` (already exists, runs hourly :17).

**Why not yet executed:** symlinking would break the kissat-side import paths that may differ. Auto-sync from SEC is the cleaner path but requires verifying `sync_from_sec.sh` is bidirectional or that the kissat copy is read-only.

**Quick risk-free win:** add a CI-style check that compares the two copies after each commit and fails loudly if they diverge. Implementation ~30 min.

### TD-3 — `audit/_global.jsonl` exceeds GitHub recommended size  *(RESOLVED 2026-05-19)*

**Status:** Resolved on 2026-05-19. `audit/_global.jsonl` is now gitignored (not version-controlled) and `pvsnp_audit.py` has `sec_audit_rotation_v1` that rotates the file at 90 MB. Existing 114 MB file moved to `_global-2026-05-19.jsonl`. Watchdog check `mirror_git_pushed` added to detect any recurrence of silent push failure.

### TD-3-historical — Original procedure (preserved for reference)

**Problem:** `~/Scrivania/SEC/research/git_mirrors/SperimentalMath/audit/_global.jsonl` is 92 MB. GitHub recommends < 50 MB. Each push triggers a warning. Not yet blocking but eventually will.

**Procedure:**

```bash
# Option A (cheapest): rotate the file
cd ~/Scrivania/SEC/research/git_mirrors/SperimentalMath/audit/
mv _global.jsonl _global.2026-04-archive.jsonl  # rename old
git rm --cached _global.jsonl 2>/dev/null
# Add the archive to .gitignore for historical files >50MB
echo "audit/_global.*-archive.jsonl" >> ../.gitignore

# Option B (cleaner): convert to Git LFS for the audit folder
git lfs track "audit/_global.jsonl"
git add .gitattributes
```

Pick A for speed, B for correctness.

### TD-4 — Two pvsnp explorer-style loops running in parallel

**Problem:** `pvsnp_explorer` (the new pipeline) and `src research --config research_gpu.yaml` (the OLD C-001 loop) are both running. Different log files, different notebook paths. Memory claims C-001 is "STOPPED" but the process started 14h35m ago and is actively cycling.

**Decision needed from user:**
1. Keep both — they complement each other (current state)
2. Kill the C-001 loop — memory becomes consistent with reality
3. Investigate what the C-001 loop is producing (`research.log` shows "Obblighi" obligations work, different from PvNP)

**No auto-action.** Awaiting your call.

### TD-5 — 1370 jsonl files at root of `audit/`

The `audit/` directory in the SperimentalMath mirror has 1,370 hash-named jsonl files at top level (~165 MB). Hard to navigate. Should be moved into `audit/agent_logs/YYYY-MM/` subfolders. ~30 min, no risk.

---

## Watchdog state machine

`sec_watchdog.py` runs every 5 min via cron. It writes `STATUS.md` at the top of the mirror. Checks performed:

| Check | Severity | Description |
|:---|:---|:---|
| `explorer_process` | CRITICAL | `python -m src.research.pvsnp_explorer --loop` running (matched by reading /proc/*/cmdline directly, no pgrep false-positives) |
| `explorer_cycle_fresh` | DEGRADED | Last timestamped line in `pvsnp_explorer.log` < 2h ago |
| `sec_entity_service` | CRITICAL | `systemctl is-active sec-entity` is `active` |
| `cron_service` | CRITICAL | `systemctl is-active cron` is `active` |
| `gpu` | DEGRADED | `nvidia-smi --query-gpu=name` succeeds |
| `disk_under_90pct` | CRITICAL | `/home` < 90% used |
| `ram_above_1g` | DEGRADED | `free -m` shows > 1024 MB available |
| `mirror_git_fresh` | DEGRADED | Last commit < 4h ago |
| `notebook_growing` | DEGRADED | Newest notebook entry < 4h ago |
| `entity_audit_log` | DEGRADED | Audit log dir present + writable |
| `cron_logs_no_trace` | DEGRADED | No unhandled tracebacks in recent .log files |

State machine:
- **OK** = all green. Exit 0.
- **DEGRADED** = ≥1 non-critical fail. Exit 1.
- **CRITICAL** = ≥1 critical fail. Exit 2.

On any **status transition** (OK↔DEGRADED↔CRITICAL), an event is appended to `monitor_alerts.jsonl` and `STATUS.md` is regenerated to reflect the new state.

**Self-test:** the watchdog runs ruff F-rules clean (`F821 = 0`, no NameError-class bugs in its own source).

---

## How a future Claude session should onboard

1. `cat STATUS.md` — system health right now (auto-refreshed every 5 min)
2. `cat OPERATIONAL_STATUS.md` (this file) — known state, tech debt, recent fixes
3. `cat AUDIT_2026-05-08.md` and `audit/code_integrity/SUMMARY.md` for the long-term audit context
4. Read the most recent ~5 entries of `audit/fixes/*.md` for the latest patches
5. Check `~/Scrivania/SEC/research/watchdog.log` tail for recent watchdog runs
6. Check `tail -50 pvsnp_explorer.log` to see what the explorer is doing right now

---

## Memory dependencies (Claude's persistent memory)

Memories that this document refers to:
- `project_sec_server_paths` — ~/SEC is diverged (D2)
- `project_sec_capabilities` — sandbox patch + audit log
- `project_sec_architecture` — ENTITY runtime location
- `project_sperimentalmath_audit` — skeptic gate diagnosis + test-gen fix
- `feedback_nvidia_apt_autoremove` — the costly NVIDIA reboot lesson

If those memories disagree with this document, **this document wins** (it is updated synchronously with system changes; memories may be stale).
