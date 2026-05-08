/-
  Mathlib-port v0 of `lean_verified/e14f176e4ef1/Eaudit.lean`.

  Purpose: lift the Float-based machine-readable record of the
  Tropical Self-Convolution Doubling Law refutation to a Real-typed
  Lean 4 file. Everything uses Mathlib's `Real`, `Complex`, and
  classical analysis. Proofs of the existential counterexample over
  `ℝ` are left as `sorry` and are the queued mathematical work
  (interval arithmetic on the explicit witness).

  Build: this file requires Mathlib. The lakefile.toml in this
  directory pulls Mathlib4 from upstream. First build: ~10-15 minutes
  (Mathlib compilation); subsequent builds: ~1-2 seconds (cached).

  Status: NOT yet built. Treated as the spec the Float port should
  eventually match.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Complex.Log

namespace EauditMathlib
namespace E14f176e4ef1

open Real Complex

abbrev TropicalPolynomial (n : ℕ) := Fin n → ℝ

/-- Min-plus self-convolution on Z_n. -/
noncomputable def tropicalConvolution {n : ℕ} (f : TropicalPolynomial n) :
    TropicalPolynomial n :=
  fun x => Finset.univ.inf' (Finset.univ_nonempty)
    (fun y => f y + f ((x - y : Fin n)))

/-- Maslov-dequantized Fourier coefficient at frequency k. -/
noncomputable def maslovTFT {n : ℕ} (β : ℝ) (f : TropicalPolynomial n)
    (k : Fin n) : ℂ :=
  -(1 / (β : ℂ)) * Complex.log
    (∑ x : Fin n, Real.exp (-β * f x) *
      Complex.exp (-2 * Real.pi * Complex.I * (k : ℂ) * (x : ℂ) / (n : ℂ)))

/-- Magnitude of the Fourier coefficient. -/
noncomputable def maslovTFTMagnitude {n : ℕ} (β : ℝ) (f : TropicalPolynomial n)
    (k : Fin n) : ℝ :=
  Complex.abs (maslovTFT β f k)

/-- Minimal Fourier coefficient. -/
noncomputable def minFC {n : ℕ} (β : ℝ) (f : TropicalPolynomial n) : ℝ :=
  (Finset.univ : Finset (Fin n)).inf'
    (Finset.univ_nonempty)
    (fun k => maslovTFTMagnitude β f k)

/-- Discrepancy as range. -/
noncomputable def disc {n : ℕ} (f : TropicalPolynomial n) : ℝ :=
  (Finset.univ.sup' (Finset.univ_nonempty) f) -
  (Finset.univ.inf' (Finset.univ_nonempty) f)

/-- The doubling-law conjecture, as a `Prop`. -/
def doublingLaw {n : ℕ} (β C : ℝ) (f : TropicalPolynomial n) : Prop :=
  let g := tropicalConvolution f
  |minFC β g - 2 * minFC β f| ≤ C / (n : ℝ) ∧
  disc g ≤ 2 * disc f

/-- The witness from the Float-based file, lifted to ℚ ⊂ ℝ.
    Empirically, |MFC(g) - 2·MFC(f)| ≈ 3.785 vs C/n = 0.625 at β=5, n=8. -/
def witnessReal : TropicalPolynomial 8 :=
  ![(-7 : ℝ), 2, -7, -1, 2, -8, -10, -10]

/-- Theorem: the Float-based existential refutation lifts to a real
    refutation. The proof requires interval arithmetic on the explicit
    Boltzmann sums; queued. -/
theorem counterexample_e14f176e4ef1_real :
    ¬ doublingLaw (5 : ℝ) (5 : ℝ) witnessReal := by
  sorry

/-- Theorem: the universal claim over ℝ is false. -/
theorem fullConjecture_false_real :
    ¬ (∀ {n : ℕ} (f : TropicalPolynomial n), doublingLaw (5 : ℝ) (5 : ℝ) f) := by
  intro h
  exact counterexample_e14f176e4ef1_real (h witnessReal)

end E14f176e4ef1
end EauditMathlib
