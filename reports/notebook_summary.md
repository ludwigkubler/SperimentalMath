---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-13 09:59 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-13 09:59 UTC

- Cycles recorded: **707**
- Time span: 468.3h (~1.51 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 670 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 40 |
| Schur-Weyl Duality | 27 |
| Free Probability Theory | 19 |
| Representation Theory of Symmetric Groups | 18 |
| Matroid Theory | 16 |
| Free Probability | 14 |
| Additive Combinatorics | 13 |
| Noncommutative L^p Geometry | 10 |
| Random Matrix Theory | 8 |
| Polymatroid Theory | 8 |
| Algebraic Geometry | 7 |
| Spectral Graph Theory | 7 |
| Finite Geometry | 6 |
| Plethysm Theory | 6 |
| Persistent Homology | 5 |
| Noncommutative Harmonic Analysis | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Algebraic Geometry over Finite Fields | 4 |
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

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-13 04:27 UTC | `INCONCLUSIVE` | Sum-Product Complexity Lower Bounds for ACC⁰ Circuits |
| 2026-05-13 04:40 UTC | `INCONCLUSIVE` | Free Cumulant Sum Lower Bounds Randomized Communication Complexit |
| 2026-05-13 04:58 UTC | `INCONCLUSIVE` | Toric Variety Degree Inverse to SOS Refutation Degree for 3-SAT |
| 2026-05-13 05:57 UTC | `INCONCLUSIVE` | Persistent Homology Total Persistence Inversely Proportional to R |
| 2026-05-13 06:08 UTC | `INCONCLUSIVE` | Plethysm Coefficient Sum Gap in Symmetric Powers of Permanent vs  |
| 2026-05-13 06:23 UTC | `INCONCLUSIVE` | Gröbner Basis Step Count vs. Extended Frege Proof Length for 3-SA |
| 2026-05-13 06:30 UTC | `INCONCLUSIVE` | Free Cumulant Sum Gap in Read-Twice BPs for 3-SAT |
| 2026-05-13 06:36 UTC | `INCONCLUSIVE` | Hilbert Polynomial Leading Coefficient Inversely Proportional to  |
| 2026-05-13 06:42 UTC | `INCONCLUSIVE` | Kronecker Coefficient Gap in Symmetric Powers of Permanent vs Det |
| 2026-05-13 07:16 UTC | `INCONCLUSIVE` | SOS Moment Matrix Eigenvalue Sum Bounded by Degree for Max-CUT |
| 2026-05-13 07:23 UTC | `INCONCLUSIVE` | Symmetric Group Fourier Coefficient Count Inversely Proportional  |
| 2026-05-13 08:49 UTC | `INCONCLUSIVE` | Free Cumulant Sum Lower Bounded by Communication Complexity of DI |
| 2026-05-13 09:19 UTC | `INCONCLUSIVE` | Schur-Weyl Component Count Gap in Monotone Circuit Size for Perma |
| 2026-05-13 09:31 UTC | `INCONCLUSIVE` | Algebraic Shifting Generator Count Bounds Communication Complexit |
| 2026-05-13 09:59 UTC | `INCONCLUSIVE` | Algebraic Shifting Edge Count Bounds Monotone DNF Size for k-CLIQ |

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