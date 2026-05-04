---
title: "SEC P vs NP — Frameworks (live)"
author: "SEC (autonomous) — attributed to Ludovico Kubler"
date: "2026-05-04 21:30 UTC"
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
sansfont: "DejaVu Sans"
mathfont: "Latin Modern Math"
geometry: "margin=2cm"
fontsize: 10pt
colorlinks: true
---

# SEC P vs NP — Frameworks (live)

Compiled 2026-05-04 21:30 UTC. Tracking 5 active + 0 dead frameworks.

## Summary table

| Framework ID | Status | Fitness | Generation | Parent | Name |
|--------------|--------|---------|-----------:|--------|------|
| `fw_b9e7d103d0` | ELABORATING | 0.000 | 0 | `-` | Ergodic Circuit Framework |
| `fw_28b4bfb95f` | ELABORATING | 0.000 | 0 | `-` | TROPICAL_FOURIER_ANALYSIS |
| `fw_85a254b4a0` | ELABORATING | 0.000 | 0 | `-` | Coarse Geometric Karchmer-Wigderson (CG-KW) |
| `fw_6997a27304` | ELABORATING | 0.000 | 0 | `-` | Coarse Geometric Lifting (CGL) |
| `fw_a1a152ae17` | ELABORATING | 0.000 | 0 | `-` | Tropical Circuit Weight Analysis (TCWA) |

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

---

### Coarse Geometric Karchmer-Wigderson (CG-KW) (`fw_85a254b4a0`)

- **Status**: `ELABORATING`
- **Fitness**: 0.000
- **Taxonomy**: KARCHMER_WIGDERSON
- **Target invariant**: Coarse depth κ(f) (non-negative real) → bounds κ(f) := sup over nontrivial c ∈ HX^1(X_f) and T ∈ C_u^*[X_f] of log|⟨c,T⟩| / log(propagation(T)). The conjecture is depth(f) ≥ κ(f), so a super-logarithmic κ(f) for an explicit f gives a super-logarithmic formula-depth lower bound (a P ⊄ NC^1 separation if κ is poly-large).

