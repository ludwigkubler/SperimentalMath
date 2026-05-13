---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-13 04:58 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-13 04:58 UTC

- Cycles recorded: **695**
- Time span: 463.3h (~1.50 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 658 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 39 |
| Schur-Weyl Duality | 26 |
| Free Probability Theory | 17 |
| Representation Theory of Symmetric Groups | 17 |
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
| Noncommutative Harmonic Analysis | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Algebraic Geometry over Finite Fields | 4 |
| Fourier Analysis of Boolean Functions | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| Persistent Homology | 4 |
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
| 2026-05-12 23:21 UTC | `INCONCLUSIVE` | Irreducible Component Count Inversely Proportional to ACC⁰ Circui |
| 2026-05-12 23:54 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice BPs for 3-SAT |
| 2026-05-13 00:19 UTC | `INCONCLUSIVE` | Real Radical Dimension Inverse Proportional to SOS Degree for Max |
| 2026-05-13 00:30 UTC | `INCONCLUSIVE` | Real Variety Connected Components Lower Bound SOS Degree for Max- |
| 2026-05-13 00:43 UTC | `INCONCLUSIVE` | Plethysm Coefficient Gap in Symmetric Powers of Permanent vs Dete |
| 2026-05-13 01:20 UTC | `INCONCLUSIVE` | Negative Eigenvalue Count in SOS Moment Matrix Bounded by Log-Siz |
| 2026-05-13 01:46 UTC | `INCONCLUSIVE` | Free Cumulant Norm Gap in Read-Twice BPs for IP_2 |
| 2026-05-13 02:16 UTC | `INCONCLUSIVE` | Secant Variety Dimension Bounds Disjointness Communication Rank |
| 2026-05-13 02:43 UTC | `INCONCLUSIVE` | Free Cumulant Spread Bounds Disjointness Communication Complexity |
| 2026-05-13 03:13 UTC | `INCONCLUSIVE` | Schur-Weyl Decomposition Term Count vs. Monotone Circuit Size for |
| 2026-05-13 03:38 UTC | `INCONCLUSIVE` | Free Cumulant Sum Inversely Proportional to Disjointness Communic |
| 2026-05-13 04:06 UTC | `INCONCLUSIVE` | Free Cumulant Spread Bounds Disjointness Communication Complexity |
| 2026-05-13 04:27 UTC | `INCONCLUSIVE` | Sum-Product Complexity Lower Bounds for ACC⁰ Circuits |
| 2026-05-13 04:40 UTC | `INCONCLUSIVE` | Free Cumulant Sum Lower Bounds Randomized Communication Complexit |
| 2026-05-13 04:58 UTC | `INCONCLUSIVE` | Toric Variety Degree Inverse to SOS Refutation Degree for 3-SAT |

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