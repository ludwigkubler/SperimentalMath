---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-13 00:43 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-13 00:43 UTC

- Cycles recorded: **685**
- Time span: 459.0h (~1.49 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 648 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 39 |
| Schur-Weyl Duality | 25 |
| Representation Theory of Symmetric Groups | 17 |
| Matroid Theory | 16 |
| Free Probability | 14 |
| Additive Combinatorics | 12 |
| Free Probability Theory | 12 |
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
| 2026-05-12 18:22 UTC | `INCONCLUSIVE` | Submodular Rank Gap in Monotone DNF for k-CLIQUE |
| 2026-05-12 19:26 UTC | `INCONCLUSIVE` | Euler Characteristic of Communication Graph Equals Deterministic  |
| 2026-05-12 19:34 UTC | `INCONCLUSIVE` | Completely Bounded Norm Gap in Read-Twice BPs for IP_2 |
| 2026-05-12 19:42 UTC | `INCONCLUSIVE` | Non-Abelian Fourier Coefficient Spread Inversely Proportional to  |
| 2026-05-12 20:10 UTC | `INCONCLUSIVE` | Secant Rank of Disjointness Communication Matrix Lower-Bounds Ran |
| 2026-05-12 20:40 UTC | `INCONCLUSIVE` | Schur Coefficient Sum Ratio in Symmetric Powers of Permanent vs D |
| 2026-05-12 21:10 UTC | `INCONCLUSIVE` | Hook-Length Ratio Bounds Monotone Circuit Size for Permanent |
| 2026-05-12 22:03 UTC | `INCONCLUSIVE` | Irreducible Component Count Inversely Proportional to SOS Refutat |
| 2026-05-12 22:47 UTC | `INCONCLUSIVE` | Gowers Norm Inverse Proportional to ACC⁰ Circuit Size for Explici |
| 2026-05-12 22:54 UTC | `INCONCLUSIVE` | Irreducible Component Count of IP_2 BP Variety Bounds Read-Twice  |
| 2026-05-12 23:21 UTC | `INCONCLUSIVE` | Irreducible Component Count Inversely Proportional to ACC⁰ Circui |
| 2026-05-12 23:54 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice BPs for 3-SAT |
| 2026-05-13 00:19 UTC | `INCONCLUSIVE` | Real Radical Dimension Inverse Proportional to SOS Degree for Max |
| 2026-05-13 00:30 UTC | `INCONCLUSIVE` | Real Variety Connected Components Lower Bound SOS Degree for Max- |
| 2026-05-13 00:43 UTC | `INCONCLUSIVE` | Plethysm Coefficient Gap in Symmetric Powers of Permanent vs Dete |

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