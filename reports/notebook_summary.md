---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-12 01:34 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-12 01:34 UTC

- Cycles recorded: **632**
- Time span: 435.9h (~1.45 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 595 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 34 |
| Schur-Weyl Duality | 22 |
| Representation Theory of Symmetric Groups | 17 |
| Free Probability | 14 |
| Matroid Theory | 13 |
| Additive Combinatorics | 10 |
| Free Probability Theory | 9 |
| Noncommutative L^p Geometry | 8 |
| Polymatroid Theory | 8 |
| Algebraic Geometry | 7 |
| Random Matrix Theory | 7 |
| Finite Geometry | 6 |
| Spectral Graph Theory | 6 |
| Plethysm Theory | 6 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Fourier Analysis of Boolean Functions | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Noncommutative Geometry | 4 |
| Fourier analysis of boolean functions | 3 |
| Algebraic Topology | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl duality | 3 |
| Diophantine Approximation | 3 |
| Persistent Homology | 3 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-11 18:31 UTC | `INCONCLUSIVE` | Free Cumulant Sum Gap in Read-Twice BP Transition Matrices |
| 2026-05-11 19:29 UTC | `INCONCLUSIVE` | Colin de Verdière Invariant Lower Bounds Resolution Length for Ts |
| 2026-05-11 19:40 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice BPs for IP_2 |
| 2026-05-11 20:25 UTC | `INCONCLUSIVE` | Free Cumulant Sum Gap in Read-Twice BPs for IP_2 |
| 2026-05-11 20:56 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice BPs for IP_2 |
| 2026-05-11 21:18 UTC | `INCONCLUSIVE` | Tropical Convex Hull Dimension Inverse Proportional to ACC^0 Circ |
| 2026-05-11 21:40 UTC | `INCONCLUSIVE` | Symmetric Power Multiplicity Gap in Permanent vs Determinant Repr |
| 2026-05-11 21:47 UTC | `INCONCLUSIVE` | Schur-Weyl Multiplicity Gap in Permanent vs Determinant Decomposi |
| 2026-05-11 21:57 UTC | `INCONCLUSIVE` | Dual Convex Body Width Bounds SOS Degree for Max-CUT |
| 2026-05-11 22:27 UTC | `INCONCLUSIVE` | Cycle Matroid Rank Inverse Proportional to Resolution Proof Size  |
| 2026-05-11 22:59 UTC | `INCONCLUSIVE` | Cohomological Dimension Inverse Proportional to Disjointness Comm |
| 2026-05-11 23:12 UTC | `INCONCLUSIVE` | Kronecker Coefficient Gap in Set Disjointness Communication Compl |
| 2026-05-11 23:33 UTC | `INCONCLUSIVE` | Symmetric Tensor Rank Gap in Permanent vs Determinant Decompositi |
| 2026-05-12 01:18 UTC | `INCONCLUSIVE` | Free Cumulant Sum Bounded by Disjointness Communication Complexit |
| 2026-05-12 01:34 UTC | `INCONCLUSIVE` | Plethysm Coefficient Gap in Permanent vs Determinant Decompositio |

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