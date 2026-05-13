# SperimentalMath — Inventory (audit sub-agent #4)

**Date**: 2026-05-13
**Audit scope**: output sink of PvNP/system_v2 (the autonomous research engine).
**Repository under audit**: `ludwigkubler/SperimentalMath`
  - Server mirror: `~/Scrivania/SEC/research/git_mirrors/SperimentalMath/`
  - Remote: `git@github.com:ludwigkubler/SperimentalMath.git` (origin, main, up-to-date)
  - Latest commit on server: `5c33a5c auto: hourly sync 2026-05-13 10:47`
  - Cadence: hourly auto-sync via `sync_output.sh`

## 1. Path-target clarification

The audit brief named `~/Scrivania/future/` as the sperimentalmath path. That directory is **not** the sink. It is an unrelated SEC autonomous-learning output (LLM self-tasks under verbs `create/`, `experiment/`, `explore/`, `practice/`, `reflect/`, `research/`, 3903 generated files of toy code/READMEs, hourly LLM exercises). The actual sperimentalmath sink lives at `~/Scrivania/SEC/research/git_mirrors/SperimentalMath/`. This inventory targets the latter.

`~/Scrivania/pubblicazioni/` is a separate sink (alerts and daily reports). Not the same as sperimentalmath.

## 2. Top-level layout

```
SperimentalMath/                 (≈ 5.6k objects, hourly-synced)
├── README.md                   (3.0 KB; declares no-false-positive policy)
├── AUDIT_2026-05-08.md         (9.3 KB; published self-audit, 9 retractions)
├── MULTIAGENT_PIPELINE.md      (12 KB; 5-gate review system spec)
├── retractions.json            (5.8 KB; 8 RETRACTED + 1 DEMOTED entries)
├── stats.json                  (1.0 KB; cumulative counters)
├── health_report.{json,md}     (daemon + cycle health)
├── claude_max_call_log.jsonl   (312 KB)
├── monitor_alerts.jsonl        (188 KB)
├── few_shot_examples.md, sync.log, sync_output.sh
├── arxiv_mirror_state.json, arxiv_mirror_stats.json
├── notebook/                   (per-month JSONL: 2026-04.jsonl, 2026-05.jsonl)
├── frameworks/                 (proposed/promoted/published/dead)
├── papers/                     (cg_kw_programme, maslov_rate, wall_atlas, compendium_v01.{tex,pdf})
├── lean_verified/              (cg_kw, cg_kw_mathlib_v0, e14f176e4ef1, e14f176e4ef1_mathlib_v0)
├── lean_stubs/                 (EMPTY)
├── lean_counterexamples/       (3 .lean + build log)
├── barriers/                   (natural_proofs, relativization, algebrization, karp_lipton JSONL)
├── audit/                      (1371 per-entry JSONL traces)
├── reports/                    (daily logs, supported_findings, falsified_findings, …)
├── replay/                     (680 .tar.gz reproducibility tarballs)
├── replay_reports/, review_alerts/ (4 digests), reports/daily/ (currently empty)
├── reviewer_packs/             (1261 files: .md + .pdf per entry)
├── citations/                  (623 JSON files)
├── compute_evidence/           (44 JSON: TARGET_MONOTONE_NP_GAP_*)
├── sandbox_archive/            (test harness archives)
├── daily_reflection/, linkage_graph/
```

## 3. Counts

| Counter | Value |
|---|---|
| total_cycles (stats.json) | 707 |
| verdict INCONCLUSIVE | 670 |
| verdict SUPPORTED | 4 |
| verdict FALSIFIED | 15 |
| verdict BARRIER_HIT | 18 |
| unique field_A | 432 |
| cycles last 24 h (health) | 54 |
| claude_calls 168 h | 674 / 2500 (27 %) |
| skeptic gate hardened/downgrade/not_invoked 168 h | 0 / 0 / 405 |
| audit traces (audit/) | 1371 |
| reviewer packs (reviewer_packs/) | 1261 |
| replays (replay/) | 680 |
| citations (citations/) | 623 |
| lean_verified entries | 4 (= 2 distinct + Mathlib-port variants) |
| lean_stubs entries | 0 |
| frameworks proposed / promoted / published / dead | 6 / 0 / 0 / 0 |

