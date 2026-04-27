---
title: "SEC P vs NP — Frameworks (live)"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-04-27 01:38 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — Frameworks (live)

Compiled 2026-04-27 01:38 UTC. Tracking 2 active + 0 dead frameworks.

## Summary table

| Framework ID | Status | Fitness | Generation | Parent | Name |
|--------------|--------|---------|-----------:|--------|------|
| `fw_b9e7d103d0` | ELABORATING | 0.000 | 0 | `-` | Ergodic Circuit Framework |
| `fw_28b4bfb95f` | ELABORATING | 0.000 | 0 | `-` | TROPICAL_FOURIER_ANALYSIS |

## Details

---

### Ergodic Circuit Framework (`fw_b9e7d103d0`)

- **Status**: `ELABORATING`
- **Fitness**: 0.000
- **Taxonomy**: COMM_COMPLEXITY
- **Target invariant**: communication_entropy_barrier (real number ≥ 0) → bounds The minimum communication complexity in a k-party number-on-forehead model, where lower bounds are derived from the growth rate of Kolmogorov-Sinai entropy in associated dynamical circuits. Aims to prove ω(log n) lower bounds for explicit functions like Disjointness, avoiding natural proofs via non-uniform dynamics.

**Primitives**:
- `measurable_dynamical_circuit` (tuple (C, X, μ, T)): A Boolean circuit C where gates are labeled by operations over a probability space (X, μ), and T: X → X is a measure-preserving transformation represe
- `orbit_signature` (function: N → [0,1]): For a fixed input x ∈ {0,1}^n, the orbit signature is the sequence (μ(C(T^k(x))))_k, capturing how the circuit's output evolves under repeated applica
- `cross_correlation_flow` (matrix ∈ R^{d×d}): For a depth-d circuit, this matrix F_{i,j} = ∫ |C_i(x) - C_i(T^j(x))|^2 dμ(x) measures how perturbations via T propagate through layers. Computable vi

**Tentative axioms**:
- A1: Any circuit with o(n) communication complexity induces a dynamical system with sublinear Kolmogorov-Sinai entropy growth.
- A2: Measure-preserving transformations corresponding to AC⁰ circuits have bounded mixing time, while those for PSPACE-complete computations exhibit super-polynomial mixer-profile decay.
- A3: If a family of circuits computes a function with high cross_correlation_flow norm, then its communication complexity is Ω(n^δ) for some δ > 0.

---

### TROPICAL_FOURIER_ANALYSIS (`fw_28b4bfb95f`)

- **Status**: `ELABORATING`
- **Fitness**: 0.000
- **Taxonomy**: FOURIER_ANALYTIC
- **Target invariant**: MinimalFourierCoefficient (RealNumber) → bounds The discrepancy of a function under tropical Fourier analysis.

**Primitives**:
- `TropicalPolynomial` (Function): A function defined over a tropical semiring (max-plus or min-plus) with computable coefficients.
- `TropicalFourierTransform` (Transformation): A mapping from tropical polynomials to their Fourier coefficients over a tropical semiring.
- `DiscrepancyMeasure` (Metric): A function quantifying the deviation of a tropical polynomial from uniformity.

**Tentative axioms**:
- A1: TropicalConvolution preserves the tropical semiring structure under composition.
- A2: TropicalFourierTransform is invertible when restricted to certain tropical polynomials.
- A3: DiscrepancyMeasure is bounded by the maximum absolute value of Fourier coefficients.