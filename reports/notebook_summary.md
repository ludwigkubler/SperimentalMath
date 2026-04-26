---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-26 22:55 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-26 22:55 UTC

- Cycles recorded: **120**
- Time span: 73.2h (~1.64 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 101 |
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
| 2026-04-26 17:44 UTC | `INCONCLUSIVE` | Persistent Homology Bottleneck Distance Lower-Bounds Set-Disjoint |
| 2026-04-26 18:14 UTC | `INCONCLUSIVE` | Antichain Cover Number of KW Relation Lower-Bounds Monotone Formu |
| 2026-04-26 18:40 UTC | `INCONCLUSIVE` | Tropical Lipschitz Stability of Discrepancy under Fourier Coeffic |
| 2026-04-26 19:10 UTC | `INCONCLUSIVE` | Young-Tableau Cell Count Bounds Border-Rank of 3x3 Permanent Slic |
| 2026-04-26 19:40 UTC | `INCONCLUSIVE` | Lehmer Pair Density of Communication Matrix Lower-Bounds Discrepa |
| 2026-04-26 20:32 UTC | `FALSIFIED` | Tropical Self-Convolution Doubling Law for MinimalFourierCoeffici |
| 2026-04-26 20:50 UTC | `FALSIFIED` | Tropical Shift-Invariance of MinimalFourierCoefficient under Addi |
| 2026-04-26 20:54 UTC | `INCONCLUSIVE` | Hypercontractive (4,2)-Norm of Clause-Count Polynomial Bounds Res |
| 2026-04-26 21:31 UTC | `INCONCLUSIVE` | Tropical Tensor-Product Factorization of MinimalFourierCoefficien |
| 2026-04-26 21:34 UTC | `INCONCLUSIVE` | Dyadic Martingale Quadratic Variation Lower-Bounds Sign-Rank Disc |
| 2026-04-26 21:43 UTC | `INCONCLUSIVE` | Legendre-Fenchel Involution Conjecture: Discrepancy Invariance un |
| 2026-04-26 21:46 UTC | `INCONCLUSIVE` | Combinatorial Discrepancy of NW Designs Predicts Generator Bias o |
| 2026-04-26 22:20 UTC | `FALSIFIED` | Tropical Max-Aggregation Monotonicity of MinimalFourierCoefficien |
| 2026-04-26 22:22 UTC | `BARRIER_HIT` | Schur-Horn Majorization Gap Lower-Bounds Sign-Rank Discrepancy |
| 2026-04-26 22:55 UTC | `INCONCLUSIVE` | Pseudoexpectation Spectral Gap Lower-Bounds SoS Refutation Degree |

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