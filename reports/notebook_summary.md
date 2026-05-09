---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-09 04:46 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-09 04:46 UTC

- Cycles recorded: **458**
- Time span: 367.1h (~1.25 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 423 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 20 |
| Schur-Weyl Duality | 9 |
| Free Probability | 8 |
| Matroid Theory | 7 |
| Additive Combinatorics | 6 |
| Algebraic Geometry | 5 |
| Random Matrix Theory | 5 |
| Finite Geometry | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Spectral Graph Theory | 4 |
| Polymatroid Theory | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Fourier analysis of boolean functions | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl duality | 3 |
| Representation Theory of Symmetric Groups | 3 |
| Persistent Homology | 3 |
| Plethysm Theory | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Schur-Weyl duality, plethysm, algebraic combinatorics | 2 |
| Free Probability Theory | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-09 00:45 UTC | `INCONCLUSIVE` | Plethysm Coefficient Inverse Proportionality to Circuit Size |
| 2026-05-09 00:51 UTC | `INCONCLUSIVE` | Free Entropy Inverse Proportionality to Disjointness Communicatio |
| 2026-05-09 00:57 UTC | `INCONCLUSIVE` | Young Tableaux Count Lower Bound on Disjointness Communication Co |
| 2026-05-09 01:10 UTC | `INCONCLUSIVE` | Symmetric Polynomial Monomial Count and Resolution Proof Size for |
| 2026-05-09 01:41 UTC | `INCONCLUSIVE` | Valuation Rank of Polynomial Coefficients Bounds ACC^0 Circuit Si |
| 2026-05-09 02:24 UTC | `INCONCLUSIVE` | Plethysm Coefficient Inverse Proportionality to SOS Refutation Si |
| 2026-05-09 02:52 UTC | `INCONCLUSIVE` | Young Tableaux Ratio Exponential Lower Bound on Permanent Circuit |
| 2026-05-09 03:07 UTC | `INCONCLUSIVE` | Plethysm Coefficient Exponential Gap in Symmetric Squares of Perm |
| 2026-05-09 03:18 UTC | `INCONCLUSIVE` | Schur-Weyl Multiplicity Exponential Gap in Symmetric Powers of Pe |
| 2026-05-09 03:44 UTC | `INCONCLUSIVE` | SOS Refutation Degree and Convex Body Volume for Random 3-SAT |
| 2026-05-09 03:53 UTC | `INCONCLUSIVE` | Random Matrix Eigenvalue Deficit and SOS Degree for Max-CUT |
| 2026-05-09 04:05 UTC | `INCONCLUSIVE` | Real Radical Rank Bounds SOS Degree for Max-CUT |
| 2026-05-09 04:26 UTC | `INCONCLUSIVE` | Discriminant Exponentiation Bounds SOS Refutation Degree for Rand |
| 2026-05-09 04:34 UTC | `INCONCLUSIVE` | Spectral Gap Exponential Lower Bound on Tseitin Resolution Length |
| 2026-05-09 04:46 UTC | `INCONCLUSIVE` | Dehn Function Exponentiation Bounds Resolution Length for Tseitin |

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