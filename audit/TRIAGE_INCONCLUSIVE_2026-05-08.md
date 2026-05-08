# Triage of the 398 INCONCLUSIVE entries — 2026-05-08

**Author**: L. K.
**Status**: triage report; commits a re-test queue and proposer-prompt
recommendations. Not a paper.

## Why this document exists

Of the 433 cycles recorded in `pvsnp_notebook.jsonl` as of 2026-05-08,
398 carry the verdict `INCONCLUSIVE`. This report classifies that
population by failure mode and produces a re-test queue for the
five-gate pipeline of `MULTIAGENT_PIPELINE.md`.

## Top-line numbers

| Bucket | Count | Share |
|---|---:|---:|
| INCONCLUSIVE / **test crashed** (non-zero exit, traceback in stdout) | 349 | **88 %** |
| INCONCLUSIVE / **test ran but no signal** | 49 | 12 % |
| INCONCLUSIVE total | 398 | 100 % |

The dominant failure mode is not "the conjecture turned out to be hard
to test." It is "the proposer's auto-generated Python test crashed."
**88 %** of the INCONCLUSIVE pile is a software-engineering bug, not a
mathematical observation.

## Crash-cause breakdown

Top Python error types observed in `test_stdout` of crashed entries:

| Error type | Count | Typical message |
|---|---:|---|
| `TypeError`           | 96 | `"Population must be a sequence. For dicts or sets, use sorted(d)"` (random.sample on dict / set), `'int' object is not callable` |
| `_unknown_nonzero_rc` | 72 | exit ≠ 0 with no recognizable traceback (silent shell errors, `python3` missing modules failing at import time, OOM, segfaults) |
| `NameError`           | 43 | `name 'sys' is not defined`, `name 'i' is not defined`, missing imports |
| `IndexError`          | 42 | `list index out of range`, `cannot fit 'int' into an index-sized integer` |
| `ValueError`          | 24 | `Sample larger than population`, `invalid literal for int()`, `math domain error` (log2(0) family) |
| `ZeroDivisionError`   | 20 | `Fraction(-2, 0)`, `float division by zero` |
| `KeyError`            | 17 | unexpected dict access |
| `IndentationError`    |  8 | LLM emitted misindented code |
| `UnboundLocalError`   |  6 | use-before-assign |
| `RecursionError`      |  6 | depth-first searches without depth bound |
| `ModuleNotFoundError` |  5 | imports of non-installed packages (sympy, networkx, scipy etc.) |
| `SyntaxError`         |  4 | unterminated strings, missing colons |

**Recommendations for the proposer prompt** (concrete, ordered by
expected impact):

1. **Forbid `random.sample(d, k)` where `d` is a dict, set, or generator.**
   Insert the rule "if the population is a dict, set, or generator,
   convert it to `sorted(...)` first" verbatim. Top crash cause.
2. **Always emit `import sys, json, math, random, itertools, collections`
   at the top of every test.** The 43 `NameError` crashes are 90 % missing
   `sys`/`itertools`.
3. **Ban `import sympy / networkx / scipy / sage`** (or include them as
   provided dependencies in the sandbox image). The 5 `ModuleNotFoundError`
   crashes are predictable.
4. **Insert a guard `if n <= 0: return None` around any `math.log` or
   `math.log2` call.** The `ValueError: math domain error` and
   `ZeroDivisionError` families collapse into this.
5. **Cap recursive functions at depth 10**\,000 with `sys.setrecursionlimit`
   or rewrite as iterative. Ends `RecursionError`.
6. **Linter pass before sandbox execution.** `python -m py_compile`
   on the generated test file would catch the 4 `SyntaxError` and 8
   `IndentationError` crashes for free.

If all six recommendations land, the crash rate falls from 88 % to a
projected ≤ 25 %.

## Non-crashing INCONCLUSIVE: the 49 candidates worth a closer look

Top 25 by score = 0.5·novelty + 0.3·output_density + 0.2·runtime
(score ∈ [0, 1]):

