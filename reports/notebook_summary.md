---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 08:45 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 08:45 UTC

- Cycles recorded: **372**
- Time span: 347.1h (~1.07 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 340 |
| FALSIFIED | 15 |
| BARRIER_HIT | 13 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 14 |
| Free Probability | 7 |
| Matroid Theory | 6 |
| Algebraic Geometry | 5 |
| Additive Combinatorics | 5 |
| Finite Geometry | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Random Matrix Theory | 4 |
| Schur-Weyl Duality | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| Fourier analysis of boolean functions | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Spectral Graph Theory | 3 |
| Polymatroid Theory | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| matroid theory | 2 |
| Free Probability Theory | 2 |
| Tropical Circuit Weight Analysis (TCWA) — Bounded Arithmetic | 2 |
| Bounded Arithmetic | 2 |
| Geometric Complexity Theory | 2 |
| Additive combinatorics | 2 |
| Schur-Weyl duality | 2 |
| Noncommutative L^p Geometry | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-08 06:56 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower-Bounds Disjointness Communication  |
| 2026-05-08 07:12 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice BPs Bounds Disjointness Communica |
| 2026-05-08 07:21 UTC | `INCONCLUSIVE` | Gowers Uniformity Norm of Boolean Functions Bounds ACC⁰ Circuit S |
| 2026-05-08 07:33 UTC | `INCONCLUSIVE` | Low-Degree Fourier Mass of Cut Indicator Bounds Tseitin Resolutio |
| 2026-05-08 07:38 UTC | `INCONCLUSIVE` | Monomial Ideal Generators and Frege Proof Complexity |
| 2026-05-08 07:43 UTC | `INCONCLUSIVE` | Positivstellensatz Rank Lower-Bounds SOS Max-CUT Degree |
| 2026-05-08 07:54 UTC | `INCONCLUSIVE` | Real Stable Rank Lower-Bounds AC⁰ PARITY Circuit Size |
| 2026-05-08 08:00 UTC | `INCONCLUSIVE` | Real Variety Connectedness Lower Bound on SOS Degree for Max-CUT |
| 2026-05-08 08:01 UTC | `INCONCLUSIVE` | Legendre-Symbol Partial-Sum Anomaly Excludes ACC^0 |
| 2026-05-08 08:12 UTC | `INCONCLUSIVE` | Möbius Coinvariant of Minterm Intersection Lattice Bounds k-CLIQU |
| 2026-05-08 08:22 UTC | `INCONCLUSIVE` | Network Reliability Deficit Lower-Bounds Tseitin Resolution |
| 2026-05-08 08:28 UTC | `INCONCLUSIVE` | Three-Distance Beatty Ordering Matches Avg DPLL on Random 3-SAT |
| 2026-05-08 08:32 UTC | `INCONCLUSIVE` | Lie Nilpotency Class of Layer Algebra Distinguishes Read-Twice BP |
| 2026-05-08 08:40 UTC | `INCONCLUSIVE` | SVD Participation Dispersion of Mid-Layer Lower-Bounds Read-Twice |
| 2026-05-08 08:45 UTC | `INCONCLUSIVE` | Hypercontractive L4/L2 Flatness of Clause-Count Lower-Bounds DPLL |

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