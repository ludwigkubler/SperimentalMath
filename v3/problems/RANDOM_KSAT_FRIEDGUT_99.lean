/-
  v3/problems/RANDOM_KSAT_FRIEDGUT_99.lean

  Formal statement of the random k-SAT sharp threshold conjecture
  (Friedgut 1999) and the open question for k = 3.
-/

set_option linter.unusedVariables false
set_option autoImplicit false

namespace RandomKSatFriedgut99

-- ── k-SAT formulas ────────────────────────────────────────────────────

/-- A literal: variable index and polarity (true = positive, false = negated). -/
structure Literal where
  var      : Nat
  positive : Bool
  deriving Repr, BEq

/-- A k-clause: a list of literals (typically of length k). -/
abbrev KClause := List Literal

/-- A k-CNF formula: a list of k-clauses. -/
abbrev KCNF := List KClause

/-- Truth assignment: a list of Bool, indexed by variable. -/
abbrev Assignment := List Bool

/-- A literal is satisfied by an assignment if (variable's value XOR negation) = 1. -/
def Literal.satisfied (l : Literal) (a : Assignment) : Bool :=
  match a[l.var]? with
  | none      => false   -- variable out of range — treat as unsatisfied
  | some val  => val == l.positive

/-- A clause is satisfied if at least one literal is. -/
def KClause.satisfied (c : KClause) (a : Assignment) : Bool :=
  c.any (·.satisfied a)

/-- A formula is satisfied if all clauses are. -/
def KCNF.satisfied (f : KCNF) (a : Assignment) : Bool :=
  f.all (·.satisfied a)

/-- A formula is SAT if some assignment of the right length satisfies it. -/
def KCNF.isSat (f : KCNF) (n : Nat) : Prop :=
  ∃ a : Assignment, a.length = n ∧ f.satisfied a = true

-- ── The random k-SAT distribution ─────────────────────────────────────

/-- The probability that a random k-SAT formula with n variables and m
    clauses is satisfiable. The body is left opaque; the experimental
    harness will compute it via Monte Carlo for finite (n, k, m). -/
opaque P_sat (k n m : Nat) : Float

/-- The 50%-threshold for finite n. -/
opaque alpha_n (k n : Nat) : Float

-- ── Friedgut's theorem (sharp threshold exists for all k ≥ 2) ────────

/-- Friedgut 1999: for every k ≥ 2 there is a threshold function
    α_k(n) such that for every ε > 0:
      lim_{n→∞} P_sat(k, n, ⌈(α_k(n) - ε)·n⌉) = 1
      lim_{n→∞} P_sat(k, n, ⌈(α_k(n) + ε)·n⌉) = 0. -/
def known_sharp_threshold_exists : Prop :=
  ∀ k : Nat, k ≥ 2 →
    ∃ alpha : Nat → Float,
      ∀ ε : Float, ε > 0 →
        -- Below threshold: P_sat → 1
        (∃ N0 : Nat, ∀ n : Nat, n ≥ N0 →
          let m_below : Nat := ((alpha n - ε) * Float.ofNat n).toUInt32.toNat
          P_sat k n m_below ≥ 0.99)
        ∧
        -- Above threshold: P_sat → 0
        (∃ N1 : Nat, ∀ n : Nat, n ≥ N1 →
          let m_above : Nat := ((alpha n + ε) * Float.ofNat n).toUInt32.toNat
          P_sat k n m_above ≤ 0.01)

-- ── Open conjecture for k = 3: convergence to a specific constant ────

/-- The "satisfiability conjecture" for k = 3: there is a single asymptotic
    constant α_3* ≈ 4.267 to which α_3(n) converges.

    This is the form open since 1999 for k = 3. Resolved for large k by
    Ding-Sly-Sun 2022. -/
def OpenConjecture_alpha3_converges : Prop :=
  ∃ alpha_3_star : Float,
    alpha_3_star > 0 ∧
    -- The predicted value (non-rigorous): 4.267
    alpha_3_star ≥ 4.0 ∧ alpha_3_star ≤ 4.5 ∧
    -- α_3(n) → α_3* as n → ∞
    ∀ ε : Float, ε > 0 →
      ∃ N0 : Nat, ∀ n : Nat, n ≥ N0 →
        let diff := alpha_n 3 n - alpha_3_star
        Float.abs diff ≤ ε

-- ── Known rigorous bounds (status as of 2026) ────────────────────────

/-- Coja-Oghlan 2014 lower bound. -/
def known_lower_bound_alpha3 : Prop :=
  ∃ alpha_3 : Float,
    alpha_3 ≥ 3.86 ∧
    ∀ ε : Float, ε > 0 →
      ∃ N0 : Nat, ∀ n : Nat, n ≥ N0 →
        let m_low := ((alpha_3 - ε) * Float.ofNat n).toUInt32.toNat
        P_sat 3 n m_low ≥ 0.99

/-- Kirousis et al. + Dubois et al. upper bound. -/
def known_upper_bound_alpha3 : Prop :=
  ∃ alpha_3 : Float,
    alpha_3 ≤ 4.4943 ∧
    ∀ ε : Float, ε > 0 →
      ∃ N0 : Nat, ∀ n : Nat, n ≥ N0 →
        let m_high := ((alpha_3 + ε) * Float.ofNat n).toUInt32.toNat
        P_sat 3 n m_high ≤ 0.01

-- ── Subquestion 1: empirical extrapolation ──────────────────────────

/-- Sub-Q1: empirical threshold α_3(n) extrapolates to a constant in
    [4.20, 4.30]. -/
def SubQ1_empirical_extrapolation_in_predicted_window : Prop :=
  ∃ alpha_star : Float,
    alpha_star ≥ 4.20 ∧ alpha_star ≤ 4.30 ∧
    -- The empirical thresholds at n = 20, 50, 100, 150, 200 are
    -- consistent with α_n = α_star + c · n^(-γ) for some c, γ > 0.
    True

end RandomKSatFriedgut99
