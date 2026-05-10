---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-10 05:06 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-10 05:06 UTC

- Cycles recorded: **524**
- Time span: 391.4h (~1.34 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 489 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 27 |
| Free Probability | 12 |
| Schur-Weyl Duality | 12 |
| Representation Theory of Symmetric Groups | 11 |
| Matroid Theory | 10 |
| Algebraic Geometry | 7 |
| Random Matrix Theory | 6 |
| Additive Combinatorics | 6 |
| Finite Geometry | 6 |
| Spectral Graph Theory | 6 |
| Polymatroid Theory | 6 |
| Plethysm Theory | 6 |
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
| Noncommutative Geometry | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Tropical geometry | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-09 23:33 UTC | `INCONCLUSIVE` | Plethysm Multiplicity Exponential Gap in Monotone Permanent vs De |
| 2026-05-10 00:08 UTC | `INCONCLUSIVE` | Tropical Convex Hull Extreme Points Lower Bound for ACC^0 Circuit |
| 2026-05-10 00:22 UTC | `INCONCLUSIVE` | Kronecker Coefficient Exponential Gap in Symmetric Powers of Perm |
| 2026-05-10 00:30 UTC | `INCONCLUSIVE` | Operator Norm Lower Bound for Disjointness Communication Matrices |
| 2026-05-10 00:53 UTC | `INCONCLUSIVE` | Tensor Rank Exponential Gap in Read-Twice vs Read-Once Branching  |
| 2026-05-10 01:02 UTC | `INCONCLUSIVE` | Projective Plane Line Count Bounds ABP Width for Monotone Circuit |
| 2026-05-10 01:08 UTC | `INCONCLUSIVE` | Quantum Rank Lower Bounds for Disjointness Communication Matrices |
| 2026-05-10 01:23 UTC | `INCONCLUSIVE` | Symmetric Tensor Rank Gap in Permanent vs Determinant Decompositi |
| 2026-05-10 01:47 UTC | `INCONCLUSIVE` | Negative Eigenvalue Count Lower Bounds SOS Degree for Max-CUT |
| 2026-05-10 03:39 UTC | `INCONCLUSIVE` | Plethysm Coefficient Gap in Homogeneous Polynomial Decompositions |
| 2026-05-10 03:58 UTC | `INCONCLUSIVE` | Hypergraph Maximum Matching Inverse Proportional to ACC^0 Circuit |
| 2026-05-10 04:08 UTC | `INCONCLUSIVE` | Finite Field Rank and Branching Program Width for Boolean Functio |
| 2026-05-10 04:25 UTC | `INCONCLUSIVE` | Matroid Rank Inverse Proportional to ACC^0 Circuit Size for GF(2) |
| 2026-05-10 04:55 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower Bounds Disjointness Communication  |
| 2026-05-10 05:06 UTC | `INCONCLUSIVE` | Real Critical Point Count Exponential in SOS Degree for Max-CUT |

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