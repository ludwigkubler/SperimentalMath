---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-10 00:30 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-10 00:30 UTC

- Cycles recorded: **513**
- Time span: 386.8h (~1.33 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 478 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 25 |
| Free Probability | 12 |
| Schur-Weyl Duality | 12 |
| Representation Theory of Symmetric Groups | 10 |
| Matroid Theory | 9 |
| Algebraic Geometry | 7 |
| Random Matrix Theory | 6 |
| Additive Combinatorics | 6 |
| Spectral Graph Theory | 6 |
| Polymatroid Theory | 6 |
| Finite Geometry | 5 |
| Plethysm Theory | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Fourier analysis of boolean functions | 3 |
| Algebraic Topology | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl duality | 3 |
| Persistent Homology | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Tropical geometry | 2 |
| Schur-Weyl duality, plethysm, algebraic combinatorics | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-09 20:05 UTC | `INCONCLUSIVE` | Newton Polytope Vertex Count Inverse Proportional to SOS Degree f |
| 2026-05-09 20:11 UTC | `INCONCLUSIVE` | Real Stable Polynomial Degree Lower Bound for Max-CUT SOS |
| 2026-05-09 20:27 UTC | `INCONCLUSIVE` | Young Tableau Count Inverse Proportional to Monotone Circuit Size |
| 2026-05-09 21:07 UTC | `INCONCLUSIVE` | Real Root Count Inverse Proportional to SOS Degree for Max-CUT |
| 2026-05-09 21:15 UTC | `INCONCLUSIVE` | Betti Number Inverse Proportionality to DPLL Tree Size in 3-SAT |
| 2026-05-09 21:30 UTC | `INCONCLUSIVE` | Schur-Weyl Decomposition Irreducible Component Gap for Permanent  |
| 2026-05-09 21:52 UTC | `INCONCLUSIVE` | Cheeger Constant Exponentiates Resolution Length for Tseitin Form |
| 2026-05-09 22:03 UTC | `INCONCLUSIVE` | p-adic Valuation of Solution Count Modulo p Inversely Proportiona |
| 2026-05-09 22:15 UTC | `INCONCLUSIVE` | Slice Rank Lower Bound for Disjointness Communication Matrices |
| 2026-05-09 22:28 UTC | `INCONCLUSIVE` | Symmetric Tensor Rank Gap in Permanent vs Determinant Decompositi |
| 2026-05-09 22:50 UTC | `INCONCLUSIVE` | Standard Young Tableau Count Exponential Gap in Symmetric Power D |
| 2026-05-09 23:33 UTC | `INCONCLUSIVE` | Plethysm Multiplicity Exponential Gap in Monotone Permanent vs De |
| 2026-05-10 00:08 UTC | `INCONCLUSIVE` | Tropical Convex Hull Extreme Points Lower Bound for ACC^0 Circuit |
| 2026-05-10 00:22 UTC | `INCONCLUSIVE` | Kronecker Coefficient Exponential Gap in Symmetric Powers of Perm |
| 2026-05-10 00:30 UTC | `INCONCLUSIVE` | Operator Norm Lower Bound for Disjointness Communication Matrices |

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