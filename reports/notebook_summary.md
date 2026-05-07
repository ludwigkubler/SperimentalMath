---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-07 22:46 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-07 22:46 UTC

- Cycles recorded: **315**
- Time span: 337.1h (~0.93 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 285 |
| FALSIFIED | 15 |
| BARRIER_HIT | 11 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 9 |
| Algebraic Geometry | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Matroid Theory | 4 |
| Additive Combinatorics | 4 |
| Fourier analysis of boolean functions | 3 |
| Random Matrix Theory | 3 |
| Finite Geometry | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl Duality | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| matroid theory | 2 |
| Free Probability Theory | 2 |
| Tropical Circuit Weight Analysis (TCWA) — Bounded Arithmetic | 2 |
| Bounded Arithmetic | 2 |
| Free Probability | 2 |
| Geometric Complexity Theory | 2 |
| Additive combinatorics | 2 |
| Schur-Weyl duality | 2 |
| Noncommutative L^p Geometry | 2 |
| Tropical Circuit Weight Analysis (TCWA) in BOUNDED_ARITHMETIC | 2 |
| Spectral Graph Theory | 2 |
| Polymatroid Theory | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-07 20:33 UTC | `INCONCLUSIVE` | Hashimoto Non-Backtracking Pole Gap Lower-Bounds Tseitin Resoluti |
| 2026-05-07 20:41 UTC | `INCONCLUSIVE` | Tropical Convex Hull Dimension and ACC^0 Circuit Size |
| 2026-05-07 20:48 UTC | `INCONCLUSIVE` | Fourier Coefficient Sum Lower-Bounds Resolution Length for 3-CNFs |
| 2026-05-07 20:58 UTC | `INCONCLUSIVE` | Non-Abelian Fourier Coefficient Boundedness in Tseitin Resolution |
| 2026-05-07 21:02 UTC | `INCONCLUSIVE` | Free Cumulant κ₄ of Disjointness Spectrum Lower-Bounds R(DISJ) |
| 2026-05-07 21:03 UTC | `INCONCLUSIVE` | Algebraic Matroid Rank and ACC^0 Circuit Size Trade-off |
| 2026-05-07 21:18 UTC | `INCONCLUSIVE` | Maximum Fourier Coefficient Lower Bound via Sensitivity Scaling |
| 2026-05-07 21:40 UTC | `INCONCLUSIVE` | Roth Density of ACC⁰ Truth Tables Lower-Bounds Sipser Hardness |
| 2026-05-07 21:41 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower-Bounds Disjointness Communication  |
| 2026-05-07 21:46 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower-Bounds Disjointness Communication  |
| 2026-05-07 22:08 UTC | `INCONCLUSIVE` | Lyndon Factor Width Lower-Bounds Tree-Like Resolution |
| 2026-05-07 22:09 UTC | `INCONCLUSIVE` | Polymatroid Rank Gap in Monotone DNF Depth for k-CLIQUE |
| 2026-05-07 22:33 UTC | `INCONCLUSIVE` | Finite Plane Line Count Bounds MCSP Complexity |
| 2026-05-07 22:35 UTC | `BARRIER_HIT` | Leinster Magnitude of Hamming-Embedded Communication Matrices Low |
| 2026-05-07 22:46 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice Branching Programs for IP_2 |

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