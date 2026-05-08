/-
  Lean 4 formalization for SperimentalMath entry `e14f176e4ef1`.

  Entry: "Tropical Self-Convolution Doubling Law for MinimalFourierCoefficient"
  Verdict: FALSIFIED at finite β, n ∈ {8, 16, 32, 64}
  Bridge: TROPICAL_FOURIER_ANALYSIS × Two-party deterministic comm. complexity

  This file produces:
    * machine-readable definitions of the primitives used in the conjecture
      (over `Float` for executable/decidable form, and the conjecture statement
      remains a `Prop`);
    * a falsifying witness as an executable `def`;
    * a `theorem counterexample_e14f176e4ef1` stating the falsification,
      whose content is purely existential over `Float` arithmetic — `decide`
      handles the inequality.

  Caveat: Float-based proofs are NOT rigorous over the reals. They certify
  that the IEEE-754 double-precision reproduction of the test verifies the
  inequality. A rigorous proof over the reals would require interval
  arithmetic (e.g. via mathlib's `IntervalArith`) and is left for Gate 4 v2.

  Status: this file is the minimal machine-readable Lean record per
  `MULTIAGENT_PIPELINE.md` §3.4 ("for supporting entries: at minimum a
  def of the primitives plus a stated conjecture"). Strengthening to a
  fully rigorous theorem is queued.
-/

namespace Eaudit
namespace E14f176e4ef1

/-- A tropical polynomial on `Z_n` is just a list of `n` Float coefficients. -/
abbrev TropicalPolynomial := List Float

/-- The min-plus self-convolution: `(f ⋆ f)[x] = min_y (f[y] + f[(x - y) mod n])`. -/
def tropicalConvolution (f : TropicalPolynomial) : TropicalPolynomial :=
  let n := f.length
  let coeffs : List (Float × Nat) :=
    (List.range n).map (fun x =>
      let candidates : List Float :=
        (List.range n).map (fun y =>
          let z := (x + n - y) % n
          (f[y]?).getD 0.0 + (f[z]?).getD 0.0)
      let m := candidates.foldl (fun a b => if b < a then b else a)
        ((candidates.head?).getD 0.0)
      (m, x))
  (coeffs.toArray.qsort (fun a b => a.2 < b.2)).toList.map Prod.fst

/-- Maslov-dequantized TFT magnitude:
    `|F_β[f](k)| = |-(1/β) · log( Σ_x exp(-β·f[x]) · exp(-2πi k x/n) )|`.
    Decomposed into real/imag parts to avoid complex `Float.exp`. -/
def maslovTFTMagnitude (β : Float) (f : TropicalPolynomial) (k : Nat) : Float :=
  let n := f.length
  let nF : Float := n.toFloat
  let kF : Float := k.toFloat
  let twoPi : Float := 2.0 * 3.141592653589793
  let pairs := (List.range n).map (fun x =>
    let fx := (f[x]?).getD 0.0
    let w := Float.exp (-β * fx)
    let angle := -(twoPi * kF * x.toFloat) / nF
    (w * Float.cos angle, w * Float.sin angle))
  let reS := pairs.foldl (fun acc p => acc + p.1) 0.0
  let imS := pairs.foldl (fun acc p => acc + p.2) 0.0
  let mod := Float.sqrt (reS * reS + imS * imS)
  -- |coeff| = |(1/β)| * |log(mod) + i·arg|; the modulus log magnitude is what's needed:
  let logMod := Float.log mod
  -- argS in (-π, π]:
  let argS := Float.atan2 imS reS
  let coeffRe := -(1.0 / β) * logMod
  let coeffIm := -(1.0 / β) * argS
  Float.sqrt (coeffRe * coeffRe + coeffIm * coeffIm)

/-- Minimal Fourier coefficient over `k ∈ {0, …, n-1}`. -/
def minFC (β : Float) (f : TropicalPolynomial) : Float :=
  let n := f.length
  let mags := (List.range n).map (fun k => maslovTFTMagnitude β f k)
  match mags with
  | []      => 0.0
  | h :: t  => t.foldl (fun a b => if b < a then b else a) h

/-- Discrepancy as defined in the test: `Disc(f) = max(f) - min(f)` (range/amplitude). -/
def disc (f : TropicalPolynomial) : Float :=
  match f with
  | []      => 0.0
  | h :: t  =>
    let mx := t.foldl (fun a b => if a < b then b else a) h
    let mn := t.foldl (fun a b => if b < a then b else a) h
    mx - mn

/-- The conjecture as a `Prop` parametrized by a slack `C / n` and a Boltzmann `β`. -/
def conjectureDoublingLaw (β : Float) (C : Float) (f : TropicalPolynomial) : Prop :=
  let g := tropicalConvolution f
  let mfF := minFC β f
  let mfG := minFC β g
  let n := f.length
  let bound := C / n.toFloat
  -- (i): | MFC(g) - 2·MFC(f) | ≤ C/n
  ((mfG - 2.0 * mfF).abs ≤ bound) ∧
  -- (ii): Disc(g) ≤ 2·Disc(f)
  (disc g ≤ 2.0 * disc f)

/-- Falsifying witness, extracted from the empirical run at seed=11, trial_idx=8.
    Reproduction: rng = random.Random(11); skip 8 polynomials; the 9th polynomial at n=8
    triggers |MFC(g) - 2·MFC(f)| ≈ 3.78546 vs the bound 5/8 = 0.625. -/
def witness : TropicalPolynomial :=
  [-7.0, 2.0, -7.0, -1.0, 2.0, -8.0, -10.0, -10.0]

/-- Existential falsification. The Lean term certifies the violation of
    inequality (i) at the witness above for β=5 and slack C=5.
    NOTE: this is over `Float`, not over `ℝ`; see file header caveat. -/
theorem counterexample_e14f176e4ef1 :
    let β : Float := 5.0
    let C : Float := 5.0
    -- The conjecture is not (∀ f, conjecture). Its falsification is (∃ f, ¬ conjecture).
    -- We record the empirical violation magnitude rather than rely on `decide`
    -- (Float Prop comparison via `decide` is fragile across kernels).
    (let g := tropicalConvolution witness
     let bound := C / witness.length.toFloat
     let mfF := minFC β witness
     let mfG := minFC β g
     -- The empirical run reports |MFC(g) - 2·MFC(f)| ≈ 3.78546 vs bound 0.625
     -- We expose the numerator and the bound; the human reader (or a
     -- future interval-arithmetic refinement) verifies 3.78 > 0.625.
     ((mfG - 2.0 * mfF).abs > bound)) := by
  -- Float Prop reduction in Lean 4 is via `native_decide` for IEEE-754 ground terms.
  native_decide

/-- The conjecture itself (universal claim) is not proven — it is empirically
    falsified. We record the universal Prop for documentation. -/
def fullConjecture : Prop :=
  ∀ (f : TropicalPolynomial), conjectureDoublingLaw 5.0 5.0 f

/-- The falsification of the universal claim follows from the witness. -/
theorem fullConjecture_false : ¬ fullConjecture := by
  intro h
  have hw := h witness
  -- hw says: (|MFC(g) - 2·MFC(f)|.abs ≤ bound) ∧ (disc g ≤ 2·disc f)
  -- counterexample_e14f176e4ef1 says: |MFC(g) - 2·MFC(f)|.abs > bound
  have hcount := counterexample_e14f176e4ef1
  -- Float `≤` and `>` are mutually exclusive (decidable on IEEE-754):
  exact absurd hw.1 (by native_decide)

end E14f176e4ef1
end Eaudit
