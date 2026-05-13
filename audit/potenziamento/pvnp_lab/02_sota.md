# PvsNP Lab — SOTA Comparison

5 SOTA systems for autonomous mathematical discovery and theorem proving.

---

## 1. AlphaProof (DeepMind, Nature 2025-11-12)

**What it does.** Reinforcement-learning agent that learns to prove
mathematical statements in Lean 4. Pairs a pretrained LM with AlphaZero-style
RL: the LM proposes tactics, MCTS searches proof trees, successful proofs
get distilled back into the policy (expert iteration). Trained on 80 million
**auto-formalized** statements pulled from natural-language sources. Reached
silver-medal on IMO 2024 (combined with AlphaGeometry 2 it solved P1, P2,
P4, P6).

**Capability key.** (a) Large-scale autoformalization → Lean training pairs,
(b) RL expert iteration over Lean proof states, (c) MCTS within tactic
search.

**URL.**
- Nature paper "Olympiad-level formal mathematical reasoning with
  reinforcement learning" — https://www.nature.com/articles/s41586-025-09833-y
- Blog — https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/

**What PvsNP Lab could learn.**
- Log every NL→Lean translation pair (success or fail) → grow a private
  training corpus; even without RL, fine-tune at periodic intervals via
  e.g. LoRA on this corpus is feasible.
- Treat each failed Lean gate attempt as a positive datapoint (failure
  reason → improve next prompt). Currently
  `pvsnp_lean_gate_log.jsonl` is logged but not learned-from.
- Introduce light MCTS / iterative best-first over tactic candidates in
  Level 3 instead of single LLM call per step.

---

## 2. AlphaGeometry / AlphaGeometry 2 (DeepMind, Nature 2024, arXiv:2502.03544 2025)

**What it does.** Neuro-symbolic geometry prover. Symbolic deduction engine
runs forward; if it gets stuck, a language model proposes a new auxiliary
construction (e.g. extend a line, drop a perpendicular) and the symbolic
engine resumes. AG2 (Gemini-based) extended the formal language to handle
ratios, distances, point movements, and added "knowledge-sharing search
trees" across multiple parallel beams. AG2 solves 42/50 IMO geometry =
above-gold; AG1 was silver.

**Capability key.** Hybrid loop: cheap deterministic deduction inside, LM
called only when stuck, with very narrow output schema (the auxiliary
construction primitive).

**URL.**
- AG1 Nature — https://www.nature.com/articles/s41586-023-06747-5
- AG2 paper — https://arxiv.org/abs/2502.03544
- Repo — https://github.com/google-deepmind/alphageometry

**What PvsNP Lab could learn.**
- Build a symbolic deduction engine over a **fragment** of complexity
  theory (e.g. CNF + clause width + treewidth + DPLL trees) — the LM is
  asked only when the deducer stalls. This is much more sample-efficient
  than today's "LLM proposes free-form Python test".
- AG2's "knowledge sharing between trees" maps directly onto F4
  framework engine: cross-conjecture lemma reuse via shared deduction
  store.

---

## 3. FunSearch (DeepMind, Nature 2023, code-named cap-set)

**What it does.** Evolutionary program search where the LM is the
mutation operator. Maintains an **island model** of program populations,
each program is scored by a Python evaluator, best programs are
prompted back to the LM to produce variants. Discovered new cap-set
constructions in F_3^n (a previously open extremal-combinatorics
problem) and improved online-bin-packing heuristics.

**Capability key.** (a) Population-based search (not a single best),
(b) program-not-answer (interpretable), (c) the evaluator is the source
of truth — LM hallucinations are filtered automatically.

**URL.**
- Nature — https://www.nature.com/articles/s41586-023-06924-6
- Blog — https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/
- Code — https://github.com/google-deepmind/funsearch

**What PvsNP Lab could learn.**
- The current explorer makes **one** test program per conjecture. A
  FunSearch island over the test program (5 islands × 10 programs each,
  60-min evolution) for each SUPPORTED candidate would massively
  strengthen the empirical signal before paying the Lean cost.
- For specific lower-bound constructions (Tseitin graphs, expanders,
  separators), FunSearch can directly search for **extremal
  constructions** — exactly the kind of object on which c003b
  counterexample search hinges.
- The same loop applies to **lower-bound proofs as Lean tactics**
  (program = tactic script).

---

## 4. LeanDojo + ReProver (Yang et al., NeurIPS 2023)

