/-
  v3/problems/PERMANENT_DETERMINANT_VALIANT_79.lean

  Formal statement of the Permanent vs Determinant problem (Valiant 1979)
  and the open question of super-polynomial determinantal complexity.
-/

set_option linter.unusedVariables false
set_option autoImplicit false

namespace PermanentDeterminantValiant79

-- ── Matrix abstraction ────────────────────────────────────────────────

/-- An n × n matrix represented as a list of lists of integers. Wrong-sized
    inputs return 0 for missing entries. -/
abbrev IntMatrix := List (List Int)

/-- Get an entry. Renamed to `entry` to avoid recursive name conflict. -/
def IntMatrix.entry (M : IntMatrix) (i j : Nat) : Int :=
  match M[i]? with
  | none      => 0
  | some row  => (row[j]?).getD 0

/-- Permanent of an n x n integer matrix. Slow but correct definition.
    Uses an `Id.run do` block for the imperative-style sum. -/
partial def perm (M : IntMatrix) (n : Nat) : Int :=
  let rec enumerate (used : List Nat) (i : Nat) : Int := Id.run do
    if i ≥ n then return 1
    let mut acc : Int := 0
    for j in [0:n] do
      if !(used.contains j) then
        let entry := M.entry i j
        acc := acc + entry * enumerate (j :: used) (i+1)
    return acc
  enumerate [] 0

/-- Determinant: sum over permutations of sign times product. -/
partial def det (M : IntMatrix) (n : Nat) : Int :=
  let rec enumerate (used : List Nat) (i : Nat) (sgn : Int) : Int := Id.run do
    if i ≥ n then return sgn
    let mut acc : Int := 0
    for j in [0:n] do
      if !(used.contains j) then
        let invs := (used.filter (· < j)).length
        let s := if invs % 2 == 0 then 1 else -1
        let e := M.entry i j
        acc := acc + e * enumerate (j :: used) (i+1) (sgn * s)
    return acc
  enumerate [] 0 1

-- ── Determinantal complexity ──────────────────────────────────────────

/-- An "affine entry" is an integer-coefficient linear combination of the
    entries of a source matrix plus a constant. -/
structure AffineEntry where
  /-- Coefficient of source entry M[i,j] in this affine combination. -/
  coeffs : List (List Int)   -- coeffs[i][j] = coefficient of M[i,j]
  /-- Additive constant. -/
  constant : Int
  deriving Repr

/-- Evaluate an affine entry on a source matrix M. -/
def AffineEntry.eval (a : AffineEntry) (M : IntMatrix) (n : Nat) : Int := Id.run do
  let mut acc := a.constant
  for i in [0:n] do
    for j in [0:n] do
      let ci := (a.coeffs[i]?).getD []
      let c := (ci[j]?).getD 0
      acc := acc + c * M.entry i j
  return acc

/-- An m x m affine matrix in terms of an n x n source. -/
abbrev AffineMatrix := List (List AffineEntry)

/-- Realize an affine matrix on a source M to get a concrete integer matrix. -/
def AffineMatrix.realize (B : AffineMatrix) (M : IntMatrix) (n : Nat) : IntMatrix :=
  B.map (fun row => row.map (fun ae => ae.eval M n))

/-- m is a *determinantal-complexity witness* for n if there is an m x m
    affine matrix B such that for every n x n integer matrix M,
    det(B(M)) = perm(M). -/
def IsDetComplexityWitness (n m : Nat) : Prop :=
  ∃ B : AffineMatrix,
    (B.length = m ∧ B.all (·.length = m)) ∧
    ∀ M : IntMatrix,
      (M.length = n ∧ M.all (·.length = n)) →
      det (B.realize M n) m = perm M n

/-- The determinantal complexity m(n) is the minimum such m. -/
def detComplexity (n m : Nat) : Prop :=
  IsDetComplexityWitness n m ∧
  ∀ m' : Nat, m' < m → ¬ IsDetComplexityWitness n m'

-- ── Known bounds ──────────────────────────────────────────────────────

/-- Grenet 2014 upper bound: m(n) ≤ 2^n - 1. -/
def known_upper_bound : Prop :=
  ∀ n : Nat, n ≥ 2 →
    ∃ m : Nat,
      IsDetComplexityWitness n m ∧
      m ≤ 2 ^ n - 1

/-- Mignon-Ressayre 2004 lower bound: m(n) ≥ n²/2. -/
def known_lower_bound : Prop :=
  ∀ n : Nat, n ≥ 3 →
    ∀ m : Nat, IsDetComplexityWitness n m →
      m ≥ n * n / 2

/-- Jansen 2011: m(3) = 7. -/
def jansen_2011_m3_equals_7 : Prop :=
  detComplexity 3 7

-- ── The Valiant conjecture (VP ≠ VNP, in the determinantal form) ─────

/-- Valiant's conjecture: m(n) is super-polynomial in n. -/
def OpenConjecture_Valiant : Prop :=
  ∀ k : Nat,
    ∃ N0 : Nat, ∀ n : Nat, n ≥ N0 →
      ∀ m : Nat, IsDetComplexityWitness n m →
        m > n ^ k

-- ── Sub-question 1: exact m(4) ───────────────────────────────────────

def SubQ1_m4_exact_value : Prop :=
  ∃ m4 : Nat, detComplexity 4 m4 ∧ m4 ≥ 8 ∧ m4 ≤ 15

-- ── Sub-question 3: tightness of Grenet at n=4 ────────────────────────

def SubQ3_grenet_tight_at_n4 : Prop :=
  detComplexity 4 15 ∨ ¬ IsDetComplexityWitness 4 14

end PermanentDeterminantValiant79
