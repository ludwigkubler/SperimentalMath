---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-30 18:30 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-30 18:30 UTC

- Cycles recorded: **248**
- Time span: 164.8h (~1.50 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 223 |
| FALSIFIED | 14 |
| BARRIER_HIT | 7 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier analysis of boolean functions | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| Real Algebraic Geometry | 3 |
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
| Directed algebraic topology (d-space homology) | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-04-29 23:43 UTC | `INCONCLUSIVE` | Star Discrepancy of Clause-Vectors Lower-Bounds Resolution Width  |
| 2026-04-30 02:07 UTC | `INCONCLUSIVE` | Kolmogorov Complexity of Shortest Resolution Refutations Bounded  |
| 2026-04-30 04:40 UTC | `INCONCLUSIVE` | EF Refutation Size vs. Clause-Indicator Complexity |
| 2026-04-30 07:04 UTC | `INCONCLUSIVE` | Tropical Derivation Sparsity Limits Phase Cell Count |
| 2026-04-30 07:30 UTC | `INCONCLUSIVE` | Persistent Homology and Communication Complexity Lower Bounds |
| 2026-04-30 07:49 UTC | `INCONCLUSIVE` | Width-Bounded Module Dimension in Barrington's Branching Programs |
| 2026-04-30 10:09 UTC | `INCONCLUSIVE` | VC-Dimension of Row-Induced Set System Bounds Monotone DNF Size f |
| 2026-04-30 12:42 UTC | `INCONCLUSIVE` | Bounded Arithmetic Reflection Strength Lower-Bounds Resolution Re |
| 2026-04-30 15:04 UTC | `BARRIER_HIT` | Kronecker Coefficients of Rectangular GLₙ-Representations Lower-B |
| 2026-04-30 16:12 UTC | `INCONCLUSIVE` | SOS Moment Matrix Rank and Real Variety Dimension for Max-CUT |
| 2026-04-30 16:48 UTC | `INCONCLUSIVE` | Bounded Arithmetic Proof Complexity and Resolution Length |
| 2026-04-30 17:18 UTC | `INCONCLUSIVE` | Real Rank of Karchmer-Wigderson Communication Matrices for AC⁰ PA |
| 2026-04-30 17:44 UTC | `INCONCLUSIVE` | Free Entropy Distinguishes Read-Twice BPs from IP_2 Trivial Ones |
| 2026-04-30 17:57 UTC | `INCONCLUSIVE` | Phase Cell Count Bounded by Tropical Proof Rank |
| 2026-04-30 18:22 UTC | `INCONCLUSIVE` | Orbit Closure Dimension vs. Circuit Complexity for Permanent |

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