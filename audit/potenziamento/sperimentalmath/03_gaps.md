# Gap analysis — sperimentalmath vs SOTA

Scoring rubric:
- **Impact** 1 (cosmetic) → 5 (existential / reputation-critical)
- **Effort** 1 (a few hours) → 5 (weeks of architecture)
- **Score** = Impact × (6 − Effort) / 5, rounded to 1 decimal; ties broken by Impact.

| # | Capability | In sperimentalmath? | In SOTA | Sytem | Impact | Effort | Score | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | **Retractions propagated to public reports** | NO — `retractions.json` exists, but `reports/supported_findings.md` still labels 4 retracted entries `SUPPORTED`. | YES — OSF / Retraction Watch keep the landing page and stamp it RETRACTED. | OSF, RW | 5 | 1 | 5.0 | Hardest reputation risk: any external reader hitting `supported_findings.pdf` sees stub-based results presented as confirmed. |
| 2 | **5-gate pipeline actually invoked** | NO — spec exists in `MULTIAGENT_PIPELINE.md`, but `health_report.skeptic_168h` shows `not_invoked: 405` and `hardened: 0` in the last 168 h. | n/a (sperimentalmath-specific) | self | 5 | 3 | 3.0 | The new pipeline must be wired into the daemon, not just specified. |
| 3 | **`lean_verified/` non-empty AND rigorous** | PARTIAL — 4 entries present, but `e14f176e4ef1/Eaudit.lean` self-declares "Float-based proofs are NOT rigorous over the reals". `cg_kw` is a programme scaffold without proofs. | Mathlib4: CI mandates `lake build` over `Real`/`Int`, not `Float`. | Mathlib4 | 5 | 4 | 2.0 | Need an "interval-arithmetic" upgrade (Mathlib `IntervalArith`) to make existing Lean files real-valued. |
| 4 | **Queueboard / public review dashboard** | NO — 1261 reviewer_packs exist but no index page; no way to know which are awaiting human review. | YES — Mathlib queueboard. | Mathlib4 | 4 | 2 | 4.0 | Trivial HTML/SSG over the JSONL would expose state to Ludo + outsiders. |
| 5 | **Pink-box / inline reviewer dialog** | NO — reviewer_packs are static PDFs; no comment-thread surface. | OEIS pink boxes, GitHub PR comments. | OEIS | 3 | 3 | 1.8 | Could be implemented as a GitHub Issue per entry + automated linking. |
| 6 | **Submission rate limit** | NO — 30 cycles/day uncapped; novelty filter trivially passed (many "Judge: NOVEL over 0 arXiv hits"). | YES — OEIS hard cap of 3 pending submissions per user. | OEIS | 4 | 1 | 4.0 | Cap *promotions* per day to (e.g.) 2; force prioritisation. |
| 7 | **Style sheet / canonical entry schema** | PARTIAL — JSONL rows have a stable schema, but reviewer packs vary; no top-level `SCHEMA.md`. | YES — OEIS Style Sheet enforced. | OEIS | 3 | 1 | 3.0 | Publishing the schema + linting JSONL would catch placeholder leaks at ingest. |
| 8 | **Dead-frameworks compendium populated** | NO — `frameworks/dead/` is empty, although `barriers/*.jsonl` has 4 categories of BARRIER_HIT and `stats.json` reports 18 such hits. | PolyMath wiki: explicit "approaches that did not work" page per project. | PolyMath | 3 | 2 | 2.4 | Auto-fill from `barriers/*.jsonl`. |
| 9 | **Source-code auditor (Gate 1 in pipeline)** | PARTIAL — defined in spec, not running. Three retracted SUPPORTED entries (§2.2-2.4 of AUDIT) would be caught by AST hard-coded-constant detector. | OSS: AST-based linters; Mathlib `lint`. | Mathlib4 | 5 | 2 | 4.0 | Highest-value safety net: AST-detect `return constant` in test harness. |
| 10 | **Honesty stamp / verification-level badges** | NO — README distinguishes "Lean-verified" vs "supported", but reports do not visibly tag each entry with its level. | DeepMind blog explicitly states "5/6 hand-formalised"; OSF stamps "retracted". | DeepMind, OSF | 4 | 1 | 4.0 | A 5-level badge (HAND_VERIFIED / LEAN_VERIFIED / SUPPORTED / INCONCLUSIVE / RETRACTED) printed next to every entry title. |
| 11 | **Auto-fix loop for INCONCLUSIVE crashes** | NO — 670 INCONCLUSIVE (94.8 % of cycles) are mostly crashed tests with no retry. | AlphaProof test-time RL: generates variants until success. | DeepMind | 4 | 4 | 1.6 | Even a simple "re-prompt the proposer with the crash trace" loop could convert 20-40 % of crashes into evaluable entries. |
| 12 | **Independent reproduction badge** | NO — `replay/*.tar.gz` exists but is never re-run by a separate machine/user. | Retraction Watch + OSF transparency&rigor index. | RW | 4 | 3 | 2.4 | A second daemon on a different host re-runs the tarball → adds `REPRODUCED_INDEPENDENT` flag. |
| 13 | **`reports/daily/` populated** | NO — directory exists but is empty; daily reports live in `reports/` root. | n/a | self | 1 | 1 | 1.0 | Cosmetic: either remove `reports/daily/` or move daily_*.md inside it. |
| 14 | **Top-level `INDEX.md` / `CATALOG.md`** | NO | OEIS lookup index; Mathlib `module_docs.json`. | OEIS | 3 | 1 | 3.0 | One-page index of all entries with verdict + badge + link to reviewer pack. |
| 15 | **External arXiv submission gate** | NO — `papers/compendium_v01.tex` exists, held back per AUDIT_2026-05-08; no checklist before submission. | Mathlib roadmap; DeepMind authorship process. | Mathlib4 | 3 | 2 | 2.4 | A `SUBMISSION_CHECKLIST.md` with mandatory tick-boxes. |

**Top 5 by score**: #1 retraction propagation (5.0), #4 queueboard (4.0), #6 rate limit (4.0), #9 AST auditor (4.0), #10 honesty badges (4.0).
