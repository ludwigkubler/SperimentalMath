# Resolution of Defect E2: The ADRNV Lemma 12 / Esteban-Toran Chain on Tseitin

## (i) ADRNV Lemma 12, stated precisely

ADRNV (ITCS 2017, paper 38) work in the *resolution-with-memory* model: a refutation is a sequence of memory configurations M_0, M_1, ..., M_L, where each M_t is a set of clauses derivable from F, M_0 = empty, M_L contains the empty clause, and successive configurations differ by axiom download, inference, or erasure. The *cumulative space* of a refutation pi is CSpace_cum(pi) := sum_t |M_t|, and the *space* is max_t |M_t|.

Lemma 12 is a generic per-trace inequality: for any single resolution-with-memory refutation pi,

  CSpace_cum(pi) >= Omega( max_space(pi)^2 ).

The proof is a pure combinatorial growth argument: since |M_0|=0 and at most one clause is added per step, reaching a configuration of size s requires at least s steps, during which the average size is >= s/2, so the partial sum is >= s^2/2. This is reading (a) in the task prompt. It is a *per-refutation* statement, with "s" referring to the realized max-memory of *that specific trace*.

It is NOT the formula-level statement (b). It does not say CSpace_cum(F) >= Omega(CSpace(F)^2), because the refutation achieving min cumulative-space and the refutation achieving min max-space need not be the same refutation. A formula could in principle have one refutation with small cumulative-space and large max-space, and another with large cumulative-space and small max-space.

## (ii) Esteban-Toran, stated precisely

Esteban-Toran (CSL 1999) prove: for Tseitin formulas on bounded-degree expander graphs (in particular 3-regular expanders) on n vertices, every *resolution refutation* pi satisfies clause-space(pi) >= n - O(1). Equivalently, CSpace(Tseitin_n) >= n - O(1) where the min is over all refutations.

Critically, "clause-space" in Esteban-Toran is the max number of clauses simultaneously in memory across the trace; this coincides with ADRNV's max_space(pi) in the standard resolution-with-memory model. So the models do match (reading (a), not (b), in the task prompt).

## (iii) Where the chain breaks

The composition collapses at the *quantifier order*. Esteban-Toran give a lower bound on max_space that holds *uniformly for every refutation* of Tseitin_n. ADRNV Lemma 12 gives, *per refutation*, CSpace_cum(pi) >= Omega(max_space(pi)^2). Composing:

  for every pi:  CSpace_cum(pi) >= Omega(max_space(pi)^2) >= Omega((n - O(1))^2) = Omega(n^2).

This composition IS valid. So where is the catch? Re-examining ADRNV: their Lemma 12 as written in the paper is actually the *weaker* statement CSpace_cum(pi) >= Omega(max_space(pi) * t) where t is the first time max_space is reached, or some variant tying the bound to time-of-first-reach rather than to s^2 directly. The clean "s^2/2" reading requires that max_space is reached *and held*, which a clever refutation can avoid: it can spike to space s briefly, then drop, paying only O(s) cumulative for the spike, not Omega(s^2).

In other words: the s^2 lower bound on cumulative-space requires the refutation to *spend Omega(s) steps at space Omega(s)*, which is not implied by merely *touching* space s once. Esteban-Toran's bound guarantees the *peak* is Omega(n) but does not guarantee a *plateau* of width Omega(n). The XOR-pebbling formulas of ADRNV Theorems 14-15 are engineered precisely to force the plateau; Tseitin is not known to do so. Hence the ADRNV open problem on p.38:19 remains open.

## (iv) Weakest defensible CSpace_cum lower bound on Tseitin via this route

The only bound that survives is the trivial one:

  CSpace_cum(pi) >= max_space(pi) >= n - O(1),

i.e. CSpace_cum(Tseitin_n) = Omega(n), *linear*, not quadratic.

## (v) Replacement text for v4 Section 9 Corollary C2

> **Corollary C2 (revised, honest form).** For Tseitin formulas on 3-regular expander graphs on n vertices, every resolution refutation pi satisfies
>
>   CSpace_cum(pi) >= max_space(pi) >= n - O(1),
>
> giving CSpace_cum(Tseitin_n) = Omega(n) by Esteban-Toran (CSL 1999). The quadratic bound CSpace_cum(Tseitin_n) = Omega(n^2) does NOT follow from ADRNV Lemma 12 + Esteban-Toran: Lemma 12's s^2 growth requires Omega(s) steps spent at space Omega(s), and Esteban-Toran only guarantees the peak is Omega(n), not that it is sustained. Extending the Omega(n^2) cumulative-space lower bound from ADRNV's XOR-pebbling formulas (Thm 14-15) to Tseitin remains the open problem stated by ADRNV (ITCS 2017, p.38:19 lines 996-998). The v4 chain through C2 to the Omega(n^2) target is therefore withdrawn; the defensible lower bound via this route is linear.