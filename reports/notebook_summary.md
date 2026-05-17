---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-17 07:23 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-17 07:23 UTC

- Cycles recorded: **734**
- Time span: 561.7h (~1.31 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 696 |
| BARRIER_HIT | 19 |
| FALSIFIED | 15 |
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
| 2026-05-17 00:26 UTC | `INCONCLUSIVE` | 2-adic Newton Slopes of DISJ Sub-blocks Scale as √n |
| 2026-05-17 00:49 UTC | `INCONCLUSIVE` | Cyclic Burnside Orbit Count Lower-Bounds AC⁰ Size for PARITY |
| 2026-05-17 01:28 UTC | `INCONCLUSIVE` | Cauchy Mean Width of Minterm Hull Lower-Bounds Monotone k-CLIQUE |
| 2026-05-17 02:01 UTC | `INCONCLUSIVE` | Costas Displacement Coincidence Lower-Bounds AC⁰ Size for PARITY |
| 2026-05-17 02:29 UTC | `INCONCLUSIVE` | Vertex Star-Discrepancy Equals Spectral Norm for XOR Comm |
| 2026-05-17 02:59 UTC | `INCONCLUSIVE` | Operator-SoS 4-Trace Gap Lower-Bounds Blocks-Order Read-Twice BP  |
| 2026-05-17 03:06 UTC | `BARRIER_HIT` | Cross-Side Fourier Symmetric-Difference Mass Lower-Bounds DISJ CC |
| 2026-05-17 03:32 UTC | `INCONCLUSIVE` | q-Major Cancellation Gap Separates Permanent from Determinant Sup |
| 2026-05-17 04:06 UTC | `INCONCLUSIVE` | Immanant Positivity Width Bounds Monotone KW Depth for Perfect Ma |
| 2026-05-17 04:32 UTC | `INCONCLUSIVE` | Curto-Fialkow Hankel Defect Separates Read-Twice IP_2 BPs |
| 2026-05-17 05:07 UTC | `INCONCLUSIVE` | Hodge-Cheeger Product Lower-Bounds Tseitin Resolution Length |
| 2026-05-17 05:45 UTC | `INCONCLUSIVE` | Sandpile Group Order Lower-Bounds Monotone KW Depth |
| 2026-05-17 06:17 UTC | `INCONCLUSIVE` | Conway Temperature Bounds Tree-Resolution Width for 3-SAT |
| 2026-05-17 06:44 UTC | `INCONCLUSIVE` | Hochster Regularity of Variable Co-Occurrence Graph Lower-Bounds  |
| 2026-05-17 07:23 UTC | `INCONCLUSIVE` | Ihara Zeta Entropy Predicts Tseitin DPLL Tree Size |

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