## 4. SUPPORTED / FALSIFIED inventory vs retractions

**`reports/supported_findings.md`** still lists 4 entries (`15ae8fd62af0`, `e006a48b37a7`, `b43a4129e5c5`, `7cbbaa3e1e4a`) as SUPPORTED.

**`retractions.json`** says:

- `e006a48b37a7` → RETRACTED (stub: hard-coded constants)
- `b43a4129e5c5` → RETRACTED (pure stub: `n ≤ 2n`)
- `7cbbaa3e1e4a` → RETRACTED (malformed matrix; XNOR artefact)
- `15ae8fd62af0` → DEMOTED to INCONCLUSIVE pending reformulation

→ **All 4 publicly-SUPPORTED entries are actually retracted/demoted in `retractions.json`. The user-facing report was NOT regenerated** after the 2026-05-08 audit. This is a hard inconsistency.

**`reports/falsified_findings.md`** lists 15 FALSIFIED entries; retractions.json says 6 of them are RETRACTED:

- `b5f9314580e6` Lattice of Flows (vacuous: enumeration skipped)
- `a8b5663ca867` Khovanov (degenerate counterexample)
- `cb842205136a` Noncommutative Algebra (stub)
- `32a1e966ed26`, `44f82c29ed79`, `cca077d3c64c` Tropical Fourier sub-conjectures (Gate 1/2 fail under new pipeline)

The remaining "principal scientific output" per AUDIT_2026-05-08 was the **Tropical Fourier cluster** of 4 entries — but the audit JSON now retracts 3 of those 4. Only `e14f176e4ef1` (Tropical Self-Convolution Doubling Law) survives, and only as a Float-arithmetic Lean witness (the file itself notes "Float-based proofs are NOT rigorous over the reals").

## 5. README / INDEX

- `README.md`: present, explicit no-false-positive policy.
- `AUDIT_2026-05-08.md`: present, lists action items and demotions.
- `MULTIAGENT_PIPELINE.md`: present, 5-gate spec (AUDITOR → MATHEMATICIAN → LITERATURE SCOUT → LEAN-FORMALIZER → ROYAL-SOCIETY).
- No top-level `INDEX.md` / `CATALOG.md` summarising the 707 entries.
- No machine-readable schema for the JSONL rows shared.
- No badge / verification-level legend (e.g. "FORMAL_VERIFIED", "DOUBLE_BLIND_REPRODUCED").

## 6. Retraction surface

`grep -rln 'retract\|withdrawn\|deprecated'` matches in this repo: `retractions.json`, `AUDIT_2026-05-08.md`, several reviewer packs, and `frameworks/dead/` (currently empty). There is **no automatic mechanism** that propagates `retractions.json` into `reports/supported_findings.md` or stamps the corresponding `notebook/2026-04.jsonl` row as retracted. Retractions are documented but **not enforced** at the public-facing layer.

## 7. Pipeline / cycle health (snapshot 2026-05-13 06:17 UTC)

```
status:        OK
daemons:       1 (PID 944529)
zombies:       0
last cycle:    0.14 h ago
cycles 24 h:   54
disk used:     13 %
skeptic gate (last 168 h):
  hardened    0
  downgrade   0
  not_invoked 405
```

→ The skeptic / multi-agent pipeline introduced in AUDIT_2026-05-08 is **not being invoked**: 405 cycles bypassed it. No conjecture has been hardened or downgraded by the new pipeline in the past week. The new pipeline exists on paper but is not gating the live engine.

## 8. Quick wins observed in the repo

- `replay/*.tar.gz` (680 entries) + `reviewer_packs/*` (1261 files) are excellent: each candidate ships with a reproducible sandbox + PDF reviewer pack. This is already SOTA.
- `audit/*.jsonl` records every LLM phase (propose, preregistration, …) with input/output, latency, model. Strong provenance.
- `barriers/*.jsonl` and `compute_evidence/TARGET_MONOTONE_NP_GAP_*.json` show the system records barrier hits and follows a long-running target.
- `papers/compendium_v01.{tex,pdf}` exists but per AUDIT_2026-05-08 is "held back from external submission" until the Tropical-Fourier cluster is independently reproduced + Lean-verified. Per retractions.json, 3 of the 4 cluster entries are now retracted, so the compendium needs major surgery.
