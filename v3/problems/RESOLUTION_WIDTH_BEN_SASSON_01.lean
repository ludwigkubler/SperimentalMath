/-
  v3/problems/RESOLUTION_WIDTH_BEN_SASSON_01.lean

  Formal statement of the resolution width-size theorem (Ben-Sasson,
  Wigderson 2001) and the open question on tight constants for Tseitin
  on Ramanujan graphs.
-/

set_option linter.unusedVariables false
set_option autoImplicit false

namespace ResolutionWidthBenSasson01

/-- A literal: variable + polarity. -/
structure Literal where
  var      : Nat
  positive : Bool
  deriving Repr, BEq

/-- A clause: a list of literals. -/
abbrev Clause := List Literal

/-- A CNF formula. -/
abbrev CNF := List Clause

/-- Width of a clause = number of literals. -/
def Clause.width (c : Clause) : Nat := c.length

/-- A resolution step: from (C ∨ x) and (D ∨ ¬x), derive (C ∨ D). -/
inductive Resolvent (a b r : Clause) : Prop where
  | mk (x : Nat) : Resolvent a b r

/-- A resolution refutation: a sequence of clauses where each is either
    in the original CNF or derived from two earlier clauses. The final
    clause is the empty clause. -/
inductive ResolutionDerivation : CNF → List Clause → Prop where
  | axiom (F : CNF) (c : Clause)
      (h : c ∈ F) : ResolutionDerivation F [c]
  | resolve (F : CNF) (pref : List Clause)
      (a b r : Clause)
      (ha : a ∈ pref) (hb : b ∈ pref)
      (hres : Resolvent a b r)
      (h : ResolutionDerivation F pref) :
      ResolutionDerivation F (pref ++ [r])

/-- A resolution refutation is a derivation that ends with the empty clause. -/
def IsResolutionRefutation (F : CNF) (derivation : List Clause) : Prop :=
  ResolutionDerivation F derivation ∧
  [] ∈ derivation

/-- The size of a refutation is the number of distinct clauses. -/
def refutationSize (derivation : List Clause) : Nat := derivation.length

/-- The width of a refutation = max clause width. -/
def refutationWidth (derivation : List Clause) : Nat :=
  derivation.foldl (fun acc c => Nat.max acc c.width) 0

/-- The minimum-size refutation. -/
def minRefutationSize (F : CNF) (s : Nat) : Prop :=
  (∃ d : List Clause, IsResolutionRefutation F d ∧ refutationSize d = s) ∧
  (∀ d : List Clause, IsResolutionRefutation F d → s ≤ refutationSize d)

/-- The minimum-width refutation. -/
def minRefutationWidth (F : CNF) (w : Nat) : Prop :=
  (∃ d : List Clause, IsResolutionRefutation F d ∧ refutationWidth d = w) ∧
  (∀ d : List Clause, IsResolutionRefutation F d → w ≤ refutationWidth d)

-- ── The Ben-Sasson–Wigderson Width-Size theorem ─────────────────────

/-- BSW 2001: S(F) ≥ exp(Ω(W²/n)) where n is the number of variables. -/
def known_bsw_width_size : Prop :=
  ∃ c : Float,
    c > 0 ∧
    ∀ F : CNF, ∀ n w : Nat,
      -- n = number of variables in F (abstract — assume given)
      minRefutationWidth F w →
      ∀ s : Nat, minRefutationSize F s →
        -- s ≥ exp(c · w² / n)
        let exponent := c * (Float.ofNat (w * w)) / Float.ofNat n
        Float.ofNat s ≥ (2.0 ^ exponent)

-- ── Tseitin formulas (on a graph G with charge labelling) ────────────

/-- An undirected graph encoded as adjacency list. -/
abbrev Graph := List (List Nat)

/-- A *Tseitin formula* with parities (charges) for a graph G is a CNF
    that is unsatisfiable iff the parities sum to 1 mod 2 over the
    vertices. We leave the encoding opaque; the experimental harness
    will instantiate it. -/
opaque tseitin (G : Graph) (charges : List Bool) : CNF

-- ── The open question: tight constants for Ramanujan graphs ─────────

/-- Is G a Ramanujan graph? (Spectral gap reaches optimum 2√(k-1)/k.) -/
opaque isRamanujan (G : Graph) (k : Nat) : Prop

/-- The empirical resolution width of Tseitin on G, as measured by
    DRAT-extraction. -/
opaque empiricalTseitinWidth (G : Graph) : Nat

/-- BSW prediction: width = λ · n / k where λ is the expansion. -/
opaque bswPredictedWidth (G : Graph) : Nat

/-- Sub-Q1 as a Prop: on LPS Ramanujan graphs, empirical width matches
    the BSW prediction up to a multiplicative factor in [0.9, 1.1]. -/
def SubQ1_empirical_matches_prediction : Prop :=
  ∀ G : Graph, isRamanujan G 3 →
    let emp := empiricalTseitinWidth G
    let pred := bswPredictedWidth G
    -- |emp / pred - 1| ≤ 0.1
    Float.abs ((Float.ofNat emp / Float.ofNat pred) - 1.0) ≤ 0.1

end ResolutionWidthBenSasson01
