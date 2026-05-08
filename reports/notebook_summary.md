---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 16:30 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 16:30 UTC

- Cycles recorded: **410**
- Time span: 354.8h (~1.16 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 375 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 15 |
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
| FOURIER_ANALYSIS | 4 |
| Fourier analysis of boolean functions | 3 |
| matroid theory | 3 |
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
| Schur-Weyl duality, plethysm, algebraic combinatorics | 2 |
| Free Probability Theory | 2 |
| Tropical Circuit Weight Analysis (TCWA) — Bounded Arithmetic | 2 |
| Bounded Arithmetic | 2 |
| Geometric Complexity Theory | 2 |
| Additive combinatorics | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-08 13:26 UTC | `INCONCLUSIVE` | Plethysm Multiplicity Gap in Symmetric Powers of Permanent vs Det |
| 2026-05-08 13:36 UTC | `INCONCLUSIVE` | Moment-Matrix Rank Deficit in Max-CUT Approximation |
| 2026-05-08 13:42 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower Bounds Disjointness Communication  |
| 2026-05-08 13:48 UTC | `INCONCLUSIVE` | Matroid Rank Deficit in Monotone DNF Depth for k-CLIQUE |
| 2026-05-08 14:08 UTC | `INCONCLUSIVE` | Monochromatic Rectangle Density Lower Bounds for PARITY Communica |
| 2026-05-08 14:26 UTC | `INCONCLUSIVE` | Spectral Gap Lower Bound on Tseitin Resolution Length |
| 2026-05-08 14:45 UTC | `INCONCLUSIVE` | Hilbert Series Complexity of Orbit Closures for Permanent vs Dete |
| 2026-05-08 14:52 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower Bounds for Disjointness Communicat |
| 2026-05-08 15:00 UTC | `INCONCLUSIVE` | Free Entropy Lower Bound on Disjointness Communication Complexity |
| 2026-05-08 15:06 UTC | `INCONCLUSIVE` | Invariant Degree Gap in Read-Twice Branching Programs for IP_2 |
| 2026-05-08 15:19 UTC | `BARRIER_HIT` | Bounded Arithmetic Complexity of Algebraic Closure in Finite Fiel |
| 2026-05-08 15:39 UTC | `INCONCLUSIVE` | Graph Energy Lower Bound on Tseitin Resolution Length |
| 2026-05-08 15:45 UTC | `INCONCLUSIVE` | Multiplicity Gap in Symmetric Powers of Permanent vs Determinant  |
| 2026-05-08 15:54 UTC | `INCONCLUSIVE` | Fourier Coefficient Sum Separation for Read-Twice Branching Progr |
| 2026-05-08 16:16 UTC | `INCONCLUSIVE` | Invariant Polynomial Generation Complexity in Determinant vs Perm |

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