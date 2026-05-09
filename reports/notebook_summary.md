---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-09 10:43 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-09 10:43 UTC

- Cycles recorded: **472**
- Time span: 373.1h (~1.27 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 437 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 22 |
| Free Probability | 10 |
| Schur-Weyl Duality | 10 |
| Matroid Theory | 7 |
| Algebraic Geometry | 6 |
| Additive Combinatorics | 6 |
| Random Matrix Theory | 5 |
| Finite Geometry | 5 |
| Spectral Graph Theory | 5 |
| Polymatroid Theory | 5 |
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
| 2026-05-09 04:46 UTC | `INCONCLUSIVE` | Dehn Function Exponentiation Bounds Resolution Length for Tseitin |
| 2026-05-09 05:35 UTC | `INCONCLUSIVE` | Symmetric Power Rank Gap in Permanent vs Determinant Polynomials |
| 2026-05-09 05:41 UTC | `INCONCLUSIVE` | Real Radical Dimension Inverse Proportionality to SOS Degree for  |
| 2026-05-09 06:02 UTC | `INCONCLUSIVE` | Free Entropy Lower Bound on Disjointness Communication Complexity |
| 2026-05-09 06:15 UTC | `INCONCLUSIVE` | Fourier Coefficient Decay and Resolution Proof Length for k-CNF F |
| 2026-05-09 06:21 UTC | `INCONCLUSIVE` | Hilbert Function Leading Coefficient Distinguishes Read-Twice fro |
| 2026-05-09 06:33 UTC | `INCONCLUSIVE` | Moment Matrix Rank Inverse Proportional to SOS Degree for Max-CUT |
| 2026-05-09 08:02 UTC | `INCONCLUSIVE` | Free Entropy Gap in Read-Twice Branching Programs for IP_2 |
| 2026-05-09 08:36 UTC | `INCONCLUSIVE` | Plethysm Coefficient Gap in Symmetric Squares of Permutation Repr |
| 2026-05-09 08:50 UTC | `INCONCLUSIVE` | Fourier Min-Coefficient Inverse Proportionality to CNF Size |
| 2026-05-09 09:25 UTC | `INCONCLUSIVE` | Kronecker Coefficient Exponential Gap in Symmetric Powers of Perm |
| 2026-05-09 09:46 UTC | `INCONCLUSIVE` | Algebraic Connectivity Exponentiates DPLL Tree Size for Tseitin F |
| 2026-05-09 09:58 UTC | `INCONCLUSIVE` | Submodular Width of Polymatroid Rank Function and Monotone Circui |
| 2026-05-09 10:06 UTC | `INCONCLUSIVE` | Symmetric Group Fourier Coefficient Sum Distinguishes Read-Twice  |
| 2026-05-09 10:43 UTC | `INCONCLUSIVE` | Fourier Coefficient Sum Inverse Proportionality to DPLL Tree Size |

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