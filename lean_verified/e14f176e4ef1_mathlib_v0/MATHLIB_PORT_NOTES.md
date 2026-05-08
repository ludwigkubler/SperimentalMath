# Mathlib port v0 — `e14f176e4ef1`

**Status**: spec only; *not* compiled.

## What this directory contains

`Eaudit.lean` lifts the Float-based machine-readable record in
`lean_verified/e14f176e4ef1/` to `Real`-typed Mathlib statements:

* `TropicalPolynomial n := Fin n → ℝ`
* `tropicalConvolution`, `maslovTFT`, `maslovTFTMagnitude`, `minFC`, `disc`
  defined over ℝ / ℂ via Mathlib's `Real`, `Complex`, `Real.exp`,
  `Complex.log`.
* `doublingLaw : Prop`
* `witnessReal : TropicalPolynomial 8` — the Float witness lifted to
  ℚ ⊂ ℝ.
* `counterexample_e14f176e4ef1_real` — the existential refutation;
  `sorry` placeholder.
* `fullConjecture_false_real` — derives the universal-claim refutation
  from the existential.

## Why not yet compiled

A `lake build` of this file requires Mathlib4 (≈ 1 GB of compiled
`.olean`s), which on a fresh checkout is a 10–15 minute build. We do
not commit pre-compiled `.olean`s; the user's CI is expected to do that.

## Sketch of the queued proof for `counterexample_e14f176e4ef1_real`

The Float-based proof in the existing
`lean_verified/e14f176e4ef1/Eaudit.lean` evaluates concretely:

```
β = 5,  n = 8,  f = (-7, 2, -7, -1, 2, -8, -10, -10)
|MFC(f★f) - 2·MFC(f)| ≈ 3.78546
bound = 5 / 8 = 0.625
```

with `native_decide` over IEEE-754 doubles. To lift this to ℝ we have two
options:

1. **Interval arithmetic.** Use `Mathlib.Tactic.NormNum`'s rational-arithmetic
   evaluator together with explicit error bounds on `Real.exp`, `Real.log`,
   `Real.cos`, `Real.sin` evaluated at the Boltzmann arguments. The
   final 6× margin of `3.78` over `0.625` is comfortable for any plausible
   rounding error.
2. **Hand-proof.** Compute MFC(f), MFC(f★f) symbolically as exact
   ℝ-valued sums, take absolute value, compare to 0.625. The Boltzmann
   weights `e^{-5·k}` for `k ∈ {-7..10}` are transcendental but the
   inequality is decidable to high precision.

Both routes are queued. Estimated effort: 1–2 working weeks.

## Status of the universal claim

`fullConjecture_false_real` is one line once the existential is in hand.

## Why "v0"

Spec is preliminary. Reviewers may want different naming conventions
(e.g. `MFC` vs `minFC`, `Disc` vs `disc`), or want the conjecture
phrased with `∃ c₀ : ℝ, c₀ > 0 ∧ ...` rather than the explicit `5`.
The naming is open to change before the file is committed for build.

— L. K., 2026-05-09
