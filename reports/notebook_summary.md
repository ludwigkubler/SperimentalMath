---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-21 08:33 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-21 08:33 UTC

- Cycles recorded: **1001**
- Time span: 658.9h (~1.52 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 955 |
| BARRIER_HIT | 26 |
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
| 2026-05-21 03:30 UTC | `INCONCLUSIVE` | Laplacian Eigenvalue and Resolution Length of Tseitin Formulas |
| 2026-05-21 03:38 UTC | `INCONCLUSIVE` | Moment Matrix Spectral Gap and SOS Degree for Max-CUT |
| 2026-05-21 03:52 UTC | `INCONCLUSIVE` | Free Entropy Gap in Read-Twice BP Transition Matrices |
| 2026-05-21 04:29 UTC | `INCONCLUSIVE` | Matroid Rank Gap in Monotone DNF for k-CLIQUE |
| 2026-05-21 04:56 UTC | `INCONCLUSIVE` | Algebraic Shifting Facet Count Bounds Tseitin Resolution Length |
| 2026-05-21 05:31 UTC | `INCONCLUSIVE` | Symmetric Group Orbit Count Distinguishes Read-Twice BPs |
| 2026-05-21 05:41 UTC | `INCONCLUSIVE` | Polynomial Threshold Function Degree Bounds Karchmer-Wigderson Pr |
| 2026-05-21 06:02 UTC | `INCONCLUSIVE` | Fourier Coefficient Sum Bounds Monotone DNF Size for k-CLIQUE |
| 2026-05-21 06:31 UTC | `INCONCLUSIVE` | Real Radical Dimension Bounds AC⁰ Circuit Size for PARITY |
| 2026-05-21 06:56 UTC | `INCONCLUSIVE` | Eigenvalue Count and SOS Degree for Max-CUT Approximation |
| 2026-05-21 07:37 UTC | `INCONCLUSIVE` | Prime Density in Arithmetic Progressions and Seed Length of Nisan |
| 2026-05-21 07:51 UTC | `INCONCLUSIVE` | Free Entropy Gap in Disjointness Communication Matrices |
| 2026-05-21 08:09 UTC | `INCONCLUSIVE` | SOS Moment Matrix Spectral Gap and Max-CUT Approximation Ratio |
| 2026-05-21 08:19 UTC | `INCONCLUSIVE` | Additive Energy of Fourier Coefficients and ACC⁰ Circuit Size |
| 2026-05-21 08:33 UTC | `INCONCLUSIVE` | Betti Number Sum Lower Bound for SOS Max-CUT Degree |

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