
============================================================
EXAMPLES OF PRIOR CONJECTURES TESTED BY THIS SYSTEM
============================================================

These are CONCRETE examples of conjectures the system has tested
in past cycles. Use them as a guide for the SHAPE of testable,
falsifiable, computationally-bounded conjectures. DO NOT propose
anything that semantically duplicates these — they are in your
blacklist by construction. Use the FORM, not the content.

### Example 1  [tier 1: FALSIFIED with Lean-verified counterexample (gold standard)]
- title: Tropical Shift-Invariance of MinimalFourierCoefficient under Additive Translation of TropicalPolynomials
- field_A × field_B: TROPICAL_FOURIER_ANALYSIS (Fourier-analytic combinatorics over the max-plus semi  ×  Circuit lower bounds for tropical (max,+) arithmetic circuits computing translat
- statement: Let f: {0,...,N-1} -> R be a TropicalPolynomial in the max-plus semiring, let TFT denote the TropicalFourierTransform, and let MFC(f) := min_{k != 0} |TFT(f)[k]| be the MinimalFourierCoefficient (excluding the DC mode k=0). For every constant c in R, define the additively-translated polynomial f_c(x) := f(x) + c (which corresponds to tropical scalar multiplication by c in the max-plus semiring). Then MFC(f_c) = MFC(f) and DiscrepancyCalculation(f_c) = DiscrepancyCalculation(f). Equivalently: the target invariant MinimalFourierCoefficient is invariant under the additive (tropical-multiplicative
- counterexample (witness of falsification): Failed MFC or Discrepancy invariance for N=16

### Example 2  [tier 1: FALSIFIED with Lean-verified counterexample (gold standard)]
- title: Tropical Self-Convolution Doubling Law for MinimalFourierCoefficient
- field_A × field_B: TROPICAL_FOURIER_ANALYSIS (Tropical Geometry intersected with Fourier-analytic m  ×  Two-party deterministic communication complexity of min-plus (tropical) convolut
- statement: Let f be a TropicalPolynomial on the cyclic group Z_n equipped with the min-plus semiring, and let g = TropicalConvolution(f, f) be its tropical self-convolution. Then (i) MinimalFourierCoefficient(g) = 2 * MinimalFourierCoefficient(f) up to an additive error of O(1/n) under the Maslov-dequantized TropicalFourierTransform, and (ii) DiscrepancyMeasure(g) <= 2 * DiscrepancyMeasure(f). As a complexity-theoretic corollary, distinguishing two tropical polynomials whose discrepancies differ by epsilon requires deterministic communication Omega(log(1/epsilon)) bits in the standard input-partition mod
- counterexample (witness of falsification): n=8,beta=5: |MinFC(g)-2*MinFC(f)|=3.78546 > C/n=0.62500

### Example 3  [tier 1: FALSIFIED with Lean-verified counterexample (gold standard)]
- title: Tropical Parseval Lower Bound on Discrepancy via Min-Coefficient Saturation
- field_A × field_B: TROPICAL_FOURIER_ANALYSIS (Tropical Geometry / Fourier Analysis over the Max-Plu  ×  Query complexity of approximating the DiscrepancyMeasure of a TropicalPolynomial
- statement: For every TropicalPolynomial f on the discrete cube {0,1,...,N-1} with computable max-plus coefficients, let F = TropicalFourierTransform(f) and let MinimalFourierCoefficient(f) = min_k F[k]. Then DiscrepancyCalculation(f) is lower-bounded by MinimalFourierCoefficient(f) and upper-bounded by max_k |F[k]| (axiom A3). Equivalently: MinimalFourierCoefficient(f) <= DiscrepancyCalculation(f) <= max_k |F[k]|, with the lower inequality saturated whenever f is a tropical convolution of two identical TropicalPolynomials (a 'tropical autoconvolution'), giving query complexity Theta(N) to certify saturat
- counterexample (witness of falsification): random poly N=8 seed=11: upper bound VIOLATED — Disc=3.776423 > max|F|=3.096445

### Example 4  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Cauchy Mean Width of Minterm Hull Lower-Bounds Monotone k-CLIQUE
- field_A × field_B: Convex geometry (Cauchy mean-width / intrinsic 1-volume of polytopes in R^N, in   ×  Karchmer–Wigderson / monotone DNF size and formula complexity for the k-CLIQUE i
- statement: For a monotone Boolean function f on N variables, let M(f) ⊂ {0,1}^N be its set of minterms (minimal satisfying assignments viewed as 0/1 vectors) and let K(f) := conv(M(f) ∪ {0}) ⊆ [0,1]^N. Define μ(f) := MW(K(f))^2, where MW(K) = 2·E_{u∼Unif(S^{N−1})}[max_{x∈K}⟨u,x⟩] is the Cauchy mean width. We conjecture: (i) for every monotone DNF representation of f with s terms, μ(f) ≤ C₁·log(s+1)·(log N+1); (ii) for the k-CLIQUE indicator on K_v with k=⌈log₂ v⌉ (so N = v(v−1)/2), μ(f) ≥ C₂·v, for absolute constants C₁,C₂>0. A single instance with μ(f) > C₁·log(s+1)(log N+1), or a k-CLIQUE indicator wit
- counterexample (witness of falsification): k-CLIQUE with v=4 has mu=1.1786757596570663 < 0.5*v=2.0

### Example 5  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Persistent H1 of Random Row Subclouds Bounds DISJ Communication
- field_A × field_B: Persistent homology / topological data analysis (Vietoris–Rips H_1 with total ba  ×  Randomized communication complexity of DISJOINTNESS (worst-case lower bound via 
- statement: Let M ∈ {0,1}^{N×N} be the communication matrix of a Boolean function (N = 2^n). For a uniformly random k-element subset S of row indices with k = ⌈√N⌉, view the rows {M[x,·] : x ∈ S} as a point cloud in {0,1}^N under Hamming distance, and let τ_PH(M;S) := Σ_{(b,d) ∈ Dgm_1(VR(S))} (d − b) denote the total persistence of the 1-dimensional bars of the Vietoris–Rips filtration of that sub-cloud, with all distances normalised by N. Conjecture: there is an absolute constant c > 0 such that for every Boolean matrix M, CC_R(M) ≥ c · log_2( 1 + E_S[τ_PH(M;S)] · k ); moreover E_S[τ_PH(M_DISJ_n;S)] = Ω(

### Example 6  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Lehmer Pair Density of Communication Matrix Lower-Bounds Discrepancy
- field_A × field_B: Analytic number theory (Lehmer-pair / close-zero-spacing statistics applied to i  ×  Discrepancy-based randomized communication complexity lower bounds
- statement: For a Boolean matrix M_f in {-1,+1}^{2^n x 2^n} arising from an XOR-function f:{0,1}^n -> {-1,+1}, define the Lehmer-pair density L(f) as follows: list the magnitudes |a_1| <= |a_2| <= ... of nonzero Walsh-Hadamard coefficients of f and let L(f) = #{ i : (a_{i+1}-a_i) < (a_{i+1}+a_i)/(8 log_2(1+i)) } / (#nonzero coefficients). We conjecture that for every nonconstant XOR-function f, the discrepancy disc(M_f) satisfies disc(M_f) >= c * 2^{-n/2} * (1 + L(f))^{-1}, for an absolute constant c >= 1/16, with equality up to the constant achieved by parity-like spectra and refuted by any single instan

============================================================
Now propose a NEW conjecture. Different field_A. Different
statement. Same SHAPE: testable, falsifiable, ≤240s on n≤40.
============================================================