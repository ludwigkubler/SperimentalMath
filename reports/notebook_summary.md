---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-10 19:08 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-10 19:08 UTC

- Cycles recorded: **559**
- Time span: 405.5h (~1.38 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 522 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 30 |
| Representation Theory of Symmetric Groups | 17 |
| Free Probability | 14 |
| Schur-Weyl Duality | 14 |
| Matroid Theory | 11 |
| Additive Combinatorics | 8 |
| Algebraic Geometry | 7 |
| Polymatroid Theory | 7 |
| Random Matrix Theory | 6 |
| Finite Geometry | 6 |
| Noncommutative L^p Geometry | 6 |
| Spectral Graph Theory | 6 |
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
| Fourier Analysis of Boolean Functions | 3 |
| Persistent Homology | 3 |
| Noncommutative Geometry | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-10 12:38 UTC | `INCONCLUSIVE` | Schur-Weyl Duality Invariant for Permanent vs Determinant Circuit |
| 2026-05-10 12:46 UTC | `INCONCLUSIVE` | Schur-Weyl Dimension Gap in 3-CNF Permanent vs Determinant Shapes |
| 2026-05-10 13:07 UTC | `INCONCLUSIVE` | Noncommutative L^p Norm Lower Bound for Disjointness Communicatio |
| 2026-05-10 13:12 UTC | `BARRIER_HIT` | Schur Coefficient Gap in Permanent vs Determinant Decompositions |
| 2026-05-10 14:15 UTC | `INCONCLUSIVE` | Secant Variety Dimension Gap in Determinant vs Permanent Orbits f |
| 2026-05-10 14:31 UTC | `INCONCLUSIVE` | Fourier Coefficient Discrepancy and ACC⁰ Circuit Size |
| 2026-05-10 14:39 UTC | `INCONCLUSIVE` | Fourier Coefficient Concentration and ACC⁰ Circuit Size |
| 2026-05-10 14:54 UTC | `INCONCLUSIVE` | Moment Matrix Rank Lower Bound for Max-CUT SOS Approximation |
| 2026-05-10 15:10 UTC | `INCONCLUSIVE` | Kronecker Coefficient Non-Zero Threshold for Permanent-Complete S |
| 2026-05-10 16:28 UTC | `INCONCLUSIVE` | SOS Degree Lower Bound via Matroid Polytope Dimension |
| 2026-05-10 16:34 UTC | `BARRIER_HIT` | Schur Coefficient Exponential Gap in 3-CNF Permanent vs Determina |
| 2026-05-10 17:22 UTC | `INCONCLUSIVE` | Symmetric Group Fourier Coefficient Gap in Disjointness Communica |
| 2026-05-10 17:37 UTC | `INCONCLUSIVE` | Harmonic Coefficient Sum Lower Bound for Resolution Proof Length |
| 2026-05-10 18:03 UTC | `INCONCLUSIVE` | Noncommutative L^p Norm Lower Bounds for Disjointness Communicati |
| 2026-05-10 19:08 UTC | `INCONCLUSIVE` | Cheeger Constant Exponentiates Resolution Length for Tseitin Form |

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