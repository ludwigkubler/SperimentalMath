---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 03:38 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 03:38 UTC

- Cycles recorded: **339**
- Time span: 342.0h (~0.99 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 308 |
| FALSIFIED | 15 |
| BARRIER_HIT | 12 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 10 |
| Algebraic Geometry | 5 |
| Finite Geometry | 5 |
| Free Probability | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Matroid Theory | 4 |
| Random Matrix Theory | 4 |
| Additive Combinatorics | 4 |
| Fourier analysis of boolean functions | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl Duality | 3 |
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
| Tropical Circuit Weight Analysis (TCWA) in BOUNDED_ARITHMETIC | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-08 00:42 UTC | `BARRIER_HIT` | Stern-Brocot Rank of Truth Tables Lifts Average-to-Worst MCSP |
| 2026-05-08 01:14 UTC | `INCONCLUSIVE` | Slice Rank of Layer-Variable Tensor Lower-Bounds Read-Twice BP Si |
| 2026-05-08 01:18 UTC | `INCONCLUSIVE` | Polymatroid Rank Lower Bound for Monotone DNF Representing k-CLIQ |
| 2026-05-08 01:28 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice BP for IP_2 |
| 2026-05-08 01:44 UTC | `INCONCLUSIVE` | Persistent Homology Barcodes and Communication Complexity of Bool |
| 2026-05-08 01:52 UTC | `INCONCLUSIVE` | Jacobi Recurrence b₂ Floor Constrains SoS-2 Max-CUT Ratio |
| 2026-05-08 02:11 UTC | `INCONCLUSIVE` | Orbit Closure Dimension Bounds Permanent Circuit Complexity |
| 2026-05-08 02:17 UTC | `INCONCLUSIVE` | Lie Stabilizer Dimension Linearly Bounds Arithmetic Formula Size |
| 2026-05-08 02:26 UTC | `INCONCLUSIVE` | Finite Plane Line Count Bounds Tseitin Resolution Size |
| 2026-05-08 02:37 UTC | `INCONCLUSIVE` | Tree-Depth of Tseitin Graph Bounds Resolution Length |
| 2026-05-08 03:03 UTC | `INCONCLUSIVE` | Projective Plane Incidence Matrix Deterministic Communication Com |
| 2026-05-08 03:10 UTC | `INCONCLUSIVE` | Multilinear Catalecticant Rank Scales Polynomially in ACC^0 Circu |
| 2026-05-08 03:25 UTC | `INCONCLUSIVE` | Asymptotic Dimension of KW Space for PARITY Matches Optimal Formu |
| 2026-05-08 03:37 UTC | `INCONCLUSIVE` | Free Logarithmic Energy Deficit Lower-Bounds R(DISJ) |
| 2026-05-08 03:38 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice BP for IP_2 |

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