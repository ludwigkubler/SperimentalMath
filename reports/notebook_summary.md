---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-01 09:13 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-01 09:13 UTC

- Cycles recorded: **277**
- Time span: 179.5h (~1.54 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 249 |
| FALSIFIED | 15 |
| BARRIER_HIT | 9 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 7 |
| Algebraic Geometry | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
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
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 2 |
| Bounded Arithmetic | 2 |
| Geometric Complexity Theory | 2 |
| Schur-Weyl duality | 2 |
| Schur-Weyl Duality | 2 |
| Noncommutative L^p Geometry | 2 |
| Combinatorial homotopy theory | 1 |
| Kazhdan-Lusztig theory of Hecke algebras | 1 |
| Combinatorial algebraic topology | 1 |
| Knot theory (quantum invariants) | 1 |
| Quadratic forms over finite fields (Grothendieck-Witt groups) | 1 |
| Clifford algebras over finite fields | 1 |
| Toric geometry (via Gröbner degenerations) | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-01 03:07 UTC | `INCONCLUSIVE` | Matroid Rank and Minimal Circuit Size for Boolean Functions |
| 2026-05-01 03:27 UTC | `INCONCLUSIVE` | Bounded Arithmetic Proof Length and Circuit Complexity for Tautol |
| 2026-05-01 03:54 UTC | `INCONCLUSIVE` | Duality-Preserved Homotopy Stability |
| 2026-05-01 04:01 UTC | `INCONCLUSIVE` | Symmetric Power Partition Dominance in Permanent vs Determinant |
| 2026-05-01 04:36 UTC | `INCONCLUSIVE` | Schur-Weyl Multiplicity Gap in Permanent vs Determinant Tensor Po |
| 2026-05-01 05:04 UTC | `INCONCLUSIVE` | Bounded Arithmetic Proof Length and 3-SAT Tautology Resolution Co |
| 2026-05-01 05:36 UTC | `INCONCLUSIVE` | Noncommutative L^p Norm Lower Bounds for Disjointness Communicati |
| 2026-05-01 05:58 UTC | `INCONCLUSIVE` | Phase Merging Complexity Bound |
| 2026-05-01 06:07 UTC | `INCONCLUSIVE` | Noncommutative L^p Norm Lower Bounds for Disjointness |
| 2026-05-01 06:41 UTC | `INCONCLUSIVE` | Real Rank of Coefficient Matrices for AC⁰ PARITY Circuits |
| 2026-05-01 07:13 UTC | `BARRIER_HIT` | Tropical Circuit Homotopy Stability under Weight Accumulation |
| 2026-05-01 07:17 UTC | `BARRIER_HIT` | Orbit Closure Dimension vs. Boolean Circuit Size |
| 2026-05-01 07:55 UTC | `INCONCLUSIVE` | Homotopy Type and AC^0 Complexity |
| 2026-05-01 08:38 UTC | `INCONCLUSIVE` | Littlewood-Richardson Coefficient Gap in Permanent vs Determinant |
| 2026-05-01 09:12 UTC | `INCONCLUSIVE` | Algebraic Curve Genus and Communication Complexity Lower Bound |

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