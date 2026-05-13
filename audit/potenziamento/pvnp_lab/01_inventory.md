# PvsNP Lab — Inventory

Date: 2026-05-13. Server: `ludo@sec`. Root: `~/kissat/pvnp_lab/` (= `/home/ludo/kissat/pvnp_lab/`).

## Top layout

```
pvnp_lab/
├── LICENSE
├── README.md
├── conjectures/
├── data/            (out, out_control, out_paper, c003b)
├── lab_c001/        (Conjecture-001 depth-first lab)
└── system_v2/       (breadth-first explorer + framework engine)
```

NB the code in `system_v2/src/*` is a mirror; the source of truth is at
`/home/ludo/Scrivania/SEC/src/research/pvsnp_*.py` and gets synced hourly
by `scripts/sync_from_sec.sh`. The repo is auto-committed every hour to
github.com/ludwigkubler/PvNP (last seen `master b10de09 ...11:17`).

## lab_c001 — depth-first lab (Tseitin / treewidth)

- `experiments/`: ~18 Python harnesses (`conjecture_001_kill_fast.py`,
  `conjecture_001_linear_tw_fit.py`, `conjecture_002_kill_fast.py`,
  `c003b_bsw_phi_test.py`, `controls_regression.py`, `cp_solver_test.py`,
  `drat_analysis.py`, `information_barrier_test.py`, `strategy_space.py`,
  `run_tseitin.py`, `run_tseitin_controlled.py`, `validate_results.py`).
- `lean/TseitinTw/`: ~45 .lean files including `TseitinPartialSat.lean`,
  `TseitinDelayerStrategy.lean`, `Conjecture001/002/003.lean`,
  `ExpanderTreewidth.lean`, `ProverDelayerGame.lean`, `Cut.lean`,
  `Separators.lean`, `SeparatorRecursion.lean`, `WidthSizeTseitin.lean`,
  `ComposedLowerBound.lean`, `TseitinAgreement.lean`, `Halving.lean`,
  `BridgeMeasure.lean`. Mathlib pulled into `.lake/packages/mathlib`.
- `scripts/`: watchdog (5 min), literature_scan (08:00 daily),
  c003b_counterexample (09:00), daily_report (18:00), monthly_report,
  git_sync (23:00), security_monitor, axiom_internalize, publish.
- `paper/`: LaTeX draft (`paper/versions/pvnp_draft_v20260410b.pdf`),
  figures.

Entry: `make -C lab_c001 run` or `make -C lab_c001 lean`.

## system_v2 — breadth-first explorer + framework engine

Entry: lives in sec-entity systemd service (autonomous `obligation PVSNP_EXPLORE`
every 30 min); not invoked locally.

### Source files (`system_v2/src/`, total 11,706 LOC)

Main pipeline:
- `pvsnp_explorer.py` — **2017 LOC**, the main pipeline (propose, embedding
  dedup, novelty arxiv+S2+ECCC, multi-seed test, critic, judge, write paper,
  write Lean stub, mutate, evolve). Key fns: `run_one_cycle`,
  `propose_conjecture`, `check_novelty`, `run_sandbox_multiseed`,
  `write_preregistration`, `critic_pass`, `judge_result`, `write_paper`,
  `write_lean_stub`, `mutate_conjecture`, `run_evolution_tick`.
- `pvsnp_barriers.py` — **608 LOC**, F1 dual-LLM barrier filter
  (Relativization / Natural Proofs / Algebrization / Karp-Lipton).
  `BARRIER_IDS=["RELATIVIZATION", "NATURAL_PROOFS", "ALGEBRIZATION",
  "KARP_LIPTON"]`, `CONFIDENCE_REJECT_THRESHOLD=0.60`, dual-LLM agreement
  required. Status: in progress.
- `pvsnp_lean_gate.py` — **471 LOC**, F3 Lean autoformalize +
  `lake build` + tactic search (Level 1 simp/decide/rfl/omega/norm_num,
  Level 2 exact?/loogle, Level 3 LLM-generated tactic step). Uses Mathlib
  from lab_c001. Status: in progress.
- `pvsnp_framework.py` — **679 LOC**, F4 framework engine. Fns:
  `propose_framework`, `elaborate_one`, `compute_fitness`, `classify`,
  `mutate_framework`, `framework_tick`. Thresholds dead=0.10,
  promoted=0.30, published=0.50. Status: planned (per README), but file
  is present.
- `pvsnp_taxonomy.py` (277 LOC) + `pvsnp_taxonomy.yaml`: F2 approach
  taxonomy (GCT, LIFTING, PROOF_COMPLEXITY_TSEITIN, BOUNDED_ARITHMETIC,
  ...). Each approach has status alive/partially_alive/dead, key_papers,
  barriers_not_triggered, weight.

Critic + meta:
- `pvsnp_skeptic.py` — 483 LOC adversarial critic.
- `pvsnp_reflection.py` — 398 LOC.
- `pvsnp_critic*` integrated in explorer.

Lean ancillary:
- `pvsnp_lean_proof.py` (354 LOC), `pvsnp_lean_counterexample.py` (498 LOC).

Search & corpus:
- `pvsnp_arxiv_mirror.py` (355 LOC) — local arXiv mirror.
- `pvsnp_citations.py` (387 LOC).
- `pvsnp_compendium.py` (464 LOC).
- `pvsnp_linkage_graph.py` (463 LOC).
- `pvsnp_few_shot.py` (283 LOC).

Reporting & ops:
- `pvsnp_report.py` (582), `pvsnp_monitor.py` (775),
  `pvsnp_reviewer_pack.py` (361), `pvsnp_review_alert.py` (251),
  `pvsnp_replay.py`, `pvsnp_weekly_replay.py`, `pvsnp_benchmark.py`
  (281), `pvsnp_compute.py` (534), `pvsnp_audit.py`,
  `pvsnp_sec_bridge.py` (258), `pvsnp_sec_diary.py`,
  `pvsnp_problem_focus.py` (260).

Misc: `orchestration/router.py`, `orchestration/claude_max.py`,
`replay_infra/Dockerfile.replay`, `replay_infra/replay_runner.sh`.

## Pipeline (verified vs design)

```
proposer
  -> embedding dedup (live)
  -> F1 barrier filter (in progress, dual-LLM, 4 barriers)
  -> preregistration (live)
  -> novelty arXiv+S2+ECCC (live)
  -> multi-seed test (live, 5 seeds)
  -> critic / skeptic (live)
  -> F3 Lean gate (in progress)
  -> paper + lean stub + notebook
```

Framework engine (F4) runs every 2h on its own cooldown.

## Data / state

- `SEC_ROOT=/home/ludo/Scrivania/SEC`, research data lives under
  `SEC_ROOT/research/`.
- `pvsnp_notebook.jsonl`: **708 entries**, 13.25 MB (as of 11:20 today).
- `pvsnp_preregistrations.jsonl`, `pvsnp_barriers_rejected.jsonl`,
  `pvsnp_frameworks.jsonl`, `pvsnp_dead_frameworks.jsonl`,
  `pvsnp_lean_gate_log.jsonl`, `pvsnp_taxonomy.yaml`.

## Capabilities already present

- Multi-seed sandbox (5 seeds default, mean/std/CI aggregation).
- Embedding-based dedup against historical proposals.
- Pre-registered acceptance criterion (Popper-style hash commit).
- Multi-source novelty (arXiv + Semantic Scholar + ECCC).
- Dual-LLM barrier filter (4 barriers) — in progress.
- Lean 4 autoformalize + `lake build` + 3-level tactic search — in progress.
- Adversarial critic LLM.
- Framework engine with 5 mutation operators + fitness — in progress.
- Curated taxonomy with weighted sampling.
- Local arXiv mirror.
- 24/7 cron + watchdog + auto-sync to GitHub.
- Weekly regression on known theorems (catches pipeline rot).

## Known gaps (skim)

1. **No retrieval-augmented Lean tactic prediction** (LeanDojo-style) —
   Level 2 uses raw `exact?` only, no premise retrieval over Mathlib.
2. **No FunSearch-style program-search island model** — proposer is a
   single LLM call per cycle, no evolutionary population of programs
   per conjecture.
3. **No AlphaProof-style RL/expert iteration** — Lean gate fails
   silently → EMPIRICAL_SUPPORTED, no learning from successes.
4. **No autoformalization training pair logging** — every NL→Lean
   conversion is thrown away when it fails.
5. **Critic is single-shot** — no debate / multi-agent agreement
   beyond barrier filter.
6. **Proposer has no problem-decomposition planner** — straight from
   high-level conjecture to executable test.
7. **No proof-state caching across Lean attempts** — each cycle
   restarts Mathlib import (~4 min lake build).
8. **No cross-conjecture lemma reuse** — Lean stubs are silos.
