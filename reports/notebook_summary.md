---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 22:24 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 22:24 UTC

- Cycles recorded: **436**
- Time span: 360.7h (~1.21 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 401 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 18 |
| Matroid Theory | 7 |
| Free Probability | 7 |
| Additive Combinatorics | 6 |
| Schur-Weyl Duality | 6 |
| Algebraic Geometry | 5 |
| Finite Geometry | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Random Matrix Theory | 4 |
| Polymatroid Theory | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Fourier analysis of boolean functions | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl duality | 3 |
| Spectral Graph Theory | 3 |
| Persistent Homology | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Schur-Weyl duality, plethysm, algebraic combinatorics | 2 |
| Free Probability Theory | 2 |
| Tropical Circuit Weight Analysis (TCWA) — Bounded Arithmetic | 2 |
| Bounded Arithmetic | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-08 19:22 UTC | `INCONCLUSIVE` | Quandle Isomorphism Complexity and ACC^0 Circuit Depth |
| 2026-05-08 19:28 UTC | `INCONCLUSIVE` | Schur-Weyl Decomposition Rank Lower Bounds Disjointness Communica |
| 2026-05-08 19:41 UTC | `INCONCLUSIVE` | Persistent Homology Barcode Length Inversely Proportional to DPLL |
| 2026-05-08 20:09 UTC | `INCONCLUSIVE` | Additive Energy Threshold Exceeds ACC⁰ Circuit Size |
| 2026-05-08 20:19 UTC | `INCONCLUSIVE` | Zarankiewicz-Free Communication Matrices Imply Monotone Circuit L |
| 2026-05-08 20:40 UTC | `INCONCLUSIVE` | Kronecker Coefficient Growth Separates Permanent vs Determinant |
| 2026-05-08 20:58 UTC | `INCONCLUSIVE` | Real Radical Dimension and SOS Degree for Max-CUT |
| 2026-05-08 21:07 UTC | `INCONCLUSIVE` | Permutation Polynomial Width Conjecture |
| 2026-05-08 21:14 UTC | `INCONCLUSIVE` | Plethysm Coefficient Gap in Symmetric Powers of Permanent vs Dete |
| 2026-05-08 21:20 UTC | `INCONCLUSIVE` | Cluster Algebra Mutation Distance Bounds ACC^0 Circuit Size |
| 2026-05-08 21:37 UTC | `INCONCLUSIVE` | Moment Matrix Eigenvalue Decay and SOS Degree for Max-CUT |
| 2026-05-08 21:44 UTC | `INCONCLUSIVE` | Matroid Representation Complexity of Monotone DNF for k-CLIQUE |
| 2026-05-08 22:01 UTC | `INCONCLUSIVE` | Plethysm Coefficient Exponential Gap in Symmetric Squares of Perm |
| 2026-05-08 22:16 UTC | `INCONCLUSIVE` | Symmetric Group Multiplicity Sum Lower Bound for Disjointness Com |
| 2026-05-08 22:24 UTC | `INCONCLUSIVE` | Polymatroid Rank Deficit in Monotone DNF for k-CLIQUE |

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