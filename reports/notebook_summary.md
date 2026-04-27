---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-27 19:45 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-27 19:45 UTC

- Cycles recorded: **167**
- Time span: 94.1h (~1.77 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 148 |
| FALSIFIED | 14 |
| SUPPORTED | 4 |
| BARRIER_HIT | 1 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier analysis of boolean functions | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Matroid Theory | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Random Matrix Theory | 2 |
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
| Motivic integration (Denef-Loeser zeta functions) | 1 |
| Matroid theory (Clifford index of binary matroids) | 1 |
| Representation theory of finite groups (Frobenius-Schur indicator) | 1 |
| Categorification and knot Floer homology | 1 |
| Modular forms | 1 |
| Algebraic geometry (ideals in polynomial rings) | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-04-27 14:43 UTC | `INCONCLUSIVE` | Roe-cohomological concentration: HX^1(X_f) vanishes for random f, |
| 2026-04-27 14:50 UTC | `INCONCLUSIVE` | Antichain-Width of Query Certificate Poset Bounds Lifted IND CC |
| 2026-04-27 15:25 UTC | `INCONCLUSIVE` | Apolar Span of Clause-Product Polynomial Bounds DPLL Leaves |
| 2026-04-27 15:55 UTC | `INCONCLUSIVE` | Cheeger Constant of Quotient Multigraph Bounds Tseitin Resolution |
| 2026-04-27 16:27 UTC | `INCONCLUSIVE` | RSK Second-Row Length of f-Sorted Permutation Bounds Lifted IND C |
| 2026-04-27 16:44 UTC | `INCONCLUSIVE` | Coarse-dimensional KRW direct sum: asdim is sub-additive under bl |
| 2026-04-27 16:59 UTC | `INCONCLUSIVE` | Fourier Variance Ratio of Violated-Clause Counter Bounds Tree-Res |
| 2026-04-27 17:25 UTC | `INCONCLUSIVE` | Frobenius Trace Defect of Clause-Indicator Polynomial Lower-Bound |
| 2026-04-27 17:34 UTC | `INCONCLUSIVE` | Oracle Collapse of κ: Anti-Relativization Stress Test for the Coa |
| 2026-04-27 17:36 UTC | `INCONCLUSIVE` | Carries-Polynomial Degree Lower-Bounds EF-Lines for PHP_n |
| 2026-04-27 18:10 UTC | `INCONCLUSIVE` | Sharply-Bounded Refutability Vanishes at 3-SAT Threshold |
| 2026-04-27 18:40 UTC | `INCONCLUSIVE` | Run-Length Entropy Floor Lower-Bounds DNF-MCSP Term Count |
| 2026-04-27 19:11 UTC | `INCONCLUSIVE` | Hamming-Weight Spectrum Slope Bounds ACC^0[2] Subcircuit Count |
| 2026-04-27 19:34 UTC | `INCONCLUSIVE` | Pullback monotonicity of coarse depth under coarse-Lipschitz redu |
| 2026-04-27 19:45 UTC | `INCONCLUSIVE` | Ihara Zeta Entropy Lower-Bounds DPLL Depth on 3-Regular Tseitin |

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