---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 05:45 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 05:45 UTC

- Cycles recorded: **347**
- Time span: 344.1h (~1.01 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 316 |
| FALSIFIED | 15 |
| BARRIER_HIT | 12 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 10 |
| Matroid Theory | 5 |
| Algebraic Geometry | 5 |
| Additive Combinatorics | 5 |
| Finite Geometry | 5 |
| Free Probability | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Random Matrix Theory | 4 |
| Fourier analysis of boolean functions | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl Duality | 3 |
| Spectral Graph Theory | 3 |
| Polymatroid Theory | 3 |
| Algebraic Geometry of Secant Varieties | 3 |
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
| 2026-05-08 02:26 UTC | `INCONCLUSIVE` | Finite Plane Line Count Bounds Tseitin Resolution Size |
| 2026-05-08 02:37 UTC | `INCONCLUSIVE` | Tree-Depth of Tseitin Graph Bounds Resolution Length |
| 2026-05-08 03:03 UTC | `INCONCLUSIVE` | Projective Plane Incidence Matrix Deterministic Communication Com |
| 2026-05-08 03:10 UTC | `INCONCLUSIVE` | Multilinear Catalecticant Rank Scales Polynomially in ACC^0 Circu |
| 2026-05-08 03:25 UTC | `INCONCLUSIVE` | Asymptotic Dimension of KW Space for PARITY Matches Optimal Formu |
| 2026-05-08 03:37 UTC | `INCONCLUSIVE` | Free Logarithmic Energy Deficit Lower-Bounds R(DISJ) |
| 2026-05-08 03:38 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice BP for IP_2 |
| 2026-05-08 04:12 UTC | `INCONCLUSIVE` | Second-Read Commutator Frobenius Excess Bounds Read-Twice BP Size |
| 2026-05-08 04:33 UTC | `INCONCLUSIVE` | Additive Energy of Fourier Coefficients Bounds SOS Refutation Siz |
| 2026-05-08 04:46 UTC | `INCONCLUSIVE` | A_5 Word-Embedding Spectral Norm Lower-Bounds R(DISJ) |
| 2026-05-08 05:10 UTC | `INCONCLUSIVE` | Algebraic Connectivity Inverse Lower-Bounds Tseitin Resolution Le |
| 2026-05-08 05:18 UTC | `INCONCLUSIVE` | Metric Dimension Lower Bound on Tseitin Resolution Length |
| 2026-05-08 05:24 UTC | `INCONCLUSIVE` | Witness-Complex Betti Sum Lower-Bounds Formula Depth |
| 2026-05-08 05:35 UTC | `INCONCLUSIVE` | Finite Field Representation Complexity and ACC^0 Circuit Size |
| 2026-05-08 05:45 UTC | `INCONCLUSIVE` | Matroid Connectivity and ACC^0 Circuit Size for 3-SAT Instances |

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