---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-21 12:07 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-21 12:07 UTC

- Cycles recorded: **1020**
- Time span: 662.4h (~1.54 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 973 |
| BARRIER_HIT | 27 |
| FALSIFIED | 16 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 59 |
| Schur-Weyl Duality | 36 |
| Free Probability | 26 |
| Representation Theory of Symmetric Groups | 24 |
| Matroid Theory | 23 |
| Free Probability Theory | 19 |
| Additive Combinatorics | 15 |
| Noncommutative L^p Geometry | 12 |
| Random Matrix Theory | 11 |
| Spectral Graph Theory | 11 |
| Noncommutative Harmonic Analysis | 10 |
| Polymatroid Theory | 9 |
| REAL_ALGEBRAIC_GEOMETRY | 9 |
| Algebraic Geometry | 8 |
| Persistent Homology | 8 |
| Algebraic Topology | 7 |
| Finite Geometry | 6 |
| Schur-Weyl duality | 6 |
| Plethysm Theory | 6 |
| Invariant Theory | 6 |
| Fourier Analysis on Boolean Functions | 5 |
| Additive combinatorics | 5 |
| Algebraic Geometry of Secant Varieties | 5 |
| FOURIER_ANALYSIS | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Algebraic Geometry over Finite Fields | 4 |
| Fourier Analysis of Boolean Functions | 4 |
| Non-Abelian Harmonic Analysis | 4 |
| COMMUNICATION_COMPLEXITY | 4 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-21 09:59 UTC | `INCONCLUSIVE` | Discrete Morse Number of Rejection Complex Bounds ACC^0[m] Size |
| 2026-05-21 10:06 UTC | `INCONCLUSIVE` | Trace-Norm Capacity Conjecture for Read-Twice BP Communication Ma |
| 2026-05-21 10:14 UTC | `INCONCLUSIVE` | Slice-Fourier Variance Asymmetry of Perm vs Monotone Det Substitu |
| 2026-05-21 10:22 UTC | `INCONCLUSIVE` | VC dimension of gadget row family tightly bounds lifted D^cc |
| 2026-05-21 10:32 UTC | `INCONCLUSIVE` | Gromov 4-Point Hyperbolicity Gap Separates k-CLIQUE Monotone DNFs |
| 2026-05-21 10:48 UTC | `INCONCLUSIVE` | Lorentzian Hessian Gap of Spanning-Tree Polynomial Bounds Max-CUT |
| 2026-05-21 10:54 UTC | `INCONCLUSIVE` | NW-Design Slice Spectral Discrepancy Bound for DISJ |
| 2026-05-21 11:03 UTC | `INCONCLUSIVE` | MST Persistence Entropy Lower-Bounds Log-Rank of Sign Matrices |
| 2026-05-21 11:12 UTC | `INCONCLUSIVE` | Instance-Complexity Certification Depth Bounds Monotone DNF Size  |
| 2026-05-21 11:23 UTC | `INCONCLUSIVE` | Cyclic Fourier Spread of Term-Vertex Incidence in Monotone k-CLIQ |
| 2026-05-21 11:29 UTC | `INCONCLUSIVE` | Coboundary Spectral Gap Lower-Bounds DPLL Tree Size on Tseitin |
| 2026-05-21 11:40 UTC | `INCONCLUSIVE` | Heilmann-Lieb Matching Root Gap Bounds Monotone k-CLIQUE DNF Size |
| 2026-05-21 11:54 UTC | `INCONCLUSIVE` | Fourier L1 Norm Cubed-Polynomial Bound for Read-Twice BPs |
| 2026-05-21 12:01 UTC | `INCONCLUSIVE` | Apolar Catalecticant Defect Bounds DISJ Randomized Communication |
| 2026-05-21 12:07 UTC | `BARRIER_HIT` | A_5 Barrington-Hash Equidistribution Gap for DISJ |

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