**What it does.** (1) LeanDojo is a tool that lets you interact with Lean
programmatically — extract every theorem, run tactic, inspect goal
state, build training datasets. (2) ReProver is a retrieval-augmented
prover: at each step, it embeds the current goal, retrieves top-k
relevant premises from Mathlib via dense vector search, then conditions
tactic generation on those premises. Benchmark: 51.2 % pass@1 on random
split, 26.3 % on novel-premises split.

**Capability key.** **Premise retrieval** — Mathlib has ~150k theorems;
without retrieval, the LM cannot possibly know which lemmas to invoke.

**URL.**
- Paper — https://arxiv.org/abs/2306.15626
- Site — https://leandojo.org/
- Code — https://github.com/lean-dojo/ReProver

**What PvsNP Lab could learn.**
- PvsNP Lab's Lean gate uses `exact?` / `loogle` (Lean's built-in
  premise search) and a single LLM tactic call. Replacing this with a
  ReProver-style **retrieval-then-generate** pass should give a big
  jump in pass@1 (the LeanDojo benchmark shows roughly 2× over pure
  generation).
- LeanDojo also provides a clean way to script Lean interactively from
  Python — pvsnp_lean_gate currently shells out to `lake build` for
  each attempt, which is slow (~4 min per import). Replacing with
  LeanDojo's persistent Lean kernel would dramatically reduce cycle
  time.
- LeanDojo's `accessible premises` analysis avoids cheating (you can't
  use a premise that wasn't yet defined). Today PvsNP Lab has no such
  guard.

---

## 5. AI Scientist v2 (Sakana AI, arXiv:2504.08066, Apr 2025 → Nature 2026)

**What it does.** End-to-end automated research agent: idea generation,
**agentic tree search** for code implementation, experiment execution,
figure plotting + VLM critique of figures, manuscript writing, peer-review
simulation. v2 dropped human templates and uses an experiment-manager
agent driving tree search over code variants. Three papers submitted
unedited to ICLR 2025 ICBINB workshop; one scored 6.33 (above human
threshold).

**Capability key.** (a) Tree search over **experimental design space**,
not just over solutions. (b) VLM critique of generated figures, which
catches a category of failures (mislabeled axes, missing baselines) that
text-only critics miss. (c) Full writeup loop including peer-review
simulation.

**URL.**
- Paper — https://arxiv.org/abs/2504.08066
- PDF — https://pub.sakana.ai/ai-scientist-v2/paper/paper.pdf
- Repo — https://github.com/SakanaAI/AI-Scientist-v2
- Nature 2026 — https://www.nature.com/articles/s41586-026-10265-5

**What PvsNP Lab could learn.**
- Manuscript-quality writeup loop: today `pvsnp_explorer.write_paper`
  is a single LLM call; v2's multi-pass (draft → check figures → revise
  → simulated review → revise) raises the quality bar without much
  extra cost.
- **VLM figure critique** for the plots produced by lab_c001
  experiments (linear_tw_fit, kill_fast) — easy to integrate, catches
  visual-only failure modes.
- Tree search over **test code variants** is the FunSearch idea
  re-skinned at a higher level — for any conjecture, generate a tree
  of test programs, prune by partial signal, branch deeper on
  promising leaves.

---

## Cross-cutting comparison

| Capability | AlphaProof | AlphaGeom2 | FunSearch | LeanDojo | AIS v2 | PvsNP Lab |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Autoformalize NL → Lean | yes (80M pairs) | n/a | n/a | n/a | partial | yes, one-shot, no training |
| RL / expert iter on Lean | yes | n/a | n/a | dataset only | n/a | **no** |
| Premise retrieval (Mathlib) | implicit via training | n/a | n/a | yes (DPR-based) | n/a | **no** (uses `exact?`) |
| MCTS / tree search tactics | yes | beam | island | beam | tree search | **no** |
| Island/population conjecture search | n/a | knowledge sharing | yes | n/a | tree search | **no** (1 seed → 5 reps only) |
| Symbolic deduction loop | partial | yes (DDAR) | n/a | n/a | n/a | **no** |
| VLM critique of figures | n/a | n/a | n/a | n/a | yes | **no** |
| Cross-conjecture lemma reuse | yes (Mathlib) | yes | n/a | yes | n/a | **partial** (F4 framework only) |
| Negative-result learning | yes (failures = training data) | partial | yes (eval signal) | n/a | yes | **partial** (logs but not trained) |
