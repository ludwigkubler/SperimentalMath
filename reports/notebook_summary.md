---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-11 18:31 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-11 18:31 UTC

- Cycles recorded: **618**
- Time span: 428.8h (~1.44 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 581 |
| BARRIER_HIT | 18 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 34 |
| Schur-Weyl Duality | 19 |
| Representation Theory of Symmetric Groups | 17 |
| Free Probability | 14 |
| Matroid Theory | 12 |
| Additive Combinatorics | 10 |
| Noncommutative L^p Geometry | 8 |
| Polymatroid Theory | 8 |
| Algebraic Geometry | 7 |
| Random Matrix Theory | 7 |
| Finite Geometry | 6 |
| Spectral Graph Theory | 6 |
| Plethysm Theory | 6 |
| Free Probability Theory | 5 |
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
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl duality | 3 |
| Diophantine Approximation | 3 |
| Persistent Homology | 3 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-11 13:41 UTC | `INCONCLUSIVE` | Plethysm Coefficient Inverse Proportional to Disjointness Communi |
| 2026-05-11 13:48 UTC | `INCONCLUSIVE` | Secant Rank of Disjointness Communication Matrix Bounds Randomize |
| 2026-05-11 14:19 UTC | `INCONCLUSIVE` | Kronecker Coefficient Gap in Symmetric Powers of Permanent vs Det |
| 2026-05-11 14:27 UTC | `INCONCLUSIVE` | Non-Commutative Rank Gap in Read-Twice BPs for IP_2 |
| 2026-05-11 14:33 UTC | `INCONCLUSIVE` | Standard Young Tableaux Count vs Monotone Circuit Size |
| 2026-05-11 14:42 UTC | `INCONCLUSIVE` | Real Rank of Moment Matrix Bounded by SOS Refutation Degree for C |
| 2026-05-11 14:59 UTC | `INCONCLUSIVE` | Schatten p-Norm Inverse Proportional to Disjointness Communicatio |
| 2026-05-11 15:18 UTC | `INCONCLUSIVE` | Tree-Depth Exponentiation Bounds Tseitin Resolution Length |
| 2026-05-11 15:41 UTC | `INCONCLUSIVE` | Resultant Degree Bounds Frege Proof Size for Tautologies |
| 2026-05-11 15:49 UTC | `INCONCLUSIVE` | Plethysm Coefficient Gap in Monotone Circuit Complexity for Perma |
| 2026-05-11 16:11 UTC | `INCONCLUSIVE` | Real Rank of Depth-3 AC⁰ Circuits for PARITY is Ω(log n) |
| 2026-05-11 17:00 UTC | `INCONCLUSIVE` | Quadratic Form Solution Count Exponential Gap in ACC⁰ Sipser Circ |
| 2026-05-11 17:52 UTC | `INCONCLUSIVE` | Additive Energy Inverse Proportional to Discrepancy of Sumset Com |
| 2026-05-11 18:06 UTC | `INCONCLUSIVE` | Symmetric Square Multiplicity Gap in Permanent vs Determinant Dec |
| 2026-05-11 18:31 UTC | `INCONCLUSIVE` | Free Cumulant Sum Gap in Read-Twice BP Transition Matrices |

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