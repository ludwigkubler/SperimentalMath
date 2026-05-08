---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 13:42 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 13:42 UTC

- Cycles recorded: **398**
- Time span: 352.0h (~1.13 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 364 |
| FALSIFIED | 15 |
| BARRIER_HIT | 15 |
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
| Fourier analysis of boolean functions | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Spectral Graph Theory | 3 |
| Polymatroid Theory | 3 |
| FOURIER_ANALYSIS | 3 |
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
| 2026-05-08 10:49 UTC | `INCONCLUSIVE` | Schur-Horn Diagonal-Spectrum Defect Bounds SOS-2 Max-Cut Gap |
| 2026-05-08 11:00 UTC | `INCONCLUSIVE` | Bregman-Minc Permanent Defect Lower-Bounds SOS-2 Max-Cut Gap on T |
| 2026-05-08 11:07 UTC | `INCONCLUSIVE` | Selberg Log-Gas Rigidity Defect Bounds SOS-2 Max-CUT Gap |
| 2026-05-08 11:12 UTC | `BARRIER_HIT` | Lasserre Moment-Rank Gap of Accept Set Bounds AC0 PARITY Size |
| 2026-05-08 11:22 UTC | `INCONCLUSIVE` | Forman-Ricci Negative-Edge Count Lower-Bounds Tseitin DPLL Size |
| 2026-05-08 11:42 UTC | `INCONCLUSIVE` | Matroid Rank Gap in Monotone DNF Depth for k-CLIQUE |
| 2026-05-08 11:59 UTC | `INCONCLUSIVE` | Fourier Coefficient Flatness Implies Worst-Case Hardness for Bool |
| 2026-05-08 12:13 UTC | `INCONCLUSIVE` | Fourier Coefficient Product Lower Bound on Disjointness Communica |
| 2026-05-08 12:27 UTC | `INCONCLUSIVE` | Fourier Coefficient Decay Implies SOS Degree Lower Bound for Max- |
| 2026-05-08 12:50 UTC | `INCONCLUSIVE` | Communication Matrix Discrepancy Lower Bound for AC⁰ PARITY Circu |
| 2026-05-08 13:02 UTC | `INCONCLUSIVE` | Seed Length of Nisan-Wigderson PRG Bounded by Minimal Linear Appr |
| 2026-05-08 13:14 UTC | `INCONCLUSIVE` | Operator Norm Separation for Read-Twice Branching Programs |
| 2026-05-08 13:26 UTC | `INCONCLUSIVE` | Plethysm Multiplicity Gap in Symmetric Powers of Permanent vs Det |
| 2026-05-08 13:36 UTC | `INCONCLUSIVE` | Moment-Matrix Rank Deficit in Max-CUT Approximation |
| 2026-05-08 13:42 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower Bounds Disjointness Communication  |

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