---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-12 14:35 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-12 14:35 UTC

- Cycles recorded: **661**
- Time span: 448.9h (~1.47 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 624 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 36 |
| Schur-Weyl Duality | 23 |
| Representation Theory of Symmetric Groups | 17 |
| Matroid Theory | 16 |
| Free Probability | 14 |
| Additive Combinatorics | 10 |
| Free Probability Theory | 10 |
| Noncommutative L^p Geometry | 9 |
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
| 2026-05-12 07:54 UTC | `INCONCLUSIVE` | Matroid Rank Submodularity in Monotone DNF for k-CLIQUE |
| 2026-05-12 08:01 UTC | `INCONCLUSIVE` | Tensor Product Multiplicity Inverse Proportional to Monotone Circ |
| 2026-05-12 08:14 UTC | `INCONCLUSIVE` | Persistent Homology of Read-Twice BPs Bounded by Log-Size |
| 2026-05-12 08:22 UTC | `INCONCLUSIVE` | Hilbert Function Growth Inversely Proportional to Extended Frege  |
| 2026-05-12 08:32 UTC | `INCONCLUSIVE` | Block Design Discrepancy and Communication Complexity Lower Bound |
| 2026-05-12 08:44 UTC | `INCONCLUSIVE` | Second Eigenvalue Inverse Proportional to Resolution Proof Length |
| 2026-05-12 09:26 UTC | `INCONCLUSIVE` | Real Radical Dimension Bounds SOS Degree for Max-CUT |
| 2026-05-12 10:22 UTC | `INCONCLUSIVE` | Noncommutative Fourier Coefficient Sum Inversely Proportional to  |
| 2026-05-12 10:30 UTC | `INCONCLUSIVE` | SOS Degree Lower Bound via Eigenvalue Count in Moment Matrix |
| 2026-05-12 11:18 UTC | `INCONCLUSIVE` | Kronecker Coefficient Gap in Symmetric Decompositions of Permanen |
| 2026-05-12 11:48 UTC | `INCONCLUSIVE` | Schur-Weyl Decomposition Component Count vs. Monotone Circuit Siz |
| 2026-05-12 12:40 UTC | `INCONCLUSIVE` | Real Radical Degree Lower Bound for AC⁰ Circuits Computing PARITY |
| 2026-05-12 13:19 UTC | `INCONCLUSIVE` | Noncommutative Fourier Coefficient Spread and Read-Twice BP Size |
| 2026-05-12 13:27 UTC | `INCONCLUSIVE` | Invariant Ring Generator Count Gap in Read-Twice BPs for IP_2 |
| 2026-05-12 14:34 UTC | `INCONCLUSIVE` | Noncommutative Fourier Coefficient Sum Bounded by Log-Size for Re |

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