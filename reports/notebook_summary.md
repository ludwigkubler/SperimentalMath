---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-03 09:30 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-03 09:30 UTC

- Cycles recorded: **292**
- Time span: 227.8h (~1.28 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 263 |
| FALSIFIED | 15 |
| BARRIER_HIT | 10 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 8 |
| Algebraic Geometry | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Matroid Theory | 4 |
| Fourier analysis of boolean functions | 3 |
| Random Matrix Theory | 3 |
| Additive Combinatorics | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl Duality | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |
| Algebraic Topology | 2 |
| Tropical geometry | 2 |
| Finite Geometry | 2 |
| matroid theory | 2 |
| Free Probability Theory | 2 |
| Tropical Circuit Weight Analysis (TCWA) — Bounded Arithmetic | 2 |
| Bounded Arithmetic | 2 |
| Geometric Complexity Theory | 2 |
| Schur-Weyl duality | 2 |
| Noncommutative L^p Geometry | 2 |
| Tropical Circuit Weight Analysis (TCWA) in BOUNDED_ARITHMETIC | 2 |
| Combinatorial homotopy theory | 1 |
| Kazhdan-Lusztig theory of Hecke algebras | 1 |
| Combinatorial algebraic topology | 1 |
| Knot theory (quantum invariants) | 1 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-01 09:26 UTC | `INCONCLUSIVE` | Matroid Girth of Monotone DNF Implies k-CLIQUE Circuit Size Lower |
| 2026-05-01 09:35 UTC | `INCONCLUSIVE` | Phase Merging Additivity in Tropical Proof Rank |
| 2026-05-01 09:55 UTC | `INCONCLUSIVE` | Spectral Gap Lower Bounds for Tseitin Resolution Length |
| 2026-05-01 10:34 UTC | `INCONCLUSIVE` | Permutation Polynomial Degree Bounds ABP Size for NC¹ Functions |
| 2026-05-01 11:29 UTC | `INCONCLUSIVE` | SOS Moment Matrix Rank and Max-CUT Approximation Ratio |
| 2026-05-01 12:03 UTC | `INCONCLUSIVE` | Schur-Weyl Multiplicity Gap in Permanent vs Determinant Tensor Po |
| 2026-05-01 13:05 UTC | `INCONCLUSIVE` | Multiplicity of Symmetric Powers in Permanent Tensor Decompositio |
| 2026-05-01 14:32 UTC | `INCONCLUSIVE` | Diophantine Solution Count Bounds Resolution Length in 3-SAT |
| 2026-05-01 15:02 UTC | `INCONCLUSIVE` | Singular Locus Dimension Bounds SOS Refutation Size for 3-SAT |
| 2026-05-01 16:11 UTC | `INCONCLUSIVE` | Expander Modulus Bounds Tseitin Proof Complexity |
| 2026-05-01 16:36 UTC | `INCONCLUSIVE` | Tropical Circuit Weight Profile Complexity Bound |
| 2026-05-01 16:47 UTC | `INCONCLUSIVE` | Finite Geometry Rank and ACC^0 Circuit Size for 3-SAT Instances |
| 2026-05-01 17:19 UTC | `BARRIER_HIT` | Moment Matrix Eigenvalue Gap and SOS Degree for Max-CUT |
| 2026-05-01 18:20 UTC | `INCONCLUSIVE` | Additive Energy Threshold and ACC⁰ Circuit Size |
| 2026-05-01 19:17 UTC | `INCONCLUSIVE` | Tropical Derivation Depth Reflects Proof Rank in Bounded Arithmet |

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