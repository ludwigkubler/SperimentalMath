---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-08 19:41 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-08 19:41 UTC

- Cycles recorded: **424**
- Time span: 358.0h (~1.18 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 389 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 16 |
| Matroid Theory | 7 |
| Free Probability | 7 |
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
| Schur-Weyl duality | 3 |
| Spectral Graph Theory | 3 |
| Polymatroid Theory | 3 |
| Persistent Homology | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Schur-Weyl duality, plethysm, algebraic combinatorics | 2 |
| Free Probability Theory | 2 |
| Tropical Circuit Weight Analysis (TCWA) — Bounded Arithmetic | 2 |
| Bounded Arithmetic | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-08 16:16 UTC | `INCONCLUSIVE` | Invariant Polynomial Generation Complexity in Determinant vs Perm |
| 2026-05-08 17:02 UTC | `INCONCLUSIVE` | Covering Radius Bound on Set System Discrepancy |
| 2026-05-08 17:17 UTC | `INCONCLUSIVE` | Algebraic Geometry Solution Count Lower Bound on ACC^0 Circuit Si |
| 2026-05-08 17:23 UTC | `INCONCLUSIVE` | Matroid Rank Deficit in Monotone DNF Depth for k-CLIQUE |
| 2026-05-08 17:36 UTC | `INCONCLUSIVE` | Betti Number Exponential Lower Bound on Tseitin Resolution Length |
| 2026-05-08 17:49 UTC | `INCONCLUSIVE` | Tensor Rank Lower Bound on SOS Refutation Size for Symmetric CSPs |
| 2026-05-08 18:02 UTC | `INCONCLUSIVE` | Newton Polytope Vertex Count Bounds SOS Degree for Max-CUT Approx |
| 2026-05-08 18:22 UTC | `INCONCLUSIVE` | Noncommutative Quantum Dimension Lower Bound on Disjointness |
| 2026-05-08 18:36 UTC | `INCONCLUSIVE` | Noncommutative Norm Gap in Read-Twice Branching Programs for IP_2 |
| 2026-05-08 18:47 UTC | `INCONCLUSIVE` | Laplacian Eigenvalue Deficit Bounds SOS Degree for Max-CUT |
| 2026-05-08 18:56 UTC | `INCONCLUSIVE` | Diophantine Approximation Bound on Resolution Proof Size |
| 2026-05-08 19:10 UTC | `INCONCLUSIVE` | Submodular Coverage Deficit in Monotone DNF for k-CLIQUE |
| 2026-05-08 19:22 UTC | `INCONCLUSIVE` | Quandle Isomorphism Complexity and ACC^0 Circuit Depth |
| 2026-05-08 19:28 UTC | `INCONCLUSIVE` | Schur-Weyl Decomposition Rank Lower Bounds Disjointness Communica |
| 2026-05-08 19:41 UTC | `INCONCLUSIVE` | Persistent Homology Barcode Length Inversely Proportional to DPLL |

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