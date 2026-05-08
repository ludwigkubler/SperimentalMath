# `lean_verified/e14f176e4ef1` — Tropical Self-Convolution Doubling Law (refutation)

**Entry**: `e14f176e4ef1` — *Tropical Self-Convolution Doubling Law for MinimalFourierCoefficient*
**Original verdict**: `FALSIFIED` (notebook 2026-04-26 20:32 UTC)
**Pipeline status (2026-05-08)**: passed Gates 1–4, Gate 5 grade C (resubmit after major revisions; not standalone-publishable).

## What this directory certifies

- A `lake build` of `Eaudit.lean` succeeds under Lean 4.26.0 (Lake 5.0.0).
- The two named theorems compile via `native_decide` over IEEE-754 `Float`:
  - `Eaudit.E14f176e4ef1.counterexample_e14f176e4ef1` — at the empirical witness `[-7.0, 2.0, -7.0, -1.0, 2.0, -8.0, -10.0, -10.0]` (β = 5, n = 8), the residue `|MinFC(g) - 2·MinFC(f)|` exceeds the bound `5 / n = 0.625`.
  - `Eaudit.E14f176e4ef1.fullConjecture_false` — the universal claim is false.

## What this directory does NOT certify

- A proof over the real numbers. The Lean proof is over `Float`. A rigorous reformulation over `ℝ` would require interval arithmetic (e.g. `Mathlib.Tactic.NormNum` with explicit bounds) and is queued.
- The "right" finite-β rate. The empirical observation is that the conjectured `O(1/n)` is too aggressive at β = 5, n = 8, by roughly 6× — but the actual asymptotic rate is not measured.

## Reproduction

```bash
cd lean_verified/e14f176e4ef1
lake build
```

Build time: ~480 ms on commodity hardware. No `Mathlib` dependency.

## Source hashes

- `Eaudit.lean` SHA-256: `3b61f3dd59e97656444b01ad3904df10e9bbe0bf988d4dbc143db36282f5de09`
- `Eaudit.olean` SHA-256: `2c8d1a99bfef3c2e88eed202bfcf0f014d65c8bd8e16c542e0593b228dbc8793`

## Empirical reproduction

The Python test harness producing the same numerical values is in `sandbox_archive/test_e14f176e4ef1.py` (or as `test_code` in the JSONL notebook entry).

Reproduction: `rng = random.Random(11); skip 8 polynomials; the 9th polynomial at n=8 triggers |MFC(g) - 2·MFC(f)| ≈ 3.78546 vs bound 0.625`.
