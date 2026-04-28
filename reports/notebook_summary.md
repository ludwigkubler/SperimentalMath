---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-28 15:27 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-28 15:27 UTC

- Cycles recorded: **197**
- Time span: 113.8h (~1.73 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 174 |
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
| 2026-04-28 09:45 UTC | `INCONCLUSIVE` | Plünnecke-Ruzsa Doubling of Constraint Vectors Lower-Bounds SoS D |
| 2026-04-28 10:22 UTC | `INCONCLUSIVE` | Kolmogorov Width of Lifted Functions Bounds MA^cc |
| 2026-04-28 10:39 UTC | `INCONCLUSIVE` | Tensor-Amplified Asdim Forces Linear Communication Blow-up on Inn |
| 2026-04-28 10:48 UTC | `INCONCLUSIVE` | Möbius Defect of NW Design Lattice Bounds Parity Bias |
| 2026-04-28 11:19 UTC | `INCONCLUSIVE` | Sandpile-Group Order of Certificate Conflict Graph Lower-Bounds Q |
| 2026-04-28 11:47 UTC | `INCONCLUSIVE` | Stanley-Reisner Projective Dimension Lower-Bounds Monotone-KW Dep |
| 2026-04-28 12:19 UTC | `INCONCLUSIVE` | Lie-Stabilizer Dimension of Clause Cubic Bounds DPLL Leaves |
| 2026-04-28 12:42 UTC | `INCONCLUSIVE` | Følner-Defect Floor Forces Logarithmic Communication Overhead on  |
| 2026-04-28 12:48 UTC | `INCONCLUSIVE` | Bipartite Token-Sliding Diameter Lower-Bounds Monotone-KW Depth |
| 2026-04-28 13:27 UTC | `INCONCLUSIVE` | Magnus Level-2 Defect Bounds DNF_min via Truth-Table Inversions |
| 2026-04-28 13:54 UTC | `INCONCLUSIVE` | Monomer-Dimer Entropy Lower-Bounds Tseitin Resolution Width |
| 2026-04-28 14:25 UTC | `INCONCLUSIVE` | Sprague-Grundy Game Value of CNF Bounds Tree-Frege Lines |
| 2026-04-28 14:45 UTC | `INCONCLUSIVE` | Roe-Skeleton Spectral Gap Forces Multiplicity in Protocol-Induced |
| 2026-04-28 14:54 UTC | `INCONCLUSIVE` | Walsh-Code Antichain Width of NW Designs Bounds PRG Linear Bias |
| 2026-04-28 15:27 UTC | `INCONCLUSIVE` | Kruskal-Katona Shadow Defect Lower-Bounds Monotone-KW Depth |

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