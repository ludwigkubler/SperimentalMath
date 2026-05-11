---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-11 01:40 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-11 01:40 UTC

- Cycles recorded: **579**
- Time span: 412.0h (~1.41 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 542 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 31 |
| Representation Theory of Symmetric Groups | 17 |
| Schur-Weyl Duality | 15 |
| Free Probability | 14 |
| Matroid Theory | 11 |
| Additive Combinatorics | 10 |
| Polymatroid Theory | 8 |
| Algebraic Geometry | 7 |
| Random Matrix Theory | 7 |
| Finite Geometry | 6 |
| Noncommutative L^p Geometry | 6 |
| Spectral Graph Theory | 6 |
| Plethysm Theory | 6 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Fourier Analysis of Boolean Functions | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Fourier analysis of boolean functions | 3 |
| Algebraic Topology | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl duality | 3 |
| Diophantine Approximation | 3 |
| Persistent Homology | 3 |
| Noncommutative Geometry | 3 |
| Noncommutative Harmonic Analysis | 3 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-10 21:20 UTC | `INCONCLUSIVE` | Polymatroid Rank Lower Bound for Monotone k-CLIQUE |
| 2026-05-10 21:50 UTC | `INCONCLUSIVE` | Coxeter Polynomial Root Count Inverse Proportional to Resolution  |
| 2026-05-10 21:59 UTC | `INCONCLUSIVE` | Spectral Concentration of Moment Matrices in Max-CUT SOS Hierarch |
| 2026-05-10 22:09 UTC | `INCONCLUSIVE` | Noncommutative Fourier Coefficient Gap in Read-Twice BPs for IP_2 |
| 2026-05-10 22:42 UTC | `INCONCLUSIVE` | Additive Energy Inverse Proportional to Disjointness Discrepancy |
| 2026-05-10 23:07 UTC | `INCONCLUSIVE` | Moment-Matrix Spectral Norm Inverse Proportional to Communication |
| 2026-05-10 23:56 UTC | `INCONCLUSIVE` | Schur-Weyl Decomposition Entropy Gap for Permanent vs Determinant |
| 2026-05-11 00:01 UTC | `INCONCLUSIVE` | Homotopy Group Rank Inverse Proportional to Disjointness Communic |
| 2026-05-11 00:27 UTC | `INCONCLUSIVE` | Diophantine Approximation Error Inversely Proportional to Communi |
| 2026-05-11 00:37 UTC | `INCONCLUSIVE` | Hypergraph Matching Complexity for Monotone DNF |
| 2026-05-11 00:43 UTC | `INCONCLUSIVE` | Additive Energy Threshold for ACC⁰ Circuit Size in CNF Formulas |
| 2026-05-11 00:50 UTC | `INCONCLUSIVE` | SOS Refutation Size Bounded by Curve Genus of CSP Constraints |
| 2026-05-11 01:05 UTC | `INCONCLUSIVE` | Tutte Polynomial Evaluation Bounded by Monotone k-CLIQUE Circuit  |
| 2026-05-11 01:20 UTC | `INCONCLUSIVE` | Young Tableau Count Exponential Gap in Disjointness Communication |
| 2026-05-11 01:40 UTC | `INCONCLUSIVE` | Fourier Coefficient Sum Inverse Proportional to Disjointness Disc |

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