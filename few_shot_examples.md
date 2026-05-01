
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
- title: Lehmer Pair Density of Communication Matrix Lower-Bounds Discrepancy
- field_A × field_B: Analytic number theory (Lehmer-pair / close-zero-spacing statistics applied to i  ×  Discrepancy-based randomized communication complexity lower bounds
- statement: For a Boolean matrix M_f in {-1,+1}^{2^n x 2^n} arising from an XOR-function f:{0,1}^n -> {-1,+1}, define the Lehmer-pair density L(f) as follows: list the magnitudes |a_1| <= |a_2| <= ... of nonzero Walsh-Hadamard coefficients of f and let L(f) = #{ i : (a_{i+1}-a_i) < (a_{i+1}+a_i)/(8 log_2(1+i)) } / (#nonzero coefficients). We conjecture that for every nonconstant XOR-function f, the discrepancy disc(M_f) satisfies disc(M_f) >= c * 2^{-n/2} * (1 + L(f))^{-1}, for an absolute constant c >= 1/16, with equality up to the constant achieved by parity-like spectra and refuted by any single instan

### Example 5  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Nisan-Wigderson Seed Length Bounded by Finite Geometry Line Count
- field_A × field_B: Finite Geometry  ×  Nisan-Wigderson PRG Seed Length
- statement: For any CNF formula Φ with n variables, the seed length of the Nisan-Wigderson PRG fooling Φ is at most the number of lines in the projective plane PG(2, q) where q = 2^⌈log₂n⌉.

### Example 6  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Tropical Convolution Subadditivity of MinimalFourierCoefficient and its Discrepancy Bound
- field_A × field_B: TROPICAL_FOURIER_ANALYSIS within tropical algebra and Fourier-analytic combinato  ×  Communication complexity lower bounds via the discrepancy method (specifically, 
- statement: Let f, g: Z_n -> R be tropical polynomials with TropicalFourierTransform coefficients f_hat(k) = min_x (f(x) - (k*x mod n)/n) and analogously g_hat. Define MinimalFourierCoefficient mu(f) = min_k f_hat(k). Then for the tropical (min-plus) convolution h = f *_trop g defined by h(z) = min_{x+y=z mod n} (f(x)+g(y)), the following holds: (i) mu(h) >= mu(f) + mu(g) (subadditivity inheriting from Axiom A1's preservation of semiring structure), and (ii) DiscrepancyMeasure(h) <= 2 * max(|mu(f)|, |mu(g)|) + |mu(f) + mu(g)|, which strictly refines Axiom A3 by replacing the maximum absolute Fourier coeff

============================================================
Now propose a NEW conjecture. Different field_A. Different
statement. Same SHAPE: testable, falsifiable, ≤240s on n≤40.
============================================================