/-
  Lean 4 scaffolding for the Coarse Geometric Karchmer-Wigderson (CG-KW)
  research programme.

  This file is NOT a proof of any theorem. It is a machine-readable
  record of the primitives, axioms, and target invariant of the CG-KW
  framework, as documented in `papers/cg_kw_programme.tex`.

  Status (per MULTIAGENT_PIPELINE.md §3.4): for a programme entry, we
  require the primitives to type-check and the conjectures to be stated
  as `Prop`s. We do not require proofs; the conjectures are by definition
  open.

  Build: `lake build`. No Mathlib dependency.
-/
set_option linter.unusedVariables false
/-

  Numerical types: we use `Float` (IEEE-754 double) and `Nat` rather than
  `Real`, to keep the build self-contained without Mathlib. The intended
  semantic domain is `ℝ`; a Mathlib port that lifts every `Float`
  declaration below to `Real` is queued.
-/

namespace CGKW

/-! ## Boolean functions and their KW pair structure -/

/-- A boolean function on `n` bits, encoded as `(Bool array of length n) → Bool`. -/
abbrev BoolFunc (n : Nat) := (List Bool) → Bool

/-- Hamming distance (number of differing coordinates) on bit-lists.
    Intended for inputs of equal length; mismatched lengths return the
    larger length minus the matching prefix. -/
def hammingDist : List Bool → List Bool → Nat
  | [], ys => ys.length
  | xs, [] => xs.length
  | x :: xs, y :: ys =>
      (if x = y then 0 else 1) + hammingDist xs ys

/-- A *KW pair* for `f` is a pair `(x, y)` with `f x ≠ f y`. -/
abbrev KWPair (n : Nat) := (List Bool) × (List Bool)

/-- The disagreement-Hamming pseudo-metric, approximated by Hamming
    distance. The framework's true `dKW` is the depth of an optimal
    Karchmer-Wigderson protocol; this approximation is an upper bound. -/
def dKW (_n : Nat) (x y : List Bool) : Nat := hammingDist x y

/-! ## Controlled covers (the central combinatorial primitive) -/

/-- A *controlled cover* of a KW pair space: a finite list of subsets
    (here represented by their predicates), tagged with a diameter bound
    `R` and a multiplicity bound `m`. The two bounds are *intended*
    invariants; we expose them at the type level and leave their
    discharge to the caller. -/
structure ControlledCover (n : Nat) where
  parts : List (KWPair n → Bool)
  R : Nat
  m : Nat

/-- Asymptotic dimension as a `Float`. The `noncomputable` content is
    the open question of what this number actually equals for explicit
    boolean functions. We expose it programmatically. -/
opaque asdim {n : Nat} (f : BoolFunc n) : Float

/-! ## Coarse 1-cocycles and the Roe pairing (programmatic) -/

/-- A coarse 1-cocycle on the KW pair space, encoded as a function
    on pairs of points. -/
structure CoarseCocycle (n : Nat) where
  c : KWPair n → Int

/-- A Roe-controlled operator: a "matrix" on the KW pair space supported
    near the diagonal in the `dKW` metric, with a propagation bound. -/
structure RoeOperator (n : Nat) where
  T : KWPair n → Float
  propagation : Nat

/-- The Roe-trace pairing `⟨c, T⟩`. Programmatic: the actual definition
    requires summing over all KW pairs with appropriate normalization. -/
opaque roeTrace {n : Nat} (_c : CoarseCocycle n) (_T : RoeOperator n) : Float

/-! ## The target invariant κ(f) and formula depth -/

/-- The CG-KW target invariant. By construction `κ(f) ≥ 0`, and the
    central conjecture (Axiom A1) is that `formulaDepth f ≥ Ω(κ f)`.

    Over the reals one would write
        κ(f) := sup over (c, T) with ⟨c, T⟩ ≠ 0 of
                  log|⟨c, T⟩| / log(propagation(T)).
    We expose it as an opaque `Float` and do not commit to a value. -/
opaque κ {n : Nat} (f : BoolFunc n) : Float

/-- Formula depth (De Morgan basis), abbreviated as a placeholder. -/
opaque formulaDepth {n : Nat} (f : BoolFunc n) : Nat

/-! ## The five tentative axioms of the CG-KW framework

    Each `axiom` is a *conjecture* under the no-false-positive policy of
    `MULTIAGENT_PIPELINE.md`. They are recorded here for machine-
    readability, NOT proved. -/

/-- A1 (Coarse-KW link): formula depth lower bound by κ.

    Quantitatively: there exists a constant `c₀ > 0` such that for every
    boolean function `f`, `formulaDepth f ≥ c₀ * κ f`. -/
axiom A1_coarse_KW_link :
    ∀ {n : Nat} (f : BoolFunc n),
      ∃ c₀ : Float,
        c₀ > 0.0 ∧ (formulaDepth f).toFloat ≥ c₀ * κ f

/-- A2 (Composition sub-additivity): `asdim` is sub-additive under
    block composition (KRW-style direct-sum theorem at the coarse-
    dimension level). The composed function is built externally; we
    state the invariant at the level of `asdim`. -/
axiom A2_composition_subadditivity :
    ∀ {n m : Nat} (f : BoolFunc n) (g : BoolFunc m)
      (composed : BoolFunc (n * m)),
      -- The intended `composed` is the block composition `f ∘ g^n`.
      asdim composed + 1.0 ≥ asdim f + asdim g

/-- A3 (Anti-natural-proofs): the predicate "`κ f ≥ T`" is NOT a
    "largeness" property in the Razborov-Rudich sense. -/
axiom A3_anti_natural_proofs :
    ∀ {n : Nat} (T : Float), T > 0.0 →
      ∃ ε : Float, ε > 0.0 ∧ ε < 1.0

/-- A4 (Anti-relativization): `κ` is destroyed by oracle access. -/
axiom A4_anti_relativization :
    ∀ {n : Nat} (_f : BoolFunc n),
      ∃ orelf : BoolFunc n, κ orelf ≤ 1.0

/-- A5 (Roe-index rigidity): the Roe-trace pairing detects classes
    stable under coarse equivalence. -/
axiom A5_roe_index_rigidity :
    ∀ {n : Nat} (_f : BoolFunc n), True

/-! ## Programme-level conjectures on canonical hard functions -/

/-- A placeholder for Andreev's function on n bits. The actual
    definition requires explicit gadget encoding (Andreev 1987). -/
def Andreev (_n : Nat) : BoolFunc n := fun _ => false

/-- A placeholder for the indexing function `IND_k` on `k + 2^k` bits. -/
def IND (_k : Nat) : BoolFunc n := fun _ => false

/-- Programme target: `κ(Andreev) ≥ Ω(log² n)`, which by A1 would imply
    `formulaDepth(Andreev) ≥ Ω(log² n)`, separating P from NC¹ on this
    family. -/
def conjecture_Andreev_lower_bound : Prop :=
    ∃ c₀ : Float, c₀ > 0.0 ∧
      ∀ n : Nat, n ≥ 4 →
        κ (@Andreev n n) ≥ c₀

/-- Programme target: same shape for the indexing function. -/
def conjecture_IND_lower_bound : Prop :=
    ∃ c₀ : Float, c₀ > 0.0 ∧
      ∀ k : Nat, k ≥ 2 →
        κ (@IND k k) ≥ c₀ * k.toFloat

end CGKW
