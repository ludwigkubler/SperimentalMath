
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
- title: [c003b_cumulative_entropy/SC2#c49] Φ(π) >= c·|S|² for a constant c>0, where |S| is the balanced separator size (the cumulative-entropy analogue of the space lower bound that A13 needs).
- field_A × field_B: Resolution proof complexity  ×  Tseitin formulas
- statement: Φ(π) >= c·|S|² for a constant c>0, where |S| is the balanced separator size (the cumulative-entropy analogue of the space lower bound that A13 needs).

### Example 5  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Minimal Tropical Motivic Rank and Resolution Proof Width Correlation
- field_A × field_B: Tropical Geometry × Tseitin formulas  ×  Resolution proof complexity
- statement: For every d-regular graph G, the minimal tropical motivic rank (mtr(G)) of its associated Tseitin formula φ_G is linearly correlated with its resolution proof width w(φ_G), such that mtr(G) = Θ(w(φ_G)).

### Example 6  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Arithmetic Hierarchy Invariant Bounds Resolution Proof Width
- field_A × field_B: Arithmetic Hierarchy Theory  ×  Resolution Proof Complexity
- statement: For any given Tseitin formula π with n variables, the resolution proof width of π is bounded by the length of the longest sequence of jumps in the arithmetic hierarchy that can be represented using natural numbers derived from π, i.e., |A(π)| ≤ L(π), where A(π) represents the arithmetic hierarchy and L(π) is a function of n.

============================================================
Now propose a NEW conjecture. Different field_A. Different
statement. Same SHAPE: testable, falsifiable, ≤240s on n≤40.
============================================================