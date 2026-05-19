---
title: "SEC P vs NP — notebook summary"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-19 17:34 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — notebook summary

Generated 2026-05-19 17:34 UTC

- Cycles recorded: **884**
- Time span: 619.9h (~1.43 cycles/h)
- Notebook: `/home/ludo/Scrivania/SEC/research/pvsnp_notebook.jsonl`

## Verdict distribution

| Verdict | Count |
|---|---|
| INCONCLUSIVE | 842 |
| BARRIER_HIT | 22 |
| FALSIFIED | 16 |
| SUPPORTED | 4 |

## Mathematical fields explored (field_A)

| Field | Cycles |
|---|---|
| Real Algebraic Geometry | 43 |
| Schur-Weyl Duality | 33 |
| Matroid Theory | 20 |
| Free Probability Theory | 19 |
| Free Probability | 18 |
| Representation Theory of Symmetric Groups | 18 |
| Additive Combinatorics | 14 |
| Noncommutative L^p Geometry | 12 |
| Spectral Graph Theory | 10 |
| REAL_ALGEBRAIC_GEOMETRY | 9 |
| Random Matrix Theory | 8 |
| Polymatroid Theory | 8 |
| Algebraic Geometry | 7 |
| Finite Geometry | 6 |
| Schur-Weyl duality | 6 |
| Persistent Homology | 6 |
| Noncommutative Harmonic Analysis | 6 |
| Plethysm Theory | 6 |
| FOURIER_ANALYSIS | 5 |
| Ergodic Circuit Framework (communication complexity via dynamical systems) | 4 |
| {"framework_name": "Ergodic Circuit Framework", "math_branch": "COMM_COMPLEXITY"} | 4 |
| Algebraic Topology | 4 |
| Fourier Analysis on Boolean Functions | 4 |
| Algebraic Geometry over Finite Fields | 4 |
| Fourier Analysis of Boolean Functions | 4 |
| Algebraic Geometry of Secant Varieties | 4 |
| COMMUNICATION_COMPLEXITY | 4 |
| Noncommutative Geometry | 4 |
| Fourier analysis of boolean functions | 3 |
| Algebraic geometry of secant varieties | 3 |

## Last 15 cycles (chronological)

| Time | Verdict | Title |
|---|---|---|
| 2026-05-19 13:55 UTC | `INCONCLUSIVE` | Additive Energy Inverse Proportionality to Karchmer-Wigderson Com |
| 2026-05-19 14:14 UTC | `INCONCLUSIVE` | Polymatroid Rank Inverse Proportionality to SOS Refutation Size |
| 2026-05-19 14:29 UTC | `INCONCLUSIVE` | Noncommutative Fourier Coefficient Inverse Proportionality to Com |
| 2026-05-19 14:38 UTC | `INCONCLUSIVE` | Jordan Rank Lower Bound for Tseitin Resolution Width |
| 2026-05-19 14:50 UTC | `INCONCLUSIVE` | Matroid Rank Inverse Proportionality to k-CLIQUE Communication Co |
| 2026-05-19 15:23 UTC | `INCONCLUSIVE` | Real Rank Lower Bound for AC⁰ Communication Matrices of PARITY |
| 2026-05-19 15:30 UTC | `INCONCLUSIVE` | Free Entropy Gap in Read-Twice Branching Programs for Inner Produ |
| 2026-05-19 15:38 UTC | `INCONCLUSIVE` | Tensor Rank of Clause Incidence Matrix Bounds ACC^0 Circuit Size |
| 2026-05-19 15:42 UTC | `BARRIER_HIT` | Schur-Weyl Component Count Separation in 3-CNF Incidence Tensors |
| 2026-05-19 15:51 UTC | `INCONCLUSIVE` | Real Rank of SOS Moment Matrix and Max-CUT Approximation Ratio |
| 2026-05-19 16:12 UTC | `INCONCLUSIVE` | Persistent Homology Betti Numbers and Communication Complexity of |
| 2026-05-19 16:36 UTC | `INCONCLUSIVE` | Gröbner Basis Monomial Count and SAT Complexity |
| 2026-05-19 17:04 UTC | `INCONCLUSIVE` | Free Entropy Lower Bound for Disjointness Communication Complexit |
| 2026-05-19 17:21 UTC | `INCONCLUSIVE` | Schur Positivity of SOS Moment Matrices for 3-SAT |
| 2026-05-19 17:34 UTC | `INCONCLUSIVE` | Plethysm Coefficient Exponential Gap in Symmetric Powers of Perma |

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