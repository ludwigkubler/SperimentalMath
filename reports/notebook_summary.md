---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-01 05:36 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-01 05:36 UTC

- Cycles recorded: **269**
- Time span: 175.9h (~1.53 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 243 |
| FALSIFIED | 15 |
| BARRIER_HIT | 7 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 6 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Algebraic Geometry | 4 |
| Fourier analysis of boolean functions | 3 |
| Matroid Theory | 3 |
| Random Matrix Theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Additive Combinatorics | 2 |
| matroid theory | 2 |
| Free Probability Theory | 2 |
| Bounded Arithmetic | 2 |
| Schur-Weyl Duality | 2 |
| Combinatorial homotopy theory | 1 |
| Kazhdan-Lusztig theory of Hecke algebras | 1 |
| Combinatorial algebraic topology | 1 |
| Knot theory (quantum invariants) | 1 |
| Quadratic forms over finite fields (Grothendieck-Witt groups) | 1 |
| Clifford algebras over finite fields | 1 |
| Toric geometry (via Gröbner degenerations) | 1 |
| Arithmetic geometry (Tate-Shafarevich groups) | 1 |
| Geometric Langlands correspondence | 1 |
| Algebraic graph theory (chromatic polynomials) | 1 |
| Clifford algebras over real vector spaces | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-04-30 22:29 UTC | `FALSIFIED` | Duality-Preserved Phase Cell Bound |
| 2026-04-30 23:07 UTC | `INCONCLUSIVE` | Algebraic Geometry over Finite Fields and EF Proof Length |
| 2026-04-30 23:42 UTC | `INCONCLUSIVE` | Additive Energy Bounds for SOS Refutations of Sipser Functions |
| 2026-05-01 00:11 UTC | `INCONCLUSIVE` | Spectral Norm of SOS Relaxation and Refutation Size in Random 3-S |
| 2026-05-01 00:46 UTC | `INCONCLUSIVE` | Spectral Radius of SOS Moment Matrix Bounds Max-CUT Approximation |
| 2026-05-01 01:19 UTC | `INCONCLUSIVE` | Secant Variety Dimension Lower Bounds for Disjointness |
| 2026-05-01 02:01 UTC | `INCONCLUSIVE` | Irreducible Component Count Bounds Circuit Complexity for CNF |
| 2026-05-01 02:29 UTC | `INCONCLUSIVE` | Schur-Weyl Multiplicity Gap in Permanent Communication Matrices |
| 2026-05-01 03:07 UTC | `INCONCLUSIVE` | Matroid Rank and Minimal Circuit Size for Boolean Functions |
| 2026-05-01 03:27 UTC | `INCONCLUSIVE` | Bounded Arithmetic Proof Length and Circuit Complexity for Tautol |
| 2026-05-01 03:54 UTC | `INCONCLUSIVE` | Duality-Preserved Homotopy Stability |
| 2026-05-01 04:01 UTC | `INCONCLUSIVE` | Symmetric Power Partition Dominance in Permanent vs Determinant |
| 2026-05-01 04:36 UTC | `INCONCLUSIVE` | Schur-Weyl Multiplicity Gap in Permanent vs Determinant Tensor Po |
| 2026-05-01 05:04 UTC | `INCONCLUSIVE` | Bounded Arithmetic Proof Length and 3-SAT Tautology Resolution Co |
| 2026-05-01 05:36 UTC | `INCONCLUSIVE` | Noncommutative L^p Norm Lower Bounds for Disjointness Communicati |

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