---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 06:40 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 06:40 UTC

- Cycles recorded: **355**
- Time span: 345.0h (~1.03 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 323 |
| FALSIFIED | 15 |
| BARRIER_HIT | 13 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 11 |
| Matroid Theory | 6 |
| Free Probability | 6 |
| Algebraic Geometry | 5 |
| Additive Combinatorics | 5 |
| Finite Geometry | 5 |
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
| 2026-05-08 04:33 UTC | `INCONCLUSIVE` | Additive Energy of Fourier Coefficients Bounds SOS Refutation Siz |
| 2026-05-08 04:46 UTC | `INCONCLUSIVE` | A_5 Word-Embedding Spectral Norm Lower-Bounds R(DISJ) |
| 2026-05-08 05:10 UTC | `INCONCLUSIVE` | Algebraic Connectivity Inverse Lower-Bounds Tseitin Resolution Le |
| 2026-05-08 05:18 UTC | `INCONCLUSIVE` | Metric Dimension Lower Bound on Tseitin Resolution Length |
| 2026-05-08 05:24 UTC | `INCONCLUSIVE` | Witness-Complex Betti Sum Lower-Bounds Formula Depth |
| 2026-05-08 05:35 UTC | `INCONCLUSIVE` | Finite Field Representation Complexity and ACC^0 Circuit Size |
| 2026-05-08 05:45 UTC | `INCONCLUSIVE` | Matroid Connectivity and ACC^0 Circuit Size for 3-SAT Instances |
| 2026-05-08 05:56 UTC | `INCONCLUSIVE` | Sparsest-Cut LP Value Lower-Bounds Tseitin Resolution Length |
| 2026-05-08 06:04 UTC | `INCONCLUSIVE` | Real Dimension Lower Bound for AC⁰ PARITY Circuits |
| 2026-05-08 06:11 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice Branching Programs for IP_2 |
| 2026-05-08 06:17 UTC | `BARRIER_HIT` | Plunnecke Doubling of Top-Fourier Spectrum Bounds ACC0 Size |
| 2026-05-08 06:23 UTC | `INCONCLUSIVE` | Matroid Rank Lower-Bounds Disjointness Communication Complexity |
| 2026-05-08 06:34 UTC | `INCONCLUSIVE` | Tree-to-Dimension Tightness for MAJ_3: Optimal KW Protocols Yield |
| 2026-05-08 06:34 UTC | `INCONCLUSIVE` | Asymptotic Dimension and Resolution Length for Tseitin Formulas |
| 2026-05-08 06:40 UTC | `INCONCLUSIVE` | Matroid Spread Bounded by Monotone DNF Size |

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