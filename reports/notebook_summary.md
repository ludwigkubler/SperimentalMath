---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-10 11:43 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-10 11:43 UTC

- Cycles recorded: **541**
- Time span: 398.1h (~1.36 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 506 |
| BARRIER_HIT | 16 |
| FALSIFIED | 15 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 29 |
| Free Probability | 14 |
| Schur-Weyl Duality | 12 |
| Representation Theory of Symmetric Groups | 12 |
| Matroid Theory | 10 |
| Algebraic Geometry | 7 |
| Additive Combinatorics | 7 |
| Polymatroid Theory | 7 |
| Random Matrix Theory | 6 |
| Finite Geometry | 6 |
| Spectral Graph Theory | 6 |
| Plethysm Theory | 6 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Noncommutative L^p Geometry | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| FOURIER_ANALYSIS | 4 |
| Fourier analysis of boolean functions | 3 |
| Algebraic Topology | 3 |
| matroid theory | 3 |
| Coarse Geometric Lifting (CGL) — Geometric Complexity Theory | 3 |
| {"framework_name": "Tropical Circuit Weight Analysis (TCWA)", "math_branch": "BOUNDED_ARITHMETIC"} | 3 |
| Tropical Circuit Weight Analysis (BOUNDED_ARITHMETIC) | 3 |
| Schur-Weyl duality | 3 |
| Persistent Homology | 3 |
| Noncommutative Geometry | 3 |
| Noncommutative geometry | 2 |
| Representation theory of symmetric groups | 2 |
| Ergodic Circuit Framework (COMM_COMPLEXITY) | 2 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-10 07:07 UTC | `INCONCLUSIVE` | Additive Energy Lower Bound via Read-Twice Branching Program Disc |
| 2026-05-10 07:15 UTC | `INCONCLUSIVE` | Real Root Count Exponential in AC⁰ PARITY Circuits |
| 2026-05-10 07:36 UTC | `INCONCLUSIVE` | Polymatroid Rank Lower Bound for Monotone CLIQUE |
| 2026-05-10 07:48 UTC | `INCONCLUSIVE` | Modular Character Degree Gap in Permanent vs Determinant Circuits |
| 2026-05-10 08:11 UTC | `INCONCLUSIVE` | Class Number Inverse Proportional to Resolution Length in 3-SAT |
| 2026-05-10 08:23 UTC | `INCONCLUSIVE` | BIBD Incidence Matrix ACC⁰ Circuit Size Lower Bound |
| 2026-05-10 09:07 UTC | `INCONCLUSIVE` | Minimal Incidence Count Inverse Proportional to Disjointness Comm |
| 2026-05-10 09:21 UTC | `INCONCLUSIVE` | Standard Young Tableau Count Exponential Gap in Symmetric Power D |
| 2026-05-10 09:36 UTC | `INCONCLUSIVE` | Symmetric Group Orbit Count Invariant for AC⁰ PARITY Circuits |
| 2026-05-10 09:46 UTC | `INCONCLUSIVE` | Free Entropy Distinguishes Read-Twice BPs from IP_2 Trivial Ones |
| 2026-05-10 09:56 UTC | `INCONCLUSIVE` | Association Scheme Eigenvalue Inverse Proportional to ACC^0 Circu |
| 2026-05-10 10:35 UTC | `INCONCLUSIVE` | Schatten p-Norm Lower Bound for Disjointness Communication Matric |
| 2026-05-10 11:14 UTC | `INCONCLUSIVE` | Free Entropy Gap in Read-Twice Branching Programs for IP_2 |
| 2026-05-10 11:23 UTC | `INCONCLUSIVE` | Non-Commutative Fourier L1 Norm Distinguishes Read-Twice from Rea |
| 2026-05-10 11:43 UTC | `INCONCLUSIVE` | Automorphism Group Generator Count Bounded by ABP Width for Symme |

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