---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-24 18:43 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-24 18:43 UTC

- Cycles recorded: **39**
- Time span: 21.0h (~1.85 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 29 |
| FALSIFIED | 7 |
| SUPPORTED | 3 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Noncommutative geometry | 2 |
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
| Hypergraph Tutte polynomials | 1 |
| Galois theory of finite field extensions | 1 |
| Combinatorial homotopy theory (unstable 2-cohomotopy) | 1 |
| Geometric group theory (Kazhdan's property T) | 1 |
| Quadratic forms over GF(2) | 1 |
| Commutative algebra (Castelnuovo-Mumford regularity) | 1 |
| Algebraic K-theory (Bass Nil-groups) | 1 |
| Arithmetic geometry (Selmer groups of elliptic curves) | 1 |
| Toric geometry (via initial ideals and monomial degenerations) | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-04-24 08:00 UTC | `INCONCLUSIVE` | Kazhdan Constant of Clause-Variable Group Action Bounds Resolutio |
| 2026-04-24 08:30 UTC | `FALSIFIED` | Clifford Algebra Signature of 2-Clause Ideal Bounds Resolution Wi |
| 2026-04-24 09:03 UTC | `INCONCLUSIVE` | Castelnuovo-Mumford Regularity of Clause-Variable Ideal Equals Re |
| 2026-04-24 09:35 UTC | `INCONCLUSIVE` | Bass Nilpotency Class of Augmented SAT Group Ring Bounded by Reso |
| 2026-04-24 10:44 UTC | `INCONCLUSIVE` | Selmer Group 2-Rank of Pythagorean Triple CNF Formula Equals Reso |
| 2026-04-24 10:50 UTC | `INCONCLUSIVE` | Toric Degeneration Polytope Volume Bounds Resolution Proof Size |
| 2026-04-24 11:21 UTC | `INCONCLUSIVE` | Clifford Algebroid Rank of SAT Dependency Graph Equals Resolution |
| 2026-04-24 11:55 UTC | `INCONCLUSIVE` | K-theory and SAT |
| 2026-04-24 13:08 UTC | `FALSIFIED` | Convex Hull Facet Count and Resolution Proof Size |
| 2026-04-24 13:38 UTC | `INCONCLUSIVE` | Quantum Dimension of Clause Algebra Bounds Communication Complexi |
| 2026-04-24 16:16 UTC | `INCONCLUSIVE` | Minimal Ideal Generators and Resolution Proof Size |
| 2026-04-24 16:30 UTC | `INCONCLUSIVE` | Vandermonde Rank of Clause-Variable Incidence Matrix Predicts Res |
| 2026-04-24 17:19 UTC | `INCONCLUSIVE` | Average Sensitivity of Clause-Indicator Function Bounds Resolutio |
| 2026-04-24 18:09 UTC | `INCONCLUSIVE` | Minimal ABP Size and Permutation Polynomial Degree |
| 2026-04-24 18:43 UTC | `INCONCLUSIVE` | Hypergraph Discrepancy and Communication Complexity of 3-SAT |

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