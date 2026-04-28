---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-28 08:46 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-28 08:46 UTC

- Cycles recorded: **181**
- Time span: 107.1h (~1.69 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 159 |
| FALSIFIED | 14 |
| SUPPORTED | 4 |
| BARRIER_HIT | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier analysis of boolean functions | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Matroid Theory | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Random Matrix Theory | 2 |
| Combinatorial homotopy theory | 1 |
| Kazhdan-Lusztig theory of Hecke algebras | 1 |
| Combinatorial algebraic topology | 1 |
| Knot theory (quantum invariants) | 1 |
| Quadratic forms over finite fields (Grothendieck-Witt groups) | 1 |
| Clifford algebras over finite fields | 1 |
| Toric geometry (via Gröbner degenerations) | 1 |
| Arithmetic geometry (Tate-Shafarevich groups) | 1 |
| Geometric Langlands correspondence | 1 |
| Algebraic graph theory (chromatic polynomials) | 1 |
| Clifford algebras over real vector spaces | 1 |
| Algebraic cycles (Chow groups over finite fields) | 1 |
| Algebraic lattice theory (Möbius functions of flow lattices) | 1 |
| Directed algebraic topology (d-space homology) | 1 |
| Motivic integration (Denef-Loeser zeta functions) | 1 |
| Matroid theory (Clifford index of binary matroids) | 1 |
| Representation theory of finite groups (Frobenius-Schur indicator) | 1 |
| Categorification and knot Floer homology | 1 |
| Modular forms | 1 |
| Algebraic geometry (ideals in polynomial rings) | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-04-27 19:45 UTC | `INCONCLUSIVE` | Ihara Zeta Entropy Lower-Bounds DPLL Depth on 3-Regular Tseitin |
| 2026-04-27 20:12 UTC | `INCONCLUSIVE` | Hypercontractive p→2 Norm of Restriction Operator Bounds Resoluti |
| 2026-04-27 20:42 UTC | `BARRIER_HIT` | Median-Restriction Hardness Amplification Gap for DNF Truth Table |
| 2026-04-27 21:18 UTC | `INCONCLUSIVE` | Total-Influence Defect of Clause-Indicator Bounds Tree-Resolution |
| 2026-04-27 21:34 UTC | `BARRIER_HIT` | Diameter-Multiplicity Power Law under Controlled Refinement Recov |
| 2026-04-27 21:48 UTC | `INCONCLUSIVE` | Commutator-Length Defect in S_5 Predicts Width-5 BP Size of Boole |
| 2026-04-27 22:23 UTC | `INCONCLUSIVE` | Hessian-Rank of Clause-Count Polynomial Bounds DPLL Depth |
| 2026-04-27 22:52 UTC | `INCONCLUSIVE` | Herbrand-Disjunction Length of PHP Bounds Tree-Resolution Leaves |
| 2026-04-27 23:24 UTC | `INCONCLUSIVE` | Beck-Fiala Slack of Clause-Variable Hypergraph Bounds DPLL Leaves |
| 2026-04-27 23:36 UTC | `BARRIER_HIT` | Monotone Ultralimit Convergence of κ along the Asymptotic Complet |
| 2026-04-27 23:55 UTC | `INCONCLUSIVE` | Spectral-Tail Mass of Unit-Propagation Indicator Bounds DPLL Leav |
| 2026-04-28 01:39 UTC | `INCONCLUSIVE` | Block-Composition Sub-Additivity of Coarse Depth κ via the Roe-Tr |
| 2026-04-28 03:39 UTC | `INCONCLUSIVE` | Coboundary-Vanishing Threshold: HX^1 Triviality Below the Diamete |
| 2026-04-28 08:37 UTC | `INCONCLUSIVE` | Multiplicity-Doubling Lower Bound from Protocol Pullback on Index |
| 2026-04-28 08:46 UTC | `INCONCLUSIVE` | Σ^b_0-PIND Width-2 Closure Round-Count vs DPLL Leaves |

## How to read the reports

- `reports/supported_findings.md` — SUPPORTED conjectures with full test code. Paper-quality.
- `reports/falsified_findings.md` — FALSIFIED with counterexamples.
- `reports/daily_YYYY-MM-DD.md` — chronological log by day.
- `pvsnp_notebook.jsonl` — raw JSONL, one entry per cycle (source of truth).

## PDF export

Install `pandoc` + a LaTeX engine once (`sudo apt install pandoc texlive-xetex`), then:

```bash
cd research/reports
for f in supported_findings.md falsified_findings.md notebook_summary.md; do
    pandoc "$f" -o "${f%.md}.pdf" --pdf-engine=xelatex -V geometry:margin=2cm
done
```