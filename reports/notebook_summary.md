---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 00:42 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 00:42 UTC

- Cycles recorded: **325**
- Time span: 339.0h (~0.96 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 294 |
| FALSIFIED | 15 |
| BARRIER_HIT | 12 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 10 |
| Algebraic Geometry | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Matroid Theory | 4 |
| Random Matrix Theory | 4 |
| Additive Combinatorics | 4 |
| Fourier analysis of boolean functions | 3 |
| Finite Geometry | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Free Probability | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl Duality | 3 |
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
| Spectral Graph Theory | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-07 22:08 UTC | `INCONCLUSIVE` | Lyndon Factor Width Lower-Bounds Tree-Like Resolution |
| 2026-05-07 22:09 UTC | `INCONCLUSIVE` | Polymatroid Rank Gap in Monotone DNF Depth for k-CLIQUE |
| 2026-05-07 22:33 UTC | `INCONCLUSIVE` | Finite Plane Line Count Bounds MCSP Complexity |
| 2026-05-07 22:35 UTC | `BARRIER_HIT` | Leinster Magnitude of Hamming-Embedded Communication Matrices Low |
| 2026-05-07 22:46 UTC | `INCONCLUSIVE` | Free Cumulant Gap in Read-Twice Branching Programs for IP_2 |
| 2026-05-07 22:58 UTC | `INCONCLUSIVE` | Kronecker Coefficient Asymmetry in Symmetric Tensor Decomposition |
| 2026-05-07 23:11 UTC | `INCONCLUSIVE` | Cubical Euler Characteristic Bounds DNF-Min for Symmetric Functio |
| 2026-05-07 23:12 UTC | `INCONCLUSIVE` | Random Matrix Spectral Norm and SOS Refutation Degree for 3-CNF |
| 2026-05-07 23:34 UTC | `INCONCLUSIVE` | Real Radical Rank and SOS Degree for Max-CUT |
| 2026-05-07 23:41 UTC | `INCONCLUSIVE` | Lorentzian Defect of Tseitin Moment Polynomial Lower-Bounds SOS D |
| 2026-05-07 23:53 UTC | `INCONCLUSIVE` | Persistent Homology Barcodes and Resolution Proof Size for Tseiti |
| 2026-05-07 23:58 UTC | `INCONCLUSIVE` | Free Cumulant Rank Gap in Read-Twice Branching Programs for IP_2 |
| 2026-05-08 00:24 UTC | `INCONCLUSIVE` | Möbius Mass of Gate-Support Meet-Semilattice Bounds AC⁰ PARITY Si |
| 2026-05-08 00:38 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower-Bounds Disjointness Communication  |
| 2026-05-08 00:42 UTC | `BARRIER_HIT` | Stern-Brocot Rank of Truth Tables Lifts Average-to-Worst MCSP |

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