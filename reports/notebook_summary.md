---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-12 19:42 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-12 19:42 UTC

- Cycles recorded: **674**
- Time span: 454.0h (~1.48 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 637 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 37 |
| Schur-Weyl Duality | 24 |
| Representation Theory of Symmetric Groups | 17 |
| Matroid Theory | 16 |
| Free Probability | 14 |
| Additive Combinatorics | 11 |
| Free Probability Theory | 11 |
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
| Schur-Weyl duality | 3 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-12 13:27 UTC | `INCONCLUSIVE` | Invariant Ring Generator Count Gap in Read-Twice BPs for IP_2 |
| 2026-05-12 14:34 UTC | `INCONCLUSIVE` | Noncommutative Fourier Coefficient Sum Bounded by Log-Size for Re |
| 2026-05-12 15:07 UTC | `INCONCLUSIVE` | Schur-Weyl Multiplicity Gap in Symmetric Powers of Permanent vs D |
| 2026-05-12 15:52 UTC | `INCONCLUSIVE` | Additive Energy of Truth Table Bounds ACC⁰ Circuit Size for Expli |
| 2026-05-12 16:08 UTC | `INCONCLUSIVE` | Plethysm Multiplicity Inverse Proportional to Monotone Circuit Si |
| 2026-05-12 16:21 UTC | `INCONCLUSIVE` | Ehrhart Polynomial Coefficient Sum Bounded by Resolution Proof Si |
| 2026-05-12 17:13 UTC | `INCONCLUSIVE` | Noncommutative L^∞ Norm Lower Bounds Disjointness Communication C |
| 2026-05-12 17:24 UTC | `INCONCLUSIVE` | Quasigroup Idempotent Density Inversely Proportional to ACC⁰ Circ |
| 2026-05-12 17:37 UTC | `INCONCLUSIVE` | Free Cumulant Sum Gap in Read-Twice BPs for IP_2 |
| 2026-05-12 17:56 UTC | `INCONCLUSIVE` | Tropical Variety Dimension Gap in Read-Twice vs Read-Once BPs |
| 2026-05-12 18:08 UTC | `INCONCLUSIVE` | Real Rank of SOS Moment Matrices for Max-CUT Bounded by Degree |
| 2026-05-12 18:22 UTC | `INCONCLUSIVE` | Submodular Rank Gap in Monotone DNF for k-CLIQUE |
| 2026-05-12 19:26 UTC | `INCONCLUSIVE` | Euler Characteristic of Communication Graph Equals Deterministic  |
| 2026-05-12 19:34 UTC | `INCONCLUSIVE` | Completely Bounded Norm Gap in Read-Twice BPs for IP_2 |
| 2026-05-12 19:42 UTC | `INCONCLUSIVE` | Non-Abelian Fourier Coefficient Spread Inversely Proportional to  |

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