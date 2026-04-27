---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-27 04:57 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-27 04:57 UTC

- Cycles recorded: **133**
- Time span: 79.3h (~1.68 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 114 |
| FALSIFIED | 14 |
| SUPPORTED | 4 |
| BARRIER_HIT | 1 |

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
| Tropical geometry | 2 |
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
| Hypergraph Tutte polynomials | 1 |
| Galois theory of finite field extensions | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-04-26 22:22 UTC | `BARRIER_HIT` | Schur-Horn Majorization Gap Lower-Bounds Sign-Rank Discrepancy |
| 2026-04-26 22:55 UTC | `INCONCLUSIVE` | Pseudoexpectation Spectral Gap Lower-Bounds SoS Refutation Degree |
| 2026-04-26 23:26 UTC | `INCONCLUSIVE` | Mahler Measure of Signed-Degree Polynomial Bounds ACC^0[6] Size |
| 2026-04-26 23:56 UTC | `INCONCLUSIVE` | Sample-Compression Gap Predicts Worst-Case DPLL Depth on Random 3 |
| 2026-04-27 00:22 UTC | `INCONCLUSIVE` | Tropical Affine Rigidity: Vanishing Discrepancy iff Single-Atom F |
| 2026-04-27 00:31 UTC | `INCONCLUSIVE` | Continued Fraction Depth of Spectral Ratio Bounds Discrepancy |
| 2026-04-27 01:05 UTC | `INCONCLUSIVE` | Young-Flattening Rank Gap Lower-Bounds Padded-Permanent Border Ra |
| 2026-04-27 01:38 UTC | `INCONCLUSIVE` | Pebble-Cost Gadget Lifts Decision Tree Depth to KW-Game Length |
| 2026-04-27 02:14 UTC | `INCONCLUSIVE` | Mealy Automaticity Lower-Bounds Truth-Table Formula Size |
| 2026-04-27 02:28 UTC | `INCONCLUSIVE` | Tropical Positive-Scalar Homogeneity of MinimalFourierCoefficient |
| 2026-04-27 02:42 UTC | `INCONCLUSIVE` | Permanent-Variance of NW Design Matrix Predicts PRG Bias |
| 2026-04-27 03:18 UTC | `INCONCLUSIVE` | Cycle-Space Cocycle Imbalance Lower-Bounds Resolution Width of Ts |
| 2026-04-27 03:49 UTC | `INCONCLUSIVE` | Halton Star-Discrepancy of Clause-Sign Embedding Bounds DPLL Leav |
| 2026-04-27 04:23 UTC | `INCONCLUSIVE` | Erdős–Ko–Rado Shadow Defect Lower-Bounds Disjointness Discrepancy |
| 2026-04-27 04:57 UTC | `INCONCLUSIVE` | Edge-Expansion Defect Predicts Resolution Width of Tseitin on Ran |

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