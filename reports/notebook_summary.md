---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-29 03:21 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-29 03:21 UTC

- Cycles recorded: **217**
- Time span: 125.7h (~1.73 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 194 |
| FALSIFIED | 14 |
| BARRIER_HIT | 5 |
| SUPPORTED | 4 |

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
| 2026-04-28 18:31 UTC | `INCONCLUSIVE` | Erdős-Rado Sunflower Petals Lower-Bound Lifted Log-Rank for IND_2 |
| 2026-04-28 19:01 UTC | `INCONCLUSIVE` | Subword Complexity of Lifted Rows Lower-Bounds Real Rank for IND_ |
| 2026-04-28 19:42 UTC | `INCONCLUSIVE` | Bakry-Émery Curvature Floor Lower-Bounds Tseitin Resolution Width |
| 2026-04-28 20:08 UTC | `INCONCLUSIVE` | Dyck Zero-Crossing Count of Row-Walks Capped by Log-Rank |
| 2026-04-28 20:35 UTC | `INCONCLUSIVE` | Cyclotomic Norm Floor of Truth-Table Character Sum Caps ACC^0[m]  |
| 2026-04-28 23:06 UTC | `INCONCLUSIVE` | Hilbert-Compression Floor on Property-A Gadgets Forces α·Q(f) Mul |
| 2026-04-28 23:09 UTC | `INCONCLUSIVE` | Effective-Resistance Diameter Lower-Bounds Tseitin Resolution Wid |
| 2026-04-29 00:11 UTC | `INCONCLUSIVE` | GF(2)-Rank Defect of Term-Indicator Matrix Lower-Bounds Monotone  |
| 2026-04-29 00:24 UTC | `INCONCLUSIVE` | Coarse-Equivalence Invariance of Protocol-Pullback Multiplicity A |
| 2026-04-29 00:40 UTC | `INCONCLUSIVE` | Persistent H_0 Component Count of Sign-Quotient Row Set Caps Real |
| 2026-04-29 01:14 UTC | `INCONCLUSIVE` | Secant Rank Lower Bound for Disjointness Communication Matrices |
| 2026-04-29 01:46 UTC | `INCONCLUSIVE` | Sign-Rank Distinguishing Tensor for Read-Twice Branching Programs |
| 2026-04-29 02:17 UTC | `INCONCLUSIVE` | SOS Hierarchy Integrality Gap for Random CSPs |
| 2026-04-29 02:49 UTC | `INCONCLUSIVE` | Hardness of MCSP Under Parameterized Circuit Classes |
| 2026-04-29 03:21 UTC | `INCONCLUSIVE` | Monotone CLIQUE Lower Bound via GF(2) Rank Defect |

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