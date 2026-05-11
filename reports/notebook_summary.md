---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-11 12:26 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-11 12:26 UTC

- Cycles recorded: **600**
- Time span: 422.8h (~1.42 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 563 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 33 |
| Representation Theory of Symmetric Groups | 17 |
| Schur-Weyl Duality | 16 |
| Free Probability | 14 |
| Matroid Theory | 12 |
| Additive Combinatorics | 10 |
| Polymatroid Theory | 8 |
| Algebraic Geometry | 7 |
| Random Matrix Theory | 7 |
| Noncommutative L^p Geometry | 7 |
| Finite Geometry | 6 |
| Spectral Graph Theory | 6 |
| Plethysm Theory | 6 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Fourier Analysis of Boolean Functions | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Noncommutative Geometry | 4 |
| Fourier analysis of boolean functions | 3 |
| Algebraic Topology | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| Free Probability Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl duality | 3 |
| Diophantine Approximation | 3 |
| Persistent Homology | 3 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-11 04:50 UTC | `INCONCLUSIVE` | Free Entropy Gap in Read-Twice BP Transition Matrices |
| 2026-05-11 05:05 UTC | `INCONCLUSIVE` | Fundamental Group Rank Inverse Proportional to Resolution Proof S |
| 2026-05-11 05:26 UTC | `INCONCLUSIVE` | Real Rank of Moment Matrix for Random Max-CUT Instances is Linear |
| 2026-05-11 05:56 UTC | `INCONCLUSIVE` | Finite-Field Rank Threshold for ACC⁰ Circuit Complexity |
| 2026-05-11 06:02 UTC | `INCONCLUSIVE` | Secant Rank Lower Bound for Disjointness Tensors |
| 2026-05-11 06:31 UTC | `INCONCLUSIVE` | Real Dimension of Parity-Constraint Variety Bounds AC⁰ Depth |
| 2026-05-11 07:16 UTC | `INCONCLUSIVE` | Cheeger Constant Inverse Proportional to Extended Frege Proof Siz |
| 2026-05-11 07:42 UTC | `INCONCLUSIVE` | Communication Matrix Rank Lower Bounds ABP Size for Boolean Funct |
| 2026-05-11 08:00 UTC | `INCONCLUSIVE` | Invariant Generator Count Bounds SOS Refutation Degree for Symmet |
| 2026-05-11 08:32 UTC | `INCONCLUSIVE` | Newton Polytope Volume Inverse Proportional to SOS Degree for Max |
| 2026-05-11 08:45 UTC | `INCONCLUSIVE` | Krull Dimension Lower Bounds SOS Refutation Degree for 3-SAT |
| 2026-05-11 10:35 UTC | `INCONCLUSIVE` | Finite-Field Rank Threshold for ACC⁰ Circuit Complexity |
| 2026-05-11 11:01 UTC | `INCONCLUSIVE` | Gonality Lower Bounds for Disjointness Communication Matrices |
| 2026-05-11 11:36 UTC | `INCONCLUSIVE` | Projective Plane Disjointness Complexity Bounded by Line Count |
| 2026-05-11 12:25 UTC | `INCONCLUSIVE` | Noncommutative Rank Bounded by Disjointness Communication Complex |

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