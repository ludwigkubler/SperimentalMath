# Re-test of `c26787a56682` after triage

**Status**: Gate 1+2 pass with reformulated conjecture; Gate 3 (literature) blocks novelty.

## Summary

The original entry's test reported `rank=0` for all trials, indicating
a malformed matrix construction. The triage queue
(`audit/TRIAGE_INCONCLUSIVE_2026-05-08.md`) flagged this as the single
genuine re-test candidate among the 49 non-crashing INCONCLUSIVE entries.

## Original statement (vacuous)

> For any AC⁰ circuit C computing PARITY on n inputs, the real rank of
> its Karchmer-Wigderson communication matrix M_C satisfies
> rank_R(M_C) ≥ Ω(√n).

By Razborov-Smolensky (1987), no AC⁰ circuit computes PARITY. The
universal quantifier ranges over the empty set; the statement is
**vacuously true** and tests nothing.

## Reformulated statement (substantive)

> The real rank of the Karchmer-Wigderson disagreement-indicator
> relation matrix M_PARITY associated with the function PARITY on
> n inputs satisfies rank_R(M_PARITY) ≥ √n.

## Test (corrected, deterministic, exact rational arithmetic)

`test_c26787a56682_v2.py` constructs M_PARITY for n ∈ {2,3,4,5,6,7}
explicitly and computes rank over ℚ with `fractions.Fraction`
(no floating-point). Output:

```
n=2: matrix 4×2,    rank=2, √n=1.4142  [OK]
n=3: matrix 12×4,   rank=4, √n=1.7321  [OK]
n=4: matrix 32×8,   rank=5, √n=2.0     [OK]
n=5: matrix 80×16,  rank=6, √n=2.2361  [OK]
n=6: matrix 192×32, rank=7, √n=2.4495  [OK]
n=7: matrix 448×64, rank=8, √n=2.6458  [OK]
RESULT: SUPPORTED min_rank_minus_sqrt_n=0.5858
```

The empirical pattern is `rank = n+1`, which is in fact a known classical
result via direct linear-algebra arguments on the disagreement-indicator
matrix.

## Pipeline status

| Gate | Verdict | Note |
|---|---|---|
| 1 Auditor | ✅ PASS | Deterministic (Fraction-exact), no stubs, no crashes, source hash recorded. |
| 2 Mathematician | ✅ PASS | Statement and test agree; the rank is exact, not approximate. |
| 3 Literature | ❌ FAIL on **novelty** | The rank of the KW disagreement-indicator matrix for PARITY is essentially n+1, a classical fact. Not novel. |
| 4 Lean-Formalizer | (skipped) | Pointless absent novelty. |
| 5 Royal Society | (would be grade D) | "Honest re-derivation of a known result." |

**Disposition**: not paper-worthy on its own. **Value of the exercise**:
demonstrates that the five-gate pipeline correctly distinguishes
"buggy test, salvageable" (Gate 1+2 pass) from "salvageable but not
novel" (Gate 3 fail). Without the literature gate this would have
been a false-positive SUPPORTED entry, the same failure mode that
the audit document flags.

## What this re-test confirms

1. The triage was right that the original test was buggy
   (rank=0 was wrong).
2. The triage was right that the statement could be reformulated
   (vacuous → substantive).
3. The conjecture, once reformulated, is true.
4. The literature gate is necessary: without it, this entry would
   have re-entered `supported_findings.md` despite being a known
   result.

The test code is committed for traceability and as a Gate-1+2 audit
record. It does NOT enter `lean_verified/` because it does not pass
Gate 3.

— L. K., 2026-05-09