**Primitives**:
- `KW-metric space` (finite metric space (X_f, d_f) with X_f = f^{-1}(0) ⊔ f^{-1}(1)): For a boolean function f:{0,1}^n -> {0,1}, define d_f(x,y) = log_2(min number of coordinates a depth-bounded distinguisher must read to certify f(x) ≠
- `Controlled cover` (finite family U = {U_i ⊂ X_f} with diameter bound R): A cover whose parts have d_f-diameter at most R and whose overlap multiplicity is at most m. Encoded as a hypergraph H_U (vertices = X_f, edges = U_i)
- `Coarse cocycle` (function c : X_f × X_f -> Z with finite support modulo controlled equivalence): A discrete 1-cochain in the Roe-style coarse cohomology HX^*(X_f) restricted to the KW pair structure. Stored as a sparse table on pairs (x,y) with d_
- `Asymptotic-dimension witness` (vertex coloring χ : X_f -> [k] together with diameter bound R): Witnesses asdim(X_f) ≤ k-1 in the sense of Gromov: each color class decomposes into d_f-bounded pieces of diameter ≤ R that are pairwise R-disjoint. C
- `Roe-controlled operator` (matrix T ∈ R^{X_f × X_f} with T_{x,y} = 0 whenever d_f(x,y) > R): Element of the algebraic uniform Roe algebra C_u^*[X_f]. Stored as a banded sparse matrix in the d_f-metric; multiplication, adjoint, and trace are al

**Tentative axioms**:
- A1 (Coarse-KW link): formula depth d(f) ≥ Ω(log(asdim(X_f))) and more strongly d(f) ≥ Ω(κ(f)); proved by translating a KW protocol into a controlled cover whose multiplicity exponent equals depth.
- A2 (Composition sub-additivity): asdim(X_{f∘g}) ≥ asdim(X_f) + asdim(X_g) − O(1), giving a KRW-style direct-sum theorem at the level of coarse dimension.
- A3 (Anti-natural-proofs): for a uniformly random f, HX^1(X_f) is generically zero (Roe-algebraic concentration of measure), so κ is NOT a 'largeness' property in the Razborov-Rudich sense — random f's
- A4 (Anti-relativization): κ is a metric invariant of d_f and is destroyed by oracle access (oracle gates collapse d_f to ≤ 1), so κ-based bounds cannot relativize, in the spirit of Mendel-Naor metric 
- A5 (Roe-index rigidity): nontrivial classes in HX^1(X_f) detected by the Roe-trace pairing are stable under coarse equivalence, mirroring Yu's coarse Baum-Connes results (Yu 2000; Nowak-Yu 2012); expl

---

### Coarse Geometric Lifting (CGL) (`fw_6997a27304`)

- **Status**: `ELABORATING`
- **Fitness**: 0.000
- **Taxonomy**: LIFTING
- **Target invariant**: CoarseLiftingComplexity (CLC) (ℕ-valued function of (f, G)) → bounds The deterministic 2-party communication complexity of f∘G^n. Specifically: CC(f∘G^n) ≥ Q(f) · log_2(asdim_R(G)+1) for the gadget scale R = diam(G), with the goal of recovering and surpassing known query-to-communication lifting bounds (Raz–McKenzie, Göös–Pitassi–Watson) for gadgets where positive asymptotic dimension can be certified.

**Primitives**:
- `MetricGadget` ((X: FiniteSet, Y: FiniteSet, g: X×Y → {0,1}, d: (X×Y)² → ℝ≥0)): A boolean gadget g equipped with a graph/Hamming metric d on X×Y. Implementable as a tuple of two finite sets, a truth-table for g, and a precomputed 
- `LiftedInputSpace` (((X×Y)^n, d_⊕)): The n-fold product of a MetricGadget under the ℓ¹ (Hamming-sum) product metric d_⊕((u_i),(v_i)) = Σ d(u_i, v_i). Implementable as a generator over tup
- `RoeCover` (List[Subset((X×Y)^n)] with multiplicity m and scale R): A finite cover of the lifted input space whose members have d_⊕-diameter ≤ R and any point is in ≤ m members. This is the discrete witness used in the
- `ProtocolPullback` (Dict[transcript → Subset((X×Y)^n)]): The partition of inputs induced by transcripts of a (deterministic or randomized) communication protocol Π, viewed as a candidate RoeCover. Implementa
- `FolnerWitness` (Sequence[Subset((X×Y)^n)]): A nested family F_1 ⊂ F_2 ⊂ ... with |∂_R F_k|/|F_k| → 0 for each scale R, certifying amenability/Property A of the lifted space relative to a gadget.

**Tentative axioms**:
- A1 (Coarse-Lift Functoriality): If two gadgets G_1, G_2 are coarsely equivalent (a bi-Lipschitz bijection up to bounded error), then CLC(f, G_1) = Θ(CLC(f, G_2)) for every f.
- A2 (Protocol → Cover): Every deterministic protocol Π for f∘G^n of cost c yields a RoeCover with multiplicity ≤ 2^c and bounded scale R_Π depending only on G; hence CC(f∘G^n) ≥ log_2 (min multiplicity
- A3 (Asdim Amplification): asdim(G_1 ⊗ G_2) ≥ asdim(G_1) + asdim(G_2) − O(1), so iterated tensoring of a single 'good' gadget produces unbounded coarse dimension.
- A4 (Property-A Transfer): If G has Property A and f has query complexity Q(f), then CLC(f, G) ≥ Q(f) · h(G) where h(G) is the Hilbert-space compression exponent of G — a non-natural, non-relativizing 
- A5 (Non-Algebrization): The Roe algebra C*_R((X×Y)^n) is not closed under polynomial extensions of the gadget alphabet; therefore lower bounds derived from its K-theory do not algebrize.

---

### Tropical Circuit Weight Analysis (TCWA) (`fw_a1a152ae17`)

- **Status**: `ELABORATING`
- **Fitness**: 0.000
- **Taxonomy**: BOUNDED_ARITHMETIC
- **Target invariant**: Tropical Proof Rank (integer) → bounds The minimum number of phase transitions required to simulate a bounded arithmetic proof line in V⁰ or IΔ₀, thereby bounding the strength of definable functions and aiming to separate bounded arithmetic theories via circuit phase complexity.

**Primitives**:
- `Tropical Circuit` (tuple (G, w)): A directed acyclic graph G with nodes labeled as inputs (variables or constants), tropical addition (min or max), or tropical multiplication (usual ad
- `Tropical Derivation` (function δ: Circuit → Circuit): A formal derivative operator on tropical circuits: for a node computing min(x,y), the derivation selects the active operand (argmin) with tie-breaking
- `Weight Profile` (list of integers): For a tropical circuit C and input x ∈ ℤⁿ, the weight profile is the sequence of edge weights traversed during evaluation under tropical semantics, or
- `Circuit Phase Space` (subset of ℝⁿ): Partition of input space ℝⁿ into convex polyhedral regions where the tropical circuit's active computation path (i.e., argmin/argmax decisions) remain

**Tentative axioms**:
- A1: (Phase Stability Axiom) Any function provably total in IΔ₀ has a tropical circuit with polynomially many phase cells under uniform input scaling.
- A2: (Weight-Proof Correspondence) The sum of absolute weights in a tropical circuit for a formula encoding a proof line is at least the bit-complexity of the cut-free proof in bounded arithmetic.
- A3: (Tropical Soundness) If a bounded arithmetic theory proves a ∀Σ₁ᵇ sentence, then its tropical circuit model exhibits a homotopy-stable phase space under perturbation.