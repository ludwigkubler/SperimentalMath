---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-18 20:36 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-18 20:36 UTC

- Cycles recorded: **791**
- Time span: 598.9h (~1.32 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 751 |
| BARRIER_HIT | 20 |
| FALSIFIED | 16 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 40 |
| Schur-Weyl Duality | 28 |
| Free Probability Theory | 19 |
| Representation Theory of Symmetric Groups | 18 |
| Matroid Theory | 16 |
| Free Probability | 14 |
| Additive Combinatorics | 13 |
| Noncommutative L^p Geometry | 10 |
| Random Matrix Theory | 8 |
| Polymatroid Theory | 8 |
| Algebraic Geometry | 7 |
| Spectral Graph Theory | 7 |
| Finite Geometry | 6 |
| Plethysm Theory | 6 |
| Persistent Homology | 5 |
| Noncommutative Harmonic Analysis | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Algebraic Geometry over Finite Fields | 4 |
| Fourier Analysis of Boolean Functions | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Noncommutative Geometry | 4 |
| Fourier analysis of boolean functions | 3 |
| Algebraic Topology | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-18 10:26 UTC | `INCONCLUSIVE` | p=3 Path-Family Modulus Lower-Bounds Tseitin Tree-Resolution |
| 2026-05-18 11:02 UTC | `INCONCLUSIVE` | Viennot Heap Radius of Clause-Conflict Graph Bounds Frege Depth |
| 2026-05-18 11:29 UTC | `INCONCLUSIVE` | Lee-Yang Zero Cluster Angle of Cut Polynomial Bounds Max-Cut SoS- |
| 2026-05-18 11:55 UTC | `INCONCLUSIVE` | Additive Energy of Out-Degree Sequence Bounds ACC^0[2] MOD_3 Size |
| 2026-05-18 12:32 UTC | `INCONCLUSIVE` | SBM Detectability Gap of Literal Conflict Graph Bounds DPLL Time |
| 2026-05-18 13:00 UTC | `INCONCLUSIVE` | Fiedler Participation Entropy Lower-Bounds Tseitin Tree-Resolutio |
| 2026-05-18 13:47 UTC | `INCONCLUSIVE` | Hypercontractive Term-Pair Contraction Defect Bounds Monotone CLI |
| 2026-05-18 16:26 UTC | `INCONCLUSIVE` | Lovász-Theta of Term-Conflict Graph Bounds Monotone k-CLIQUE DNF |
| 2026-05-18 17:00 UTC | `INCONCLUSIVE` | Sidon B_2-Witness Failure of ACC⁰[2] for Sipser via MOD-Gate Outp |
| 2026-05-18 17:28 UTC | `INCONCLUSIVE` | RSK Shape Concentration Separates Permanent from Padded Determina |
| 2026-05-18 17:45 UTC | `INCONCLUSIVE` | Tusnady 2-Box Discrepancy of Clause-Polarity Cloud Bounds DPLL Si |
| 2026-05-18 18:40 UTC | `INCONCLUSIVE` | Hook-Length Dim of Tseitin T-Join Partition Lower-Bounds Tree-Res |
| 2026-05-18 19:09 UTC | `INCONCLUSIVE` | Dismantlability Core of Clause-Sharing Graph Bounds Tree-Res Size |
| 2026-05-18 19:38 UTC | `INCONCLUSIVE` | Baker-Norine ω-Gonality Lower-Bounds Tseitin DPLL Size |
| 2026-05-18 20:36 UTC | `INCONCLUSIVE` | Morse-Hedlund Factor Complexity of XOR-Lifted Rows Upper-Bounds D |

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