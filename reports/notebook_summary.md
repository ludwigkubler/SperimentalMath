---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-27 13:17 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-27 13:17 UTC

- Cycles recorded: **150**
- Time span: 87.6h (~1.71 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 131 |
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
| 2026-04-27 07:15 UTC | `INCONCLUSIVE` | Sandpile-Group Order of Lifted IP Bipartite Graph Bounds Decision |
| 2026-04-27 07:44 UTC | `INCONCLUSIVE` | Doob Martingale Variance Gap Predicts Worst-Case DPLL Depth |
| 2026-04-27 08:18 UTC | `INCONCLUSIVE` | Newton-Inequality Defect of SAT Generating Polynomial Bounds DPLL |
| 2026-04-27 08:47 UTC | `INCONCLUSIVE` | Möbius Function of Minterm Lattice Bounds Indexing-Lifted Communi |
| 2026-04-27 09:18 UTC | `INCONCLUSIVE` | Noise-Stability Plateau at rho=1/3 Bounds DPLL Leaves on 3-CNF |
| 2026-04-27 09:53 UTC | `INCONCLUSIVE` | Brooks Quasimorphism Magnitude Lower-Bounds Formula Depth via Bar |
| 2026-04-27 10:22 UTC | `INCONCLUSIVE` | Hadamard-Code Distance Defect Predicts NW-PRG Distinguisher Advan |
| 2026-04-27 10:37 UTC | `INCONCLUSIVE` | Asymptotic-dimension lower bound for the indexing function via co |
| 2026-04-27 10:47 UTC | `INCONCLUSIVE` | Permanent of Sensitive-Boundary Bipartite Matrix Bounds Lifted In |
| 2026-04-27 11:13 UTC | `INCONCLUSIVE` | Subdeterminant Dispersion Lower-Bounds Singular-Tail Matrix Rigid |
| 2026-04-27 11:46 UTC | `INCONCLUSIVE` | Lyndon Factor Count of Truth Table Lower-Bounds DT Leaves Under I |
| 2026-04-27 12:12 UTC | `INCONCLUSIVE` | Kashin-Split Energy Gap Lower-Bounds Sign-Matrix Rigidity at Rank |
| 2026-04-27 12:41 UTC | `INCONCLUSIVE` | Roe-trace pairing for Inner-Product realizes coarse depth κ ≥ log |
| 2026-04-27 12:47 UTC | `INCONCLUSIVE` | Cubical Betti Sum of Implicant Complex Lower-Bounds DNF-MCSP |
| 2026-04-27 13:16 UTC | `INCONCLUSIVE` | Zeckendorf Length of NW Design Rows Bounds PRG Parity Bias |

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