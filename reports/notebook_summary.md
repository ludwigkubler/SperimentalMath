---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-19 01:40 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-19 01:40 UTC

- Cycles recorded: **807**
- Time span: 604.0h (~1.34 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 767 |
| BARRIER_HIT | 20 |
| FALSIFIED | 16 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 40 |
| Schur-Weyl Duality | 28 |
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
| 2026-05-18 22:41 UTC | `INCONCLUSIVE` | FCA Antichain Width of Implicant Lattice Caps DNF-MCSP Within Fac |
| 2026-05-18 22:48 UTC | `INCONCLUSIVE` | Schatten Stable Rank of Layer-Difference Stack Lower-Bounds RT-BP |
| 2026-05-18 22:57 UTC | `INCONCLUSIVE` | Matousek Det-LB Submatrix Dispersion Lower-Bounds Friedman Sign R |
| 2026-05-18 23:14 UTC | `INCONCLUSIVE` | Treewidth of Prime-Implicant Compatibility Graph Tracks DNF-MCSP |
| 2026-05-18 23:25 UTC | `INCONCLUSIVE` | Kashin L1-Flatness of Top Laplacian Eigenvector Bounds Max-Cut So |
| 2026-05-18 23:39 UTC | `INCONCLUSIVE` | Free 4-Cumulant Excess Capped by Stable Rank Lower-Bounds R(DISJ) |
| 2026-05-19 00:11 UTC | `INCONCLUSIVE` | Decision Tree Depth and Communication Complexity via Lifting |
| 2026-05-19 00:24 UTC | `INCONCLUSIVE` | Laplacian Apolar Rank Caps Delorme-Poljak Max-CUT SoS-2 Gap |
| 2026-05-19 00:32 UTC | `INCONCLUSIVE` | Cross-Read Kronecker Sum Rank Lower-Bounds Read-Twice BP for IP_2 |
| 2026-05-19 00:39 UTC | `INCONCLUSIVE` | SoS Cone-Gram Stable Rank Caps AC⁰ Depth-d Size for PARITY |
| 2026-05-19 00:46 UTC | `INCONCLUSIVE` | Talagrand L1 Influence Spread of Clause-Falsification Polynomial  |
| 2026-05-19 01:09 UTC | `INCONCLUSIVE` | Border Rank Lower Bound for Communication Complexity of Disjointn |
| 2026-05-19 01:23 UTC | `INCONCLUSIVE` | Communication Complexity Lower Bound for Disjointness Implies Mon |
| 2026-05-19 01:33 UTC | `INCONCLUSIVE` | Cubical First-Betti Linearly Lower-Bounds DNF-MCSP |
| 2026-05-19 01:40 UTC | `INCONCLUSIVE` | Fourier Spectral Entropy of Clause-Falsification Polynomial Bound |

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