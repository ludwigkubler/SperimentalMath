
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
- title: Tusnady 2-Box Discrepancy of Clause-Polarity Cloud Bounds DPLL Size
- field_A × field_B: Geometric combinatorial discrepancy — Tusnady's problem and the Chazelle–Matouse  ×  Tree-like Resolution / DPLL refutation size t*(F) for random unsatisfiable 3-CNF
- statement: For an unsatisfiable 3-CNF F with m clauses on n variables, define the 2-marginal polarity discrepancy D_2(F) := max over 1 ≤ i < j ≤ n and (s,t) in {-,+}^2 of |c_{ij}^{st}(F) − mu_{ij}^{st}|, where c_{ij}^{st}(F) is the number of clauses of F containing literal x_i^s AND literal x_j^t, and mu_{ij}^{st} = m·(3/n)·(2/(n−1))·(1/4) is the expected count under the uniform random 3-CNF model with parameters (m,n). Conjecture: for unsat 3-CNFs F drawn at clause density alpha = 4.5 on n in {12, 14, 16, 18, 20} variables, the Spearman rank correlation between −D_2(F)/sqrt(m) and log_2 t*(F) across 30 
- counterexample (witness of falsification): correlation=0.19999999999999996

### Example 5  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Halász L^2 Spectrum Discrepancy Lower-Bounds Sign-Matrix Rigidity
- field_A × field_B: Erdős–Turán / Halász L^2 discrepancy of empirical measures on [0,1] (Halász 1981  ×  Matrix rigidity R_M(r) for sign matrices M∈{±1}^{N×N} in the Valiant 1977 / Frie
- statement: Let M∈{±1}^{N×N} have singular values σ_1≥…≥σ_N≥0; since ‖M‖_F^2=N^2 the weights p_i:=σ_i^2/N^2 form a probability distribution on [N]. Define the empirical descending-cumulative CDF F_M:[0,1]→[0,1] by F_M(t):=Σ_{i≤⌊tN⌋} p_i and the Halász L^2 discrepancy against the uniform-spectrum reference U(t)=t by D_2(M):=(∫_0^1 (F_M(t)−t)^2 dt)^{1/2}∈[0,1/√3]. Conjecture: there exists an absolute constant c>0 such that for every M∈{±1}^{N×N}, σ_{⌊N/2⌋+1}(M)^2 ≥ c·N·(1−4·D_2(M))_+ (where (x)_+:=max(0,x)); a single sign matrix exhibiting σ_{⌊N/2⌋+1}^2 < (c/2)·N·(1−4D_2)_+ falsifies it.

### Example 6  [tier 4: INCONCLUSIVE but well-tested (showcases test grain)]
- title: Bourgain-Tzafriri Sub-Column Spectral Excess Bounds DISJ CC_R
- field_A × field_B: Bourgain–Tzafriri / Kashin restricted invertibility theory — average operator no  ×  Randomized two-party communication complexity CC_R(M) of N×N Boolean matrices, w
- statement: Center M ∈ {0,1}^{N×N} to M̃ = 2M − J ∈ {±1}^{N×N}. Fix k = ⌈log_2 N⌉ and let S_1,…,S_{30} ⊂ [N] be uniformly random column subsets of size k drawn with seeds 1..30. Define the sub-column spectral excess ξ(M) := (1/30)·Σ_{s=1}^{30}(‖M̃|_{S_s}‖_op² / N − 1), where M̃|_S is the N×k column submatrix. We conjecture that for every Boolean matrix M with N ≤ 32: (i) ξ(M) ≥ 0; (ii) CC_R(M) ≥ ⌊log_2(1 + N·ξ(M)/k)⌋ − 1; (iii) ξ(M_PARITY_n) ≤ 0.05 (so the bound gives O(1), matching CC_R = O(1)) and ξ(M_DISJ_n) ≥ 0.5·k/n at n=3,4,5 (so the bound delivers Ω(log N) for DISJ). A single seed-30 ensemble at an
- counterexample (witness of falsification): xi_parity=25.05 > 0.05

============================================================
Now propose a NEW conjecture. Different field_A. Different
statement. Same SHAPE: testable, falsifiable, ≤240s on n≤40.
============================================================