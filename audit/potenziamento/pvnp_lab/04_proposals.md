# PvsNP Lab — Concrete Proposals (max 10)

Ranked by Score from `03_gaps.md`. Each proposal cites at least one URL,
names exact files to modify under `~/kissat/pvnp_lab/...`, gives a first
test, and estimates man-hours.

---

## P1 — Premise retrieval (ReProver-style) for the Lean gate

**Description.** Replace the current single LLM-tactic call with a
retrieval-then-generate pass. Build a dense index once over (a) all of
Mathlib (already on disk under
`lab_c001/lean/TseitinTw/.lake/packages/mathlib`), (b) the lab_c001
local lemmas, (c) all PvsNP-Lab-verified stubs accumulated so far. At
each tactic step, embed the current proof goal, retrieve top-k (k=8)
premises, splice them into the LLM tactic prompt as candidate lemmas.

**Motivation + URL.** ReProver achieves 51.2% pass@1 (random) vs ~26%
without retrieval (LeanDojo, NeurIPS 2023).
- arXiv:2306.15626 — https://arxiv.org/abs/2306.15626
- ReProver code — https://github.com/lean-dojo/ReProver

**Files to modify.**
- New: `~/kissat/pvnp_lab/system_v2/src/pvsnp_lean_retriever.py`
  (~350 LOC).
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_lean_gate.py` —
  `_llm_tactic_step` and `_apply_level_2_tactics` take a `retriever`
  arg, splice top-k into the prompt.
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_lean_gate.py` —
  `run_lean_gate` constructs / loads the retriever once per process.

**Primer test.** Take 10 previously-FORMAL_VERIFIED entries from
`pvsnp_notebook.jsonl`, replay through `run_lean_gate` with and
without retrieval, measure pass@1 and median Lean attempts. Expect
≥2× pass@1 lift on adversarial replays where the proof needs an
obscure Mathlib lemma.

**Effort.** 14h (build index 4h + integrate 6h + benchmark 4h).

---

## P2 — Persistent Lean kernel via LeanDojo

**Description.** Today each `lake build` re-imports Mathlib (~4 min).
Adopt `lean-dojo`'s persistent-process API: open one Lean session per
project, send tactics over its stdin, receive goal state. Cycle time
should drop from ~6 min to ~30 s, enabling MUCH more aggressive tactic
search.

**Motivation + URL.** Same reference — LeanDojo provides the
`Dojo`/`Theorem` abstractions for interactive Lean.
- https://leandojo.org/

**Files to modify.**
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_lean_gate.py`. Replace
  `_lake_build` with a `LeanSession` wrapper; replace
  `_apply_level_*_tactics` with kernel calls. Likely 250 LOC delta.
- Possibly new: `~/kissat/pvnp_lab/system_v2/src/pvsnp_lean_session.py`
  containing the wrapper.

**Primer test.** Wall-clock time for one Lean gate cycle on a known
SUPPORTED entry before/after. Target ≥5x speedup.

**Effort.** 16h (install + scaffold 6h + port 6h + benchmark 4h).

---

## P3 — NL → Lean autoformalization corpus + nightly fine-tune

**Description.** Every call to `autoformalize` in
`pvsnp_lean_gate.py` already returns an NL conjecture + a generated
Lean source. Persist the pair (and a label `compiled / syntax_fail /
sorry_remained`) to `pvsnp_autoformalize_pairs.jsonl`. Add a nightly
cron that LoRA-fine-tunes a small open base model (Qwen2.5-Coder 7B or
DeepSeek-Math 7B) on this growing corpus. After K nights, swap the
`AUTOFORMALIZER_SYSTEM` to use the local fine-tuned model.

**Motivation + URL.** AlphaProof's 80M auto-formalization pairs are
the primary training signal; even at small scale, in-domain pairs
beat off-the-shelf models.
- Nature 2025-11 —
  https://www.nature.com/articles/s41586-025-09833-y

**Files to modify.**
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_lean_gate.py` —
  `autoformalize`, `repair_syntax` write a sidecar JSONL line.
- New: `~/kissat/pvnp_lab/system_v2/scripts/autoformalize_lora.py`
  (~200 LOC) — uses `peft` + `transformers`.
- New cron: edit `~/kissat/pvnp_lab/lab_c001/scripts/` to schedule
  nightly run on RTX 3070 Ti.

**Primer test.** After 1 week of logging, train LoRA, evaluate on
held-out 50 pairs. Compare BLEU on Lean source + lake-build success
rate against the off-the-shelf baseline.

**Effort.** 14h (logging 2h + LoRA pipeline 6h + smoke train + 6h
eval).

---

## P4 — FunSearch islands per conjecture

