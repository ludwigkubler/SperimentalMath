# SUMMARY — Code Integrity Audit

**Date:** 2026-05-13
**Scope:** 17,437 source files across 7 roots on `ludo@sec`
**Method:** read-only multi-agent scan (6 specialists + coordinator)
**Total LOC:** ~2.91 M (Lean 75% — mostly mathlib vendored — Python 21%, other 4%)

> Read **[00_DISCOVERIES.md](./00_DISCOVERIES.md)** first for the unexpected findings (ENTITY location, SEC divergence, mirror dupes). The rest of this summary aggregates the per-agent reports.

---

## Top 5 cross-cutting issues

1. **Two SEC trees exist on the server, with diverged source.** `~/SEC/` and `~/Scrivania/SEC/` are both 12 GB. Memory says only Scrivania survives — wrong. They share most module names but file contents differ (see [D2 in DISCOVERIES](./00_DISCOVERIES.md#d2)). Until reconciled, every fix has to be applied twice or someone is editing dead code. **Highest blast-radius issue in this report.**

2. **`~/Scrivania/future/` is the source of ~90% of issue volume but ~0% of actionable bugs.** It is dated LLM scratch directories (`research_*`, `practice_*`, `create_*`, ...). 91% of orphan files (373/409), 86% of dead public functions (2,701/3,128), and the bulk of ruff issues (E501/F401/W293/F821) live there. *Do not* "fix" this tree — archive or delete it instead.

3. **PvsNP framework lives in TWO copies between SEC and pvnp_lab.** Four files (`pvsnp_explorer.py`, `pvsnp_monitor.py`, `pvsnp_report.py`, `pvsnp_framework.py`, ~3,000 LOC total) are byte-identical across `~/Scrivania/SEC/research/` and `~/kissat/pvnp_lab/`. Extract to a shared library.

4. **Sandbox archive contains broken Python.** `~/Scrivania/SEC/research/pvsnp_sandbox/` and `.../sandbox_archive/` are full mirrors of each other (140+ files) and many fail `py_compile`. Pure noise; delete one tree.

5. **Anti-pattern volume is concentrated in non-project code.** Wav2Lip (third-party) and `Scrivania/future/` (autogen) account for almost all 50 HIGH-severity hits. The truly actionable items are: 2 `rm -rf "$WORK"` lines in `replay_runner.sh` (need `: "${WORK:?}"`), 4 `subprocess shell=True` in `pvnp_lab/scripts/*`, and ~20 `eval()`/`exec()` calls in the auto-generated research artefacts. **Zero hardcoded-secret literals found** — env-loading discipline is solid.

---

## Per-system health (1 = burning, 5 = healthy)

| System | LOC (k) | Files | Health | Notes |
|:-------|--------:|------:|-------:|:------|
| `~/Scrivania/SEC` (production) | ~600 | 2,838 | **3 / 5** | Bears most of the technical debt that *matters*. F821 in `src/`, dead functions in `worker.py`, `continuous_run.py`, `bridges/tseitin_tw/`. Tractable if `Scrivania/future` is excluded from metrics. |
| `~/SEC` (diverged fork) | small | 156 | **2 / 5** | Diverged from canonical SEC — invisible drift. See D2. |
| `~/kissat/pvnp_lab` | ~2,240 (mostly Lean) | 8,872 | **4 / 5** | Project-owned Lean has 96 `sorry`/`admit` in ~20 files; `mathlib/` vendored dominates raw size. 5 `sorry` align with `project_lean_sorry_status.md`. Python side is small. |
| `~/Scrivania/future` (autogen) | ~? | thousands | **1 / 5** | Disposable. ~90% of audit noise. |
| `~/tools/Wav2Lip` (vendored) | ~? | 28 | **N/A** | Third-party; not under our control. |
| `~/projects` (old) | ~? | 153 | **3 / 5** | Looks dormant. Worth a `git log --since=...` check. |
| `~/Scrivania/pubblicazioni` | tiny | a few | **5 / 5** | Mostly text. |

ENTITY (`~/Scrivania/SEC/src/entity/`, 17.9 K LOC) is a subset of `~/Scrivania/SEC` and shares its health rating.

---

## Top 10 most-problematic files

Ranked by **total issues across all 6 agents**. Wav2Lip and `Scrivania/future` excluded — they would otherwise dominate.

| Rank | File | Issues |
|----:|:-----|:-------|
| 1 | `~/Scrivania/SEC/research/pvsnp_sandbox/test_8baeebe4.py` | 289 ruff + duplicate of sandbox_archive copy |
| 2 | `~/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_8baeebe4.py` | 289 ruff (mirror of #1) |
| 3 | `~/Scrivania/SEC/src/monetization/continuous_run.py` | 9 dead public functions, strong cleanup target |
| 4 | `~/Scrivania/SEC/src/worker.py` | 6 dead public functions (likely cron-dispatched — verify before removing) |
| 5 | `~/Scrivania/SEC/research/pvsnp_sandbox/test_b400daf9.py` | 174 ruff + mirror |
| 6 | `~/Scrivania/SEC/research/git_mirrors/SperimentalMath/sandbox_archive/test_b400daf9.py` | 174 ruff (mirror) |
| 7 | `~/Scrivania/SEC/scripts/replay_runner.sh` | 2 unguarded `rm -rf "$WORK"` lines |
| 8 | `~/Scrivania/SEC/src/bridges/tseitin_tw/bridge.py` | 4 dead helpers |
| 9 | `~/kissat/pvnp_lab/<lean files with 5 sorry>` | aligned with known status |
| 10 | `~/Scrivania/SEC/src/entity/core.py.bak.20260428` | stale backup committed in-tree |

---

## Quick wins (estimated 50% of debt reduction)

In rough order of (impact × ease):

1. **Decide canonical SEC tree.** Either delete `~/SEC` or merge unique files (`monetization/sec_face_animator.py`, `sec_talking_head.py`, `youtube.py`) and *then* delete it. Updates memory ([D2](./00_DISCOVERIES.md#d2)).
2. **Delete one of `pvsnp_sandbox/` / `sandbox_archive/`.** They are mirrors. Removes ~140 broken Python files in one rm.
3. **Extract pvsnp_explorer/monitor/report/framework to a shared module.** 4 files × 2 copies → 4 files × 1 copy, lib used by both consumers. ~3,000 LOC dedup.
4. **`ruff check --select=F --fix` on `~/Scrivania/SEC/src/`.** Autofixes ~5K F401 (unused imports) issues in seconds with low risk. Triage F821 (undefined names — 2,810 total but the SEC subset is the actionable slice).
5. **Add `.ruffignore` for `tools/Wav2Lip/` and `Scrivania/future/`.** Future audits become 5× more signal-dense.
6. **Harden `replay_runner.sh`**: add `: "${WORK:?must be set}"` before the two `rm -rf "$WORK"` lines.
7. **Wrap `subprocess shell=True` in `~/kissat/pvnp_lab/scripts/`** (4 call sites) in a helper that defaults to `shell=False` + list args.
8. **Delete `~/Scrivania/SEC/src/entity/core.py.bak.20260428`** — stale backup in-tree.

---

## Discoveries (also see 00_DISCOVERIES.md)

- **D1** ENTITY = `~/Scrivania/SEC/src/entity/` (17,859 LOC, class `DigitalEntity`)
- **D2** `~/SEC` is diverged from `~/Scrivania/SEC` — memory says only one exists; both do
- **D3** `pvsnp_sandbox/` ≡ `sandbox_archive/` (mirror, both contain broken Python)
- **D4** 4 PvsNP-framework files duplicated across SEC and pvnp_lab (~3 K LOC)
- **D5** Hourly auto-sync commits drown the SperimentalMath git log
- **D6** `audit/` folder is flat-jsonl chaos (1,370 files at root)
- **D7** Runtime state lives in `~/data/` SQLite DBs, not in source roots
- **D8** Wav2Lip third-party code inflates anti-pattern counts
- **D9** Both SEC venvs diverged — pick one canonical lockfile
- **D10** Server is missing pyflakes/mypy/shellcheck/eslint/jscpd/sqlite3 — next audit will be richer with `apt install …`

---

## Corpus scanned

| Extension | Files | LOC |
|:----------|------:|----:|
| `.lean` | 8,924 | 2,193 K |
| `.py` | 6,348 | 601 K |
| `.js/.ts/.tsx/.jsx/.vue/.svelte` | 676 | ~80 K |
| `.sh/.bash` | 67 | ~5 K |
| Other (toml/yaml/sql/css/html/…) | ~1,420 | ~35 K |
| **Total** | **17,437** | **~2,914 K** |

---

## Methodology and caveats

- All execution via `ssh ludo@sec` from coordinator. Read-only, no commits during scanning.
- Linter coverage limited (pyflakes/mypy/shellcheck/eslint not installed). Ruff (0.15.12) was the only Python linter available; it was sufficient for E/F/W rule families.
- Dead-code analysis is heuristic — dynamically dispatched functions (cron entry points, decorator-routed handlers, framework callbacks) may be false positives. The Agent 4 report flags this.
- Duplication detection used custom Python n-gram hashing (W=40 tokens, S=10) since `jscpd`/`simian` not available. ~75% window-level duplication is dominated by stdlib prelude across LLM-generated test files; the *cross-system* clusters (top 20) are the actionable signal.
- Secrets check (P5 in Agent 6) returned **zero** literal matches and the report is verified clean — no apparent secret values were written into any audit file.

---

## Files in this audit

- `00_DISCOVERIES.md` — unexpected findings (read first)
- `01_inventory.md` — file counts, LOC, top-20 largest
- `02_static_python.md` — ruff + py_compile across 6,348 .py
- `03_static_other.md` — shell, lean, JS/TS, toml/yaml
- `04_dead_code.md` — 409 orphan files, 3,128 dead public functions
- `05_duplication.md` — top 20 clusters, ~3K LOC of full-file dupes
- `06_antipatterns.md` — security patterns + bug patterns, severity table
- `SUMMARY.md` — this file
