---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-09 16:43 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-09 16:43 UTC

- Cycles recorded: **486**
- Time span: 379.0h (~1.28 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 451 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 25 |
| Free Probability | 11 |
| Schur-Weyl Duality | 10 |
| Matroid Theory | 9 |
| Algebraic Geometry | 7 |
| Additive Combinatorics | 6 |
| Polymatroid Theory | 6 |
| Random Matrix Theory | 5 |
| Finite Geometry | 5 |
| Spectral Graph Theory | 5 |
| Representation Theory of Symmetric Groups | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Plethysm Theory | 4 |
| Fourier analysis of boolean functions | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Fourier Analysis on Boolean Functions | 3 |
| Schur-Weyl duality | 3 |
| Persistent Homology | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Schur-Weyl duality, plethysm, algebraic combinatorics | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-09 10:43 UTC | `INCONCLUSIVE` | Fourier Coefficient Sum Inverse Proportionality to DPLL Tree Size |
| 2026-05-09 11:18 UTC | `INCONCLUSIVE` | Positive Eigenvalue Count Inverse Proportional to SOS Refutation  |
| 2026-05-09 11:32 UTC | `INCONCLUSIVE` | Matroid Rank Gap in Monotone DNF for k-CLIQUE |
| 2026-05-09 11:59 UTC | `INCONCLUSIVE` | Hilbert Leading Coefficient Inverse Proportional to ABP Size |
| 2026-05-09 12:07 UTC | `INCONCLUSIVE` | Resultant Degree Exponential Lower Bound for ACC^0 Circuit Size |
| 2026-05-09 12:44 UTC | `INCONCLUSIVE` | Semialgebraic Dimension Inverse Proportional to SOS Degree for Ma |
| 2026-05-09 13:00 UTC | `INCONCLUSIVE` | Polymatroid Rank and SOS Refutation Degree for Monotone k-CLIQUE |
| 2026-05-09 13:27 UTC | `INCONCLUSIVE` | Matroid Rank Submodularity Bounds Monotone DNF Size |
| 2026-05-09 13:33 UTC | `INCONCLUSIVE` | Operator Norm Separation for Read-Twice vs Read-Once BPs |
| 2026-05-09 13:46 UTC | `INCONCLUSIVE` | Convex Body Volume Lower Bounds Disjointness Communication Comple |
| 2026-05-09 14:30 UTC | `INCONCLUSIVE` | Free Entropy Lower Bound on Disjointness Communication Complexity |
| 2026-05-09 15:27 UTC | `INCONCLUSIVE` | Kronecker Coefficient Exponential Gap in Symmetric Powers of Perm |
| 2026-05-09 16:11 UTC | `INCONCLUSIVE` | Noncommutative Fourier Norm Inverse Proportional to Disjointness  |
| 2026-05-09 16:25 UTC | `INCONCLUSIVE` | Moment Matrix Sparsity Lower Bound for Max-CUT SOS Approximation |
| 2026-05-09 16:43 UTC | `INCONCLUSIVE` | Hypergraph Treewidth Inverse Proportional to DPLL Tree Size for R |

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