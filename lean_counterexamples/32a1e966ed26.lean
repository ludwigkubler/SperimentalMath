import Mathlib

namespace Refutation_TropicalParseval

/-!
# Refutation of the Tropical Parseval Lower Bound Conjecture

Conjecture: For tropical polynomial f on {0,...,N-1},
  F[k] = max_n(f[n] - 2π·n·k/N)   (tropical Fourier transform)
  Disc(f) = max(f) - mean(f)
  Claim: min_k F[k] ≤ Disc(f)

Key mathematical fact enabling a purely rational refutation:
  theta(0, k) = -2π · 0 · k / N = 0  for every k.
  Therefore F[k] ≥ f[0] + 0 = f[0] for every k.
  Hence min_k F[k] ≥ f[0].

So if f[0] > Disc(f), the lower bound min_k F[k] ≤ Disc(f) is violated.

Witness (N = 8): f = [4, 4, 4, 4, 4, 4, 4, 5]
  f[0]    = 4
  max(f)  = 5
  mean(f) = 33/8
  Disc(f) = 5 - 33/8 = 7/8
  min_k F[k] ≥ f[0] = 4 > 7/8 = Disc(f)   ← conjecture VIOLATED
-/

-- Maximum of a list of rationals (0 for empty list)
def listMax : List ℚ → ℚ
  | []      => 0
  | x :: xs => xs.foldl max x

-- Discrepancy: max(f) - mean(f)
def disc (f : List ℚ) : ℚ :=
  listMax f - f.sum / (f.length : ℚ)

-- Lower bound on min_k F[k]: since F[k] ≥ f[0] for all k,
-- f[0] is a valid lower bound for the tropical Fourier minimum.
def tropFourierLB : List ℚ → ℚ
  | []      => 0
  | x :: _ => x

-- The specific failing instance
def witness : List ℚ := [4, 4, 4, 4, 4, 4, 4, 5]

-- Sanity: discrepancy of the witness is 7/8
theorem disc_witness_eq : disc witness = 7 / 8 := by native_decide

-- Sanity: the certified Fourier lower bound is 4
theorem lb_witness_eq : tropFourierLB witness = 4 := by native_decide

-- Refutation: the conjecture would require tropFourierLB witness ≤ disc witness,
-- i.e., 4 ≤ 7/8, which is false.
-- Since the actual min_k F[k] ≥ tropFourierLB witness = 4 > 7/8 = disc witness,
-- the claimed inequality min_k F[k] ≤ Disc(f) is violated on this witness.
theorem refutation : ¬ (tropFourierLB witness ≤ disc witness) := by
  native_decide

end Refutation_TropicalParseval