---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-18 13:00 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-18 13:00 UTC

- Cycles recorded: **782**
- Time span: 591.3h (~1.32 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 742 |
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
| 2026-05-18 05:56 UTC | `INCONCLUSIVE` | Mansour L1 Fourier Mass of Clause-Falsification Polynomial Bounds |
| 2026-05-18 06:21 UTC | `INCONCLUSIVE` | Chang Spectrum Dimension of Wire-Source DFS Labels Bounds ACC^0[2 |
| 2026-05-18 06:47 UTC | `INCONCLUSIVE` | Bourgain Noise-Sensitivity Mass of Clause-Falsification Polynomia |
| 2026-05-18 07:28 UTC | `INCONCLUSIVE` | Generated Algebra Dimension of Layer Operators Bounds IP_2 Read-T |
| 2026-05-18 08:08 UTC | `INCONCLUSIVE` | Szegedy Quantum-Walk Phase Gap Lower-Bounds Tseitin Tree-Resoluti |
| 2026-05-18 08:28 UTC | `INCONCLUSIVE` | Halász L^2 Spectrum Discrepancy Lower-Bounds Sign-Matrix Rigidity |
| 2026-05-18 08:56 UTC | `INCONCLUSIVE` | Mostar Index of Gate-Adjacency Graph Bounds ACC^0[m] Size for MOD |
| 2026-05-18 09:23 UTC | `INCONCLUSIVE` | Patience-Sort LIS of XOR-Lifted Row Permutations Bounds CC^D |
| 2026-05-18 09:54 UTC | `INCONCLUSIVE` | Effective Resistance of Charged Vertex Pairs Bounds Tseitin DPLL  |
| 2026-05-18 10:26 UTC | `INCONCLUSIVE` | p=3 Path-Family Modulus Lower-Bounds Tseitin Tree-Resolution |
| 2026-05-18 11:02 UTC | `INCONCLUSIVE` | Viennot Heap Radius of Clause-Conflict Graph Bounds Frege Depth |
| 2026-05-18 11:29 UTC | `INCONCLUSIVE` | Lee-Yang Zero Cluster Angle of Cut Polynomial Bounds Max-Cut SoS- |
| 2026-05-18 11:55 UTC | `INCONCLUSIVE` | Additive Energy of Out-Degree Sequence Bounds ACC^0[2] MOD_3 Size |
| 2026-05-18 12:32 UTC | `INCONCLUSIVE` | SBM Detectability Gap of Literal Conflict Graph Bounds DPLL Time |
| 2026-05-18 13:00 UTC | `INCONCLUSIVE` | Fiedler Participation Entropy Lower-Bounds Tseitin Tree-Resolutio |

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