**Description.** When the explorer reaches the test-program stage, run
N=5 islands × M=10 programs evolutionary loop for K=15 minutes. The
LLM is the mutation operator: prompted with two parent programs from
the same island, asked to produce a child that improves the test
signal (e.g. larger gap between control and treatment, sharper
significance). Best program from any island is the one fed into the
multi-seed harness and critic.

**Motivation + URL.** FunSearch discovered new cap-set constructions
in F_3^n by exactly this loop.
- Nature 2023 — https://www.nature.com/articles/s41586-023-06924-6
- Code — https://github.com/google-deepmind/funsearch

**Files to modify.**
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.py` —
  `generate_and_run_test_with_retry` extended to drive island loop
  (or extracted to a new helper).
- New: `~/kissat/pvnp_lab/system_v2/src/pvsnp_funsearch.py` (~500
  LOC) — Island, Program, evolve_step.

**Primer test.** Pick 10 INCONCLUSIVE entries from the notebook;
re-run with islands; expect ≥3 to flip to SUPPORTED or FALSIFIED
with sharper statistics.

**Effort.** 18h (architecture 4h + impl 8h + replay benchmark 6h).

---

## P5 — Symbolic deduction engine for CNF/treewidth/proof-complexity

**Description.** Mini DDAR-style deducer over a small fragment of
proof complexity. Nodes: CNF formulae, clauses, variables, decision
trees, resolution proofs. Forward-deduction rules: subsumption,
unit propagation, clause-graph treewidth bounds, width-size
trade-offs, Tseitin parity-on-cycle facts. When the explorer's LLM
proposes a conjecture in this fragment, run deducer forward first;
verdict can be reached deductively without paying for sandbox
multi-seed.

**Motivation + URL.** AlphaGeom2's DDAR proves ~84% of olympiad
geometry **without** the LM. The asymmetry "cheap deducer first,
expensive LM only when stalled" is the right architecture for any
domain with a working symbolic engine.
- AG2 arXiv:2502.03544 — https://arxiv.org/abs/2502.03544
- Repo — https://github.com/google-deepmind/alphageometry

**Files to modify.**
- New: `~/kissat/pvnp_lab/system_v2/src/pvsnp_deducer.py` (~1200 LOC,
  pure Python).
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.py` —
  `run_one_cycle` calls `deducer.try_close(conj)` BEFORE the sandbox.
- Edit: `~/kissat/pvnp_lab/lab_c001/experiments/` — wire deducer into
  c003b counterexample loop.

**Primer test.** Replay 100 Tseitin-related conjectures from notebook;
count how many the deducer resolves outright vs how many it strictly
narrows (provides a lemma the sandbox didn't have).

**Effort.** 40h (5 dev-days), high-variance. Even partial coverage
pays off.

---

## P6 — MCTS / iterative best-first over Level-3 tactic candidates

**Description.** In `pvsnp_lean_gate._llm_tactic_step`, instead of
1 LLM call → 1 tactic, generate K=5 candidates per call. Apply each
in the (now-persistent — see P2) Lean kernel, score each leaf by
goal-state shrink (or LLM verdict on remaining difficulty),
best-first expand top-2. Total budget bounded.

**Motivation + URL.** AlphaProof uses AlphaZero-style MCTS. Even a
shallow K=5 fan-out, depth-3 search at human-feasible LLM cost gives
big gains over depth-1.
- AlphaProof Nature 2025 —
  https://www.nature.com/articles/s41586-025-09833-y

**Files to modify.**
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_lean_gate.py` —
  `_llm_tactic_step` → returns list[str]; new helper
  `_best_first_tactic_search(router, session, max_depth=3, fanout=5)`.

**Primer test.** Same 10 SUPPORTED replays as P1; measure pass@K vs
K. Expect pass@1 of MCTS run ≈ pass@5 of single-step.

**Effort.** 12h.

---

## P7 — Cross-conjecture / cross-framework lemma reuse

**Description.** Every FORMAL_VERIFIED Lean stub is currently in its
own isolated lake project. Auto-publish each verified theorem into a
shared private lake package `PvNPCommon`. The retriever (P1) indexes
that package too. F4 framework children inherit their parent's
verified lemmas as imports.

**Motivation + URL.** Mathlib's compounding-knowledge structure is
the reason ReProver works at all. LeanDojo paper §4 specifically
argues that **accessible-premise** indexing is what enables novel
premise generalization.
- LeanDojo arXiv:2306.15626 — https://arxiv.org/abs/2306.15626
- AG2 "knowledge-sharing trees" — arXiv:2502.03544

**Files to modify.**
- New: `~/kissat/pvnp_lab/system_v2/PvNPCommon/lakefile.toml` +
  per-conjecture `.lean` files.
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_lean_gate.py` —
  `_finalize_verified` writes a polished copy into PvNPCommon.
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_framework.py` —
  framework children import their parent's verified module.

**Primer test.** After 50 FORMAL_VERIFIED entries accumulate, count
how many later proofs invoke a previously-verified PvNPCommon lemma
(via P1 retrieval).

**Effort.** 14h.

---

## P8 — VLM figure critique stage

**Description.** After any plot is produced (lab_c001's
`make_plots.py`, system_v2's paper figures), pass the PNG to a
vision-capable LLM with a checklist (axes labeled, units, baseline
present, error bars, legend consistent with caption). If critique
fails, the figure is regenerated with the corrections, or flagged for
Ludo's review.

**Motivation + URL.** AI Scientist v2's plotting+VLM-critique stage
catches a class of failures that pure-text reviewers miss. Sakana
report: significant improvement in paper acceptance probability.
- AIS v2 arXiv:2504.08066 — https://arxiv.org/abs/2504.08066
- Repo — https://github.com/SakanaAI/AI-Scientist-v2

**Files to modify.**
- New: `~/kissat/pvnp_lab/system_v2/src/pvsnp_figure_critic.py`
  (~120 LOC).
- Edit: `~/kissat/pvnp_lab/lab_c001/experiments/make_plots.py` —
  after savefig, call `figure_critic.review(path)`.
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.write_paper`
  — pass each figure through the critic before LaTeX include.

**Primer test.** Mutate a working figure (delete axis label, swap
colors), confirm critic flags both.

**Effort.** 6h.

---

## P9 — Multi-pass manuscript polish loop (AIS v2 inspired)

**Description.** Today `pvsnp_explorer.write_paper` is one LLM call.
Replace with a 4-pass loop: (a) initial draft, (b) simulated
peer-review (3-LLM panel with reviewer-persona prompts), (c)
revision conditioned on reviews + the figure critique from P8, (d)
final copy-edit pass.

**Motivation + URL.** AIS v2 paper §3.4 explicitly attributes its
acceptance-quality output to the simulated-review loop.
- arXiv:2504.08066 — https://arxiv.org/abs/2504.08066

**Files to modify.**
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.py` —
  refactor `write_paper` to call new pipeline in
  `pvsnp_writeup_loop.py`.
- New: `~/kissat/pvnp_lab/system_v2/src/pvsnp_writeup_loop.py`
  (~250 LOC).
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_reviewer_pack.py` —
  reuse existing reviewer prompts.

**Primer test.** Take 5 recent paper drafts; run new loop; ask Ludo
to blind-rank old vs new.

**Effort.** 10h.

---

## P10 — Negative-result curriculum & hard-negative novelty embedder

**Description.** Today the explorer uses
`_build_blacklist(notebook)` to dedupe by raw text and embedding. We
miss two opportunities: (a) near-miss FALSIFIED conjectures should
seed proposer prompts as "avoid this exact pitfall — here is
counterexample", (b) the embedding model used for dedup is
off-the-shelf; fine-tune on (proposal, neighbor) pairs from notebook,
treating FALSIFIED/SCOOPED neighbors as hard negatives. Cheap
contrastive training.

**Motivation + URL.** AlphaProof uses failures as positive training
data (failure to prove = strong signal for the next iteration).
FunSearch's island elite-vs-trash split is the same principle.
- AlphaProof Nature 2025 —
  https://www.nature.com/articles/s41586-025-09833-y
- FunSearch Nature 2023 —
  https://www.nature.com/articles/s41586-023-06924-6

**Files to modify.**
- Edit: `~/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.py` —
  `_build_blacklist` becomes a richer prompt section
  `_build_negative_curriculum`.
- New: `~/kissat/pvnp_lab/system_v2/scripts/train_novelty_embed.py`
  (~150 LOC) — periodic contrastive fine-tune.
- Edit: `_embed_text` reads a local model path if present.

**Primer test.** Curate 30 historical "near duplicate but slipped
past dedup" pairs; measure embedding-cosine improvement after
contrastive training.

**Effort.** 10h.

---

## Cumulative effort: ~154 h ≈ 20 dev-days

Recommended sequencing:
1. P2 (Lean kernel) — unlocks throughput for everything Lean-side
2. P3 (autoformalize logging) — passive, no risk, compounds
3. P1 (retrieval) — biggest single win
4. P8 (VLM critic) + P10 (curriculum) — small, parallel
5. P6 (MCTS tactics), then P4 (FunSearch), then P9 (writeup polish)
6. P7 (lemma reuse), P5 (deducer) — biggest builds, last.
