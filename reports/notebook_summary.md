---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-09 21:30 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-09 21:30 UTC

- Cycles recorded: **504**
- Time span: 383.8h (~1.31 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 469 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 25 |
| Free Probability | 12 |
| Schur-Weyl Duality | 11 |
| Matroid Theory | 9 |
| Representation Theory of Symmetric Groups | 8 |
| Algebraic Geometry | 7 |
| Random Matrix Theory | 6 |
| Additive Combinatorics | 6 |
| Polymatroid Theory | 6 |
| Finite Geometry | 5 |
| Spectral Graph Theory | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Plethysm Theory | 4 |
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
| 2026-05-09 17:37 UTC | `INCONCLUSIVE` | Fourier Coefficient Sum Submodularity for Monotone DNF |
| 2026-05-09 17:48 UTC | `INCONCLUSIVE` | Metric Dispersion Lower Bound for Monotone DNF Depth |
| 2026-05-09 18:13 UTC | `INCONCLUSIVE` | Gowers Uniformity Norm Gap in Read-Twice vs Read-Once BPs |
| 2026-05-09 18:20 UTC | `INCONCLUSIVE` | Littlewood-Richardson Coefficient Asymmetry in Permanent vs Deter |
| 2026-05-09 18:32 UTC | `INCONCLUSIVE` | Genus Inverse Proportionality to Disjointness Communication Compl |
| 2026-05-09 18:58 UTC | `INCONCLUSIVE` | Free Entropy Lower Bound on Disjointness Communication Complexity |
| 2026-05-09 19:24 UTC | `INCONCLUSIVE` | Symmetric Group Irreducible Component Exponential Gap in Permanen |
| 2026-05-09 19:47 UTC | `INCONCLUSIVE` | Quadratic Form Rank Inverse Proportional to SOS Refutation Degree |
| 2026-05-09 19:56 UTC | `INCONCLUSIVE` | Algebraic Circuit Complexity via Monodromy Action on Tseitin Form |
| 2026-05-09 20:05 UTC | `INCONCLUSIVE` | Newton Polytope Vertex Count Inverse Proportional to SOS Degree f |
| 2026-05-09 20:11 UTC | `INCONCLUSIVE` | Real Stable Polynomial Degree Lower Bound for Max-CUT SOS |
| 2026-05-09 20:27 UTC | `INCONCLUSIVE` | Young Tableau Count Inverse Proportional to Monotone Circuit Size |
| 2026-05-09 21:07 UTC | `INCONCLUSIVE` | Real Root Count Inverse Proportional to SOS Degree for Max-CUT |
| 2026-05-09 21:15 UTC | `INCONCLUSIVE` | Betti Number Inverse Proportionality to DPLL Tree Size in 3-SAT |
| 2026-05-09 21:30 UTC | `INCONCLUSIVE` | Schur-Weyl Decomposition Irreducible Component Gap for Permanent  |

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