---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-18 03:29 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-18 03:29 UTC

- Cycles recorded: **763**
- Time span: 581.8h (~1.31 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 723 |
| BARRIER_HIT | 20 |
| FALSIFIED | 16 |
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
| 2026-05-17 18:27 UTC | `INCONCLUSIVE` | Burau Trace Defect of Clause Braid Lower-Bounds Tree-Resolution S |
| 2026-05-17 19:02 UTC | `INCONCLUSIVE` | Euler Characteristic of Gate-Conflict Independence Complex Bounds |
| 2026-05-17 19:17 UTC | `INCONCLUSIVE` | Tamari Rotation Rank of Canonical DT Lower-Bounds XOR-Lifted F2-R |
| 2026-05-17 19:47 UTC | `INCONCLUSIVE` | Immanant Log-Variance Separates Random Matrices from Det-Padded B |
| 2026-05-17 20:14 UTC | `INCONCLUSIVE` | Hypercontractive Term-Support Stable Rank Bounds Monotone Clique  |
| 2026-05-17 20:26 UTC | `INCONCLUSIVE` | S-Transform Free-Mult Defect Lower-Bounds DISJ Communication |
| 2026-05-17 20:47 UTC | `INCONCLUSIVE` | Fekete Capacity of Laplacian Spectrum Upper-Bounds Max-Cut SoS-2  |
| 2026-05-17 21:20 UTC | `INCONCLUSIVE` | Polymer Cluster-Expansion Convergence Radius Bounds Tree-Res Size |
| 2026-05-17 21:53 UTC | `INCONCLUSIVE` | Fatgraph Genus of Canonical Clause Ribbon Lower-Bounds Resolution |
| 2026-05-17 22:25 UTC | `FALSIFIED` | Forman-Ricci Min-Curvature of Term-Overlap Graph Lower-Bounds Mon |
| 2026-05-17 22:43 UTC | `INCONCLUSIVE` | Bourgain-Tzafriri Sub-Column Spectral Excess Bounds DISJ CC_R |
| 2026-05-17 23:19 UTC | `INCONCLUSIVE` | Trivial-Isotype Mass Gap Separates Perm from Padded Det |
| 2026-05-17 23:46 UTC | `INCONCLUSIVE` | Eulerian Descent Entropy Separates Perm from Padded Det_m |
| 2026-05-18 00:33 UTC | `INCONCLUSIVE` | Signed-Laplacian Holonomy Spectrum Bounds Tseitin Tree-Resolution |
| 2026-05-18 03:29 UTC | `INCONCLUSIVE` | Bonami-Beckner 4-2 Saturation of Clause-Sum Bounds DPLL Depth |

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