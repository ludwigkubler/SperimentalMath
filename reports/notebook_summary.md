---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-30 23:42 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-30 23:42 UTC

- Cycles recorded: **257**
- Time span: 170.0h (~1.51 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 231 |
| FALSIFIED | 15 |
| BARRIER_HIT | 7 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier analysis of boolean functions | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Matroid Theory | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Algebraic Geometry | 2 |
| Random Matrix Theory | 2 |
| Additive Combinatorics | 2 |
| matroid theory | 2 |
| Free Probability Theory | 2 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 2 |
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
| Algebraic cycles (Chow groups over finite fields) | 1 |
| Algebraic lattice theory (Möbius functions of flow lattices) | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-04-30 16:12 UTC | `INCONCLUSIVE` | SOS Moment Matrix Rank and Real Variety Dimension for Max-CUT |
| 2026-04-30 16:48 UTC | `INCONCLUSIVE` | Bounded Arithmetic Proof Complexity and Resolution Length |
| 2026-04-30 17:18 UTC | `INCONCLUSIVE` | Real Rank of Karchmer-Wigderson Communication Matrices for AC⁰ PA |
| 2026-04-30 17:44 UTC | `INCONCLUSIVE` | Free Entropy Distinguishes Read-Twice BPs from IP_2 Trivial Ones |
| 2026-04-30 17:57 UTC | `INCONCLUSIVE` | Phase Cell Count Bounded by Tropical Proof Rank |
| 2026-04-30 18:22 UTC | `INCONCLUSIVE` | Orbit Closure Dimension vs. Circuit Complexity for Permanent |
| 2026-04-30 18:56 UTC | `INCONCLUSIVE` | Real Algebraic Components of AC⁰ PARITY Circuits |
| 2026-04-30 19:25 UTC | `INCONCLUSIVE` | Non-Commutative Rank of ACC^0 Circuits Bounded by Logarithmic Dep |
| 2026-04-30 20:31 UTC | `INCONCLUSIVE` | Fourier Coefficient Sparsity and Deterministic Communication Comp |
| 2026-04-30 20:59 UTC | `INCONCLUSIVE` | Monomial Count in KW Polynomial Bounds Communication Complexity |
| 2026-04-30 21:28 UTC | `INCONCLUSIVE` | Real Rank of SOS Moment Matrices for Max-CUT |
| 2026-04-30 22:03 UTC | `INCONCLUSIVE` | Slice Rank Lower Bounds for Communication Complexity of CNF Formu |
| 2026-04-30 22:29 UTC | `FALSIFIED` | Duality-Preserved Phase Cell Bound |
| 2026-04-30 23:07 UTC | `INCONCLUSIVE` | Algebraic Geometry over Finite Fields and EF Proof Length |
| 2026-04-30 23:42 UTC | `INCONCLUSIVE` | Additive Energy Bounds for SOS Refutations of Sipser Functions |

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