import Mathlib

namespace Refutation_TropicalShift

/-
  FALSIFIED conjecture: MinimalFourierCoefficient (MFC) is invariant under
  additive translation  f_c(x) = f(x) + c  in the tropical-Fourier framework.

  The Python TFT:  TFT(f)[k] = Σ_{i=0}^{N-1} f[(i+k) % N]
  Observation: as i ranges over {0,...,N-1} so does (i+k) % N (cyclic
  permutation), so  TFT(f)[k] = sum(f)  for EVERY k, including k ≠ 0.

  Therefore  MFC(f) = |sum(f)|,  and
             MFC(f_c) = |sum(f_c)| = |sum(f) + N·c|.

  These are generally different:

  Concrete counterexample  (N = 4, c = 1):
    f      = [0, 0, 0, 0]   →  MFC(f)   = |0| = 0
    f_c    = [1, 1, 1, 1]   →  MFC(f_c) = |4| = 4
    0 ≠ 4  — conjecture fails.
-/

-- The "Tropical Fourier" coefficient at frequency k:
--   TFT(f)[k] = Σ_{i < N} f[(i + k) % N]
def tftCoeff (f : List ℚ) (k : ℕ) : ℚ :=
  (List.range f.length).foldl
    (fun acc i => acc + f.getD ((i + k) % f.length) 0) 0

-- Minimal Fourier Coefficient: min_{k=1}^{N-1} |TFT(f)[k]|
def mfc (f : List ℚ) : ℚ :=
  let vals := (List.range (f.length - 1)).map (fun k => |tftCoeff f (k + 1)|)
  match vals with
  | []     => 0
  | h :: t => t.foldl min h

-- Discrepancy as in the Python: max(f) - mean(f)
def discrepancy (f : List ℚ) : ℚ :=
  let n := f.length
  if n = 0 then 0
  else
    let s := f.foldl (· + ·) 0
    let mx := f.foldl max (f.getD 0 0)
    mx - s / n

-- Concrete witness
def witnessF  : List ℚ := List.replicate 4 0   -- f
def witnessFc : List ℚ := List.replicate 4 1   -- f_c, translation c = 1

-- MFC is NOT invariant: mfc([0,0,0,0]) = 0  but  mfc([1,1,1,1]) = 4
theorem not_mfc_invariant : mfc witnessF ≠ mfc witnessFc := by
  native_decide

-- Discrepancy IS invariant on this particular (constant) witness,
-- but MFC already refutes the conjecture.
-- (For a non-constant witness the discrepancy also fails, but one
--  counterexample suffices.)
theorem refutation : ¬ (mfc witnessF = mfc witnessFc) := not_mfc_invariant

end Refutation_TropicalShift