import Mathlib

namespace Refutation_TropicalMFC

/-!
  The Python "TropicalFourierTransform" is defined as:
    TFT(f)[k] = Σ_{i=0}^{N-1} f[(i + k) mod N]

  Observe: {(i + k) mod N : i ∈ {0 .. N-1}} is always a permutation of
  {0 .. N-1}, so TFT(f)[k] = Σ_i f[i] for EVERY k — all modes are identical.

  Under additive translation f_c[x] = f[x] + c (no clamping needed for our
  witness since all values stay above -10):
    TFT(f_c)[k] = Σ_i (f[i] + c) = Σ_i f[i] + N · c

  Hence MFC(f_c) = |Σ f + N · c|, while MFC(f) = |Σ f|.
  These differ whenever N · c ≠ 0 — so the invariance claimed by the
  conjecture is GENERICALLY FALSE.

  Concrete refutation  (N = 2, f = [0, 0], c = 1/2):
    MFC([0, 0])       = |0 + 0|       = 0
    MFC([1/2, 1/2])   = |1/2 + 1/2|   = 1
    0 ≠ 1  ✓
-/

-- Python's tropical_fourier_transform: TFT(f)[k] = Σ_{i<N} f[(i+k) % N]
def tftCoeff (f : List ℚ) (k : ℕ) : ℚ :=
  (List.range f.length).foldl
    (fun acc i => acc + f.getD ((i + k) % f.length) 0)
    0

-- MFC(f) = min_{k ≠ 0} |TFT(f)[k]|
-- For N = 2 there is only one non-DC mode (k = 1), so MFC(f) = |TFT(f)[1]|.
def mfc (f : List ℚ) : ℚ := |tftCoeff f 1|

-- The specific failing instance
def f₀ : List ℚ := [0, 0]       -- original polynomial
def f_c : List ℚ := [1/2, 1/2]  -- translated by c = 1/2; max(0 + 1/2, -10) = 1/2, no clamping

-- The conjecture asserts mfc f₀ = mfc f_c.  We exhibit that it fails.
theorem refutation : mfc f₀ ≠ mfc f_c := by native_decide

end Refutation_TropicalMFC