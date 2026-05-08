# CG-KW sub-conjecture test repair queue

**Date**: 2026-05-09
**Author**: L. K.
**Disposition**: re-emit, do not hand-patch.

## Summary

The 10 sub-conjectures generated under the CG-KW framework
(`fw_85a254b4a0`) all have buggy auto-generated empirical tests. None of
them can be hand-patched cost-effectively because the underlying
mathematical content (asymptotic dimension, Roe-trace pairing, Property A,
asdim sub-additivity, ultralimit completion) requires careful redesign of
the test, not a one-line fix.

Re-emission under the patched proposer
(`papers/cg_kw_programme/`, with the
`pvsnp_explorer.py` patches landed today)
is the cost-effective path.

## Crash table

| Entry ID | Verdict | Crash type | Diagnosis |
|---|---|---|---|
| `e871be18b26c` | INCONCLUSIVE | `ValueError: math domain error` | `log2(0)` on the root node of a hierarchical cover construction |
| `738bb754804a` | INCONCLUSIVE | `ValueError: math domain error` | Same family — log of vanishing pairing under a special test instance |
| `7c5ad65991c5` | INCONCLUSIVE | `TypeError: 'int' object is not iterable` | Auto-generated test treats an integer like a list |
| `f685d342f4c0` | INCONCLUSIVE | `NameError: name 'f' is not defined` | Loop variable scoping bug in the auto-generated code |
| `a81b4af0bc2b` | INCONCLUSIVE | `TypeError: 'int' object is not subscriptable` | Index access on a scalar |
| `cc8127953d91` | INCONCLUSIVE | `IndexError: tuple index out of range` | Pullback over a coarse-Lipschitz reduction with empty domain |
| `ed6023df7533` | BARRIER_HIT | `NATURAL_PROOFS` (conf 0.70) | Pre-rejected by barrier filter; A3 tension flagged in CG-KW programme paper |
| `2ee2e2f64a25` | BARRIER_HIT | `NATURAL_PROOFS` (conf 0.78) | Same A3 tension |
| `8047f7f8eea1` | INCONCLUSIVE | `TypeError: 'int' object is not iterable` | Same family as `7c5ad65991c5` |
| `264c40c0d040` | INCONCLUSIVE | `IndexError: list index out of range` | Off-by-one in HX¹ computation |

## Coverage by the patched proposer

The `pvsnp_explorer.py` patch (commit landing today) addresses exactly
this class of crashes:

* **anti-pattern (b)** — `math.log` / `math.log2` domain guard — fixes
  `e871be18b26c`, `738bb754804a`.
* **anti-pattern (e)** — index bounds — fixes `cc8127953d91`,
  `264c40c0d040`.
* The TypeError family (`7c5ad65991c5`, `a81b4af0bc2b`,
  `8047f7f8eea1`) is harder to address purely at the prompt level; the
  proposer needs to write more careful type-checking. Lean port (queued)
  would catch these statically.
* The NameError (`f685d342f4c0`) is covered by the existing
  `DEFAULT_TEST_PRELUDE` and shouldn't recur.

## Action

1. The two BARRIER_HIT entries (`ed6023df7533`, `2ee2e2f64a25`) are
   stricken from the CG-KW sub-conjecture pool. Their A3 tension is
   documented as Open Problem 7 of the CG-KW programme paper.
2. The 8 crashed entries are flagged for re-emission. The proposer's
   next CG-KW cycle should be allowed to re-attempt them with the
   patched prompt; we expect the crash rate on this batch to drop
   from 8/8 to ≤ 2/8.
3. No hand-patches are committed. The buggy test code remains in the
   notebook for traceability but the entries are tagged
   `awaiting_reemission` in `inconclusive_triage.json`.

— L. K., 2026-05-09
