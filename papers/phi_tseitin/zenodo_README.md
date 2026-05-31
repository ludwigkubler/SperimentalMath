Now I have all the info needed. Generating the README.

# Replication package: Cumulative Clause-Space on Tseitin Formulas (Kubler, 2026)

## What is in this bundle

Reference harness and v2 analysis pipeline:

- `c003b_harness.py` — faithful Davis-Putnam variable-elimination harness that computes the cumulative proof entropy Φ(π) = Σ_t |activeClauses(σ_t)| on Tseitin formulas over random 3-regular graphs; per-cycle seed nonce, bad-order (max-occurrence) ablation at n=12, pure stdlib.
- `push_n.py` — v2 DP push-n extension (n=6..30 step 2, 10 seeds/n) with forward subsumption and tautology removal; emits `push_n_data.jsonl`.
- `push_n_kissat.py` — DRAT-replay Φ estimator (n=18..46 step 4, 5 seeds/n) using kissat as backend; emits `push_n_kissat_data.jsonl`.
- `drat_phi.py` — DRAT cross-check: generates Tseitin CNF, runs kissat with binary DRAT proof, replays step-by-step and computes Φ_drat = Σ_t |db_t|; emits `drat_table.txt`.
- `drat_mechanism.py` — DRAT-Φ mechanism diagnostic explaining the ~12x gap between DRAT-Φ (kissat) and DP-Φ over n=10..30 on identical instances; emits `drat_mechanism.txt` and `drat_mechanism_run.log`.
- `model_selection.py` — AIC/BIC model selection (power-law vs exponential vs stretched-exponential) with paired-by-seed bootstrap 95% CI; consumes both jsonl files plus `drat_table.txt`; emits `model_selection.txt`.
- `families.py` — Φ across graph families (path / star / grid / random-3-regular / random-4-regular); emits `families_table.txt`.
- `orders.py` — elimination-order sensitivity (five orders on identical instances); emits `orders_table.txt`.
- `structured_graphs.py` — structured Tseitin families isolating the degree-encoding confound from genuine expansion-driven Φ growth; emits `structured_table.txt` and `structured_results.json`.
- `weight_vs_count.py` — phi_weight vs phi_count gap analysis on random 3-regular Tseitin, n=6..18, 20 instances each; emits `weight_vs_count_table.txt`.

Data:

- `push_n_data.jsonl` — 130 records, DP harness, fields: n, instance, seed, m_edges, initial_clauses, phi_count, phi_weight, steps, derived_empty, blew_up, elapsed.
- `push_n_kissat_data.jsonl` — 40 records, kissat+DRAT-replay harness, fields: n, instance, seed, m_edges, n_vars, phi_count, phi_weight, steps, derived_empty, final_db, elapsed.

Tables and intermediate text artifacts:

- `model_selection.txt` — model-selection table; documents v1 misspecification (the v1 "power-law with exponent 2.9–3.0" headline is biased; the v1 slope drift 2.5 → 3.0 is a symptom of model misspecification under AIC).
- `structured_table.txt` + `structured_results.json` — structured-graph table (degree-confound ablation).
- `drat_table.txt` — DRAT cross-check artifacts at n ∈ {10,14,20,30}, 3 seeds/n.
- `drat_mechanism.txt` — mechanism-of-gap diagnostic.
- `families_table.txt`, `orders_table.txt`, `weight_vs_count_table.txt` — auxiliary tables.
- `push_n_table.txt`, `push_n_kissat_table.txt`, `push_n_run.log`, `push_n_kissat_run.log` — run logs and summary tables.
- `tiny.drat`, `tiny2.drat` — minimal DRAT fixtures used to validate the replayer.
- `itcs2017_cumulative.txt` — extracted reference notes (Beck/Impagliazzo/Razborov-style baselines) used in the v2 framing.

Pre-registration and prose:

- `preregistration_audit.md` — pre-registration audit document listing SC1..SC6, the registry timestamps, and the final adjudication of each statement against the v2 data.
- `paper_v2.md` — v2 manuscript draft (markdown source of the Zenodo prose).

Formal anchor:

- `Conjecture003.lean` — Lean 4 formalization of the Mirror Principle (Kubler, 2026) and the abstract `MirrorSystem` typeclass; shows that the composed lower bound is an instance of the Mirror Principle for regular resolution. Builds against the project's `TseitinTw` namespace (imports `TseitinTw.ComposedLowerBound`, `TseitinTw.Conjecture002`).

## How to reproduce

All Python scripts are pure stdlib, single-file, and pinned to `master_seed = 20260530`. Each `(n, instance)` seed is derived as `master_seed + n * 1009 + k`, so any subset can be re-run independently.

From a clean checkout of this bundle, on the canonical research host:

```
ssh ludo@sec
cd /tmp
python3 push_n.py                 # ~6 min,  emits push_n_data.jsonl
python3 push_n_kissat.py          # ~9 min,  emits push_n_kissat_data.jsonl (requires kissat 4.0.4 on PATH)
python3 drat_phi.py               # ~3 min,  emits drat_table.txt
python3 drat_mechanism.py         # ~4 min,  emits drat_mechanism.txt + drat_mechanism_run.log
python3 structured_graphs.py      # ~2 min,  emits structured_table.txt + structured_results.json
python3 families.py               # ~2 min,  emits families_table.txt
python3 orders.py                 # ~3 min,  emits orders_table.txt
python3 weight_vs_count.py        # ~1 min,  emits weight_vs_count_table.txt
python3 model_selection.py        # ~30 s,   emits model_selection.txt  (consumes the jsonl + drat_table.txt)
python3 c003b_harness.py 11 23 37 # ~1 min,  reference falsification trial on three seeds
```

Total end-to-end runtime on a single modern x86_64 core: approximately 30 minutes. No GPU is required. No network access is required after the bundle is downloaded.

To rebuild the formal anchor (optional):

```
cd lean/TseitinTw
lake update
lake build TseitinTw.Conjecture003
```

## Environment

- Python 3.12.3, pure stdlib only (no `numpy`, `networkx`, `pysat`, or third-party packages are imported by the harness or by `c003b_harness.py`; `model_selection.py` does import `numpy` for the AIC/BIC fitting step — install via `pip install numpy==1.26.*` if not present).
- kissat 4.0.4, invoked with binary DRAT proof emission (`-d`, binary mode); must be reachable as `kissat` on `PATH`.
- Linux x86_64 (developed on Linux 6.17, Ubuntu-family userland). No platform-specific code; macOS and other Unix are expected to work but are not pinned.
- Optional, for the formal anchor only: Lean 4 (elan-managed toolchain pinned by `lean-toolchain` in the Lean subtree) and mathlib at the revision pinned in `lake-manifest.json`.

## License

- Data (`*.jsonl`, `*.txt`, `*.json`, `*.drat`) and prose (`paper_v2.md`, `preregistration_audit.md`, this README): CC-BY-4.0.
- Code (`*.py`, `*.lean`): MIT.

Attribution in all cases: Ludovico Kubler. Please cite as

> Kubler, L. (2026). Cumulative Clause-Space on Tseitin Formulas. Zenodo. [DOI placeholder].

## DOI and version

- DOI: 10.5281/zenodo.XXXXXXX (placeholder — to be minted on upload).
- Bundle version: v2.0.0.
- Bundle date: 2026-05-30.
- Snapshot commit / archive checksum: [placeholder — to be filled by Zenodo at deposit].

## Pre-registration

This bundle is the empirical companion to a pre-registered study. See `preregistration_audit.md` in this bundle for the SC1..SC6 statements that were committed to the registry before the experiments ran, and for the final adjudication of each (CONFIRMED, REVISED, or FALSIFIED) against the v2 data. The pre-registry record itself is appended in machine-readable form to `pvsnp_preregistrations.jsonl` on the originating research host; the audit document reproduces the relevant lines verbatim along with their registry timestamps, so the bundle is self-contained for the purpose of reviewing the pre-registration / outcome correspondence.