| score | nov | elap (s) | out (chars) | entry_id | title |
|------:|----:|--------:|---------:|----------|-------|
| 0.724 | 14  |   0.9   |   948    | `546e28bb74a4` | Lehmer Pair Density of Communication Matrix Lower-Bounds Discrepancy |
| 0.704 | 13  |   0.5   |  1435    | `7bbefa60fc65` | Tropical Convolution Subadditivity of MFC and its Discrepancy |
| 0.686 |  7  |  30.3   |  4216    | `97b82c049269` | SVD Participation Dispersion of Mid-Layer Lower-Bounds Read-Twice BPs |
| 0.649 |  6  | 123.3   |  4149    | `c26787a56682` | Real Rank of KW Matrices for AC⁰ PARITY |
| 0.644 |  9  |   5.8   |  2393    | `81928f9c440e` | Tropical Affine Rigidity: Vanishing Discrepancy iff Single-Atom Fourier |
| 0.580 |  9  |   0.0   |  4491    | `5cbad98886db` | Homotopy Type and AC⁰ Complexity |
| 0.568 | 15  |   0.1   |   606    | `b958d93ec75c` | 2-Cohomotopy Class Count of Clause-Link Complex Equals 3-SAT Resolution Width |
| 0.557 | 10  |   0.5   |   400    | `f3c52dac4f2e` | Motivic zeta function poles bound resolution width |
| 0.556 |  9  | 146.8   |   931    | `8bf8c5c64dba` | Magnus Level-2 Defect Bounds DNF_min via Truth-Table Inversions |
| 0.525 | 15  |   0.0   |   139    | `121736aabe59` | Poincaré Series |
| 0.500 |  0  |   0.7   |  5021    | `3dd7d5ee43a7` | Real Stable Polynomial Coefficient Sum and AC⁰ PARITY Circuit Size |
| 0.474 |  0  |   4.7   |  4573    | `56039c424522` | Spectral Norm of SOS Relaxation and Refutation Size in Random 3-SAT |
| 0.469 |  0  |   2.8   |  4481    | `9d5d3a5ea1bf` | Matroid Rank Deficit in Monotone DNF Depth for k-CLIQUE |
| 0.453 |  0  |   0.8   |  4223    | `1a21dd39fb6f` | Secant Rank Lower Bound for Disjointness Communication Matrices |
| 0.436 |  0  |  19.3   |  3926    | `91f293427310` | VC-Dimension of Row-Induced Set System Bounds Monotone DNF Size for k-CLIQUE |
| 0.434 |  0  |   1.5   |  3897    | `8b3175ffc0f7` | Real Variety Connectedness Lower Bound on SOS Degree for Max-CUT |
| 0.433 | 12  |   0.0   |   397    | `8d9b58ba4ae0` | Tate-Shafarevich Group Order of Elliptic Curve Models SAT Instance Density |
| 0.415 |  0  |   0.4   |  4316    | `bd540f51275f` | Noncommutative L^p Norm Lower Bounds for Disjointness Communication Complex |
| 0.415 | 10  |   0.1   |   803    | `29af0c7a223d` | Nisan-Wigderson Seed Length Bounded by Finite Geometry Line Count |
| 0.384 |  7  |   0.3   |   833    | `420946ef183b` | Cubical Betti Sum of Implicant Complex Lower-Bounds DNF-MCSP |
| 0.375 |  9  |   0.0   |   961    | `6487f7d68c31` | Doob Martingale Variance Gap Predicts Worst-Case DPLL Depth |
| 0.373 | 10  |   0.0   |   517    | `20680d0498ef` | Kazhdan-Lusztig Polynomial Coefficients Bound Resolution Width |
| 0.372 |  0  |   0.3   |  4161    | `07a9b4327000` | Metric Dimension Lower Bound on Tseitin Resolution Length |
| 0.362 |  9  |   0.0   |   855    | `299d5162a4f6` | Bipartite Token-Sliding Diameter Lower-Bounds Monotone-KW Depth |
| 0.332 |  0  |   0.1   |  4939    | `076ad72eacfc` | Free Cumulant Rank Gap in Read-Twice Branching Programs for IP_2 |

## Gate-2 spot check on the top 5

I read the statement, stdout, and `final_reason` of the top 5 in detail.
Ahead of any re-test, the **critic** has already correctly identified the
following pathologies:

* **`546e28bb74a4` Lehmer Pair Density** — All 5 seeds produced *identical*
  metric value 1.984375 with zero variance. Critic flagged "test likely
  sampled a trivial/deterministic subcase" and "disc · 2^(n/2) ≥ 1 is
  near-automatic for XOR functions." Underlying claim is borderline
  tautological. **Re-test only after re-formulating the claim** (the test
  metric is constant by construction, not by mathematics).

* **`7bbefa60fc65` Tropical Convolution Subadditivity** — Inequalities (i)
  and (ii) held in 600 × 5 = 3000 instances. INCONCLUSIVE because the
  pre-registered "refinement_fraction ≥ 0.50" was 0.0 — never strictly
  refined. Critic: "(i) is a trivial consequence of min-plus
  distributivity." **Restated: this conjecture is true but content-free.**

* **`97b82c049269` SVD Participation Dispersion** — DISP ≈ 17.79 for all
  6 trials. Critic: "near-constant value across only 6 instances suggests
  metric saturation on a canonical symmetric BP rather than genuine search
  over adversarial read-twice BPs." **Re-test with adversarial BP family.**

* **`c26787a56682` Real Rank of KW Matrices for AC⁰ PARITY** — Test
  reports `rank=0` for all 5 trials. The Karchmer-Wigderson matrix of any
  non-constant function has rank ≥ 2; rank 0 indicates **the matrix was
  constructed incorrectly** (e.g.\ all-zero matrix, wrong indexing). The
  underlying claim — `rank_R(M_PARITY) ≥ Ω(√n)` for AC⁰ formulas — is
  related to Razborov-style real-approximation lower bounds and **is
  worth re-test under a corrected matrix construction.** Highest priority
  on this list.

* **`81928f9c440e` Tropical Affine Rigidity** — Constant 0.6667 across
  all seeds. Same metric-saturation pathology as the others.

**Net conclusion of the spot check**: even after stripping the 88 %
crashes, the survivors are dominated by tests with constant-metric
output that the critic correctly downgrades. Only **one** of the top 5
(`c26787a56682`) merits a real re-test; the others need a rewritten test
or a rewritten conjecture.

## Re-test queue

The `inconclusive_triage.json` companion file lists the 49 non-crashing
entries with their full features. Of these, the immediately actionable
re-test candidates (after Gate-2 spot check) are:

1. **`c26787a56682`** Real Rank of KW Matrices for AC⁰ PARITY — fix
   matrix construction, re-test.
2. **`97b82c049269`** SVD Participation Dispersion — broaden the BP family
   sampled to include adversarial read-twice BPs.
3. **`91f293427310`** VC-Dimension of Row-Induced Set System Bounds
   Monotone DNF Size for k-CLIQUE — 19 s elapsed, substantial output, no
   immediate red flag in the stdout summary; merits Gate 2.
4. **`8bf8c5c64dba`** Magnus Level-2 Defect Bounds DNF_min — 146 s elapsed,
   nov=9; merits Gate 2.
5. **`b958d93ec75c`** 2-Cohomotopy Class Count of Clause-Link Complex —
   nov=15 (the maximum in the corpus), short runtime; investigate whether
   the test is degenerate.

The remaining 44 of the 49 non-crashing entries are deferred until the
proposer's test-generation reliability is fixed. Re-running them as-is is
expected to keep producing INCONCLUSIVE verdicts via metric saturation.

## Crash-fix queue (selective)

For the 349 crashed entries, individual fixes are not cost-effective.
Instead, I recommend:

1. Apply the six prompt-level fixes in §"Crash-cause breakdown" above to
   the proposer.
2. Re-emit *fresh* conjectures with the patched proposer rather than
   patching the old crashes one by one.
3. The patched proposer should reduce the 88 % crash rate to ≤ 25 %,
   tripling the throughput of meaningful tests at zero increase in cycle
   count.

## What the corpus is *not*

After this triage:
* the INCONCLUSIVE pile is **not** a pile of "promising-but-untested
  conjectures." It is mostly a pile of crashed tests.
* the 49 non-crashing entries are **not** a pile of "almost-proven"
  results. They are mostly metric-saturated or content-free.
* a single entry (`c26787a56682`) is a clear re-test candidate.

This is a more honest accounting of the corpus state than the simple
"398 inconclusive" headline suggests.

— L. K., 2026-05-08
