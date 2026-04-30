---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-30 04:40 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-04-30 04:40 UTC

- Cycles recorded: **236**
- Time span: 151.0h (~1.56 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 212 |
| FALSIFIED | 14 |
| BARRIER_HIT | 6 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
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

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-04-29 05:58 UTC | `INCONCLUSIVE` | Submodular Matroid Rank Defect for Monotone CLIQUE |
| 2026-04-29 06:32 UTC | `INCONCLUSIVE` | SOS Integrality Gap and Secant Variety Dimension for Polynomial C |
| 2026-04-29 07:23 UTC | `INCONCLUSIVE` | Protocol-Induced Covers on Tensor-Powered Girth Gadgets Exhibit L |
| 2026-04-29 07:53 UTC | `INCONCLUSIVE` | Real Rank Lower Bound for ACC^0 Circuit Size |
| 2026-04-29 08:50 UTC | `INCONCLUSIVE` | Free Entropy Lower Bound for Disjointness Communication Matrices |
| 2026-04-29 10:34 UTC | `INCONCLUSIVE` | Roe-Cover Multiplicity Lower Bound from Asymptotic Dimension Grow |
| 2026-04-29 10:45 UTC | `INCONCLUSIVE` | Additive Energy of Sipser Function Bounds ACC⁰ Circuit Size |
| 2026-04-29 13:06 UTC | `INCONCLUSIVE` | Protocol-Induced Covers on High-Asdim Gadget Lifts Require Expone |
| 2026-04-29 15:43 UTC | `INCONCLUSIVE` | Free Entropy Gap in Read-Twice Branching Programs for IP_2 |
| 2026-04-29 18:05 UTC | `INCONCLUSIVE` | Protocol-Induced Covers from Low-Cost Protocols on High-Distortio |
| 2026-04-29 21:06 UTC | `INCONCLUSIVE` | Spectral Radius of Vertex Contraction Graph Controls Tseitin Reso |
| 2026-04-29 23:34 UTC | `BARRIER_HIT` | Tropical Circuit Weight Accumulation Bound |
| 2026-04-29 23:43 UTC | `INCONCLUSIVE` | Star Discrepancy of Clause-Vectors Lower-Bounds Resolution Width  |
| 2026-04-30 02:07 UTC | `INCONCLUSIVE` | Kolmogorov Complexity of Shortest Resolution Refutations Bounded  |
| 2026-04-30 04:40 UTC | `INCONCLUSIVE` | EF Refutation Size vs. Clause-Indicator Complexity |

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