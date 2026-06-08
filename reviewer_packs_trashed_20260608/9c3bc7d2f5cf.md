---
title: "Reviewer Pack — Betti Numbers of Independence Complexes Bound Resolution Wid..."
subtitle: "Entry 9c3bc7d2f5cf · INCONCLUSIVE"
author: "SEC autonomous research engine — attribution: Ludovico Kubler"
date: "2026-04-23 21:43:56 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
header-includes:
  - \usepackage{listings}
  - \usepackage{xcolor}
  - \definecolor{codebg}{rgb}{0.96,0.96,0.96}
  - \lstset{basicstyle=\ttfamily\footnotesize,backgroundcolor=\color{codebg},breaklines=true}
---

# Betti Numbers of Independence Complexes Bound Resolution Width
**Entry ID**: `9c3bc7d2f5cf`  **Verdict**: `INCONCLUSIVE`  **Recorded**: 2026-04-23 21:43:56 UTC

## 1. Conjecture
**Field A** (mathematical branch): Combinatorial algebraic topology
**Field B** (complexity object): Resolution proof width

**Statement**:

> For every unsatisfiable 3-CNF formula F with n variables and m clauses, the total sum of reduced Betti numbers of the independence complex of its variable-clause incidence graph is at least the minimum width of any resolution refutation of F minus 1. This inequality is tight for minimally unsatisfiable formulas with connected incidence graphs.

**Rationale (proposer's reasoning)**:

> The independence complex captures higher-order dependencies among variable appearances, and its homology reflects combinatorial obstructions to satisfiability. Resolution width measures how globally the refutation must reason; high Betti numbers may signal many obstructions, forcing wide derivations. This provides a topological lower bound that is sensitive to clause-variable structure, not just counts.

## 2. Pre-registration (Popper-style)
_(no pre-registration recorded)_

## 3. Barrier filter (F1)
_(no barrier check recorded — conjecture passed without filtering or pre-V2)_

## 4. Novelty audit
**Verdict**: `NOVEL` against 15 hits across arXiv + Semantic Scholar + ECCC

**Search queries** (5):
- `"independence complex" "Betti numbers" "resolution proof width" "incidence graph" "3-CNF"`
- `"combinatorial algebraic topology" "resolution complexity" "independence complex" "Betti number bound"`
- `"reduced Betti numbers" "resolution refutation width" "variable-clause incidence graph" "unsatisfiable 3-CNF"`
- `"topological complexity" "resolution width" "independence complex" "unsatisfiable formulas"`
- `"monomial ideal" "Stanley-Reisner" "resolution width" "Betti numbers" "incidence graph 3-CNF"`

**Top relevant hits considered**:
- [http://arxiv.org/abs/1101.4831v1] The $f$--vector of the clique complex of chordal graphs and Betti numbers of edge ideals of uniform hypergraphs
- [http://arxiv.org/abs/2111.02551v4] Bigraded Betti numbers and Generalized Persistence Diagrams
- [http://arxiv.org/abs/math/0001101v4] Integrality of L2-Betti numbers
- [http://arxiv.org/abs/2208.13438v3] Intermediate Ricci curvatures and Gromov's Betti number bound
- [http://arxiv.org/abs/2501.12623v1] Betti number bounds for varieties and exponential sums
- [http://arxiv.org/abs/2004.13281v2] Independence complexes of hypergraphs and bounded degree complexes
- [http://arxiv.org/abs/2411.14268v1] Supercritical Tradeoffs for Monotone Circuits
- [http://arxiv.org/abs/2601.12503v3] Hard Clique Formulas for Resolution

## 5. Empirical test harness
**Multi-seed protocol**: 5 seeds (11, 23, 37, 53, 71)  
**Sandbox**: isolated subprocess, stdlib-only, ≤90s wall time per cycle
**Execution**: rc=-1, elapsed=0.0s

## 6. Per-seed results

_(no seed-level data — test crashed before producing TRIAL: lines)_

## 7. Test stdout (last 2KB)

```
(empty)
```

## 8. Critic adversarial review
**Critic verdict**: ``

## 9. Final verdict & safety rail
**Verdict**: `INCONCLUSIVE`

**Reasoning**:

> test_code_gen_failed

## 11. Audit log (LLM calls)

_(no audit log file — pre-Fase-A cycle)_

## 12. Reproducibility
To reproduce this cycle:

1. Apply the test harness in section 5.1 with seeds 11,23,37,53,71
2. The Python sandbox is pure-stdlib; any Python 3.11+ should suffice
3. The full LLM transcripts are in `research/audit/9c3bc7d2f5cf.jsonl` for verification of provenance
4. The pre-registration hash in section 2 commits to the test design before execution; tampering would be detectable.

**Sandbox file**: `research/pvsnp_sandbox/test_*.py` (per-cycle)  
**Replay tarball**: `research/replay/9c3bc7d2f5cf.tar.gz` (if generated)
