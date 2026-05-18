/-
  v3/problems/3SUM_FINEGRAINED.lean

  Formal statement of the 3SUM problem and the 3SUM conjecture.
-/

set_option linter.unusedVariables false
set_option autoImplicit false

namespace ThreeSumFineGrained

-- ── The 3SUM decision problem ─────────────────────────────────────────

/-- Input: a list of integers. Output: true iff some three of them sum to 0.
    Implementation via triple-nested fold over indices. -/
def threeSum (xs : List Int) : Bool := Id.run do
  let n := xs.length
  for i in [0:n] do
    for j in [i+1:n] do
      for k in [j+1:n] do
        let ai := (xs[i]?).getD 0
        let aj := (xs[j]?).getD 0
        let ak := (xs[k]?).getD 0
        if ai + aj + ak = 0 then return true
  return false

-- ── Computational models ──────────────────────────────────────────────

/-- Computational time on a word RAM with word size w(n) = O(log n).
    Abstract; the experimental harness measures actual cycles. -/
opaque time_word_ram (algorithm_id : String) (n : Nat) : Nat

/-- Number of comparisons in a linear decision tree. -/
opaque ldt_comparisons (algorithm_id : String) (n : Nat) : Nat

-- ── Known upper bound: textbook O(n²) ─────────────────────────────────

def known_upper_bound_textbook : Prop :=
  ∃ C : Nat,
    ∀ n : Nat, n ≥ 3 →
      time_word_ram "textbook_sort_two_pointer" n ≤ C * n * n

-- ── Baran–Demaine–Pătraşcu O(n²/log² n) ──────────────────────────────

def known_upper_bound_bdp : Prop :=
  ∃ C : Nat,
    ∀ n : Nat, n ≥ 8 →
      time_word_ram "baran_demaine_patrascu" n ≤
        (let logn := n.log2
         if logn ≥ 2 then C * n * n / (logn * logn) else C * n * n)

-- ── Known lower bound: Linear Decision Tree Ω(n²) ─────────────────────

def known_lower_bound_ldt : Prop :=
  ∃ c : Nat,
    ∀ algorithm_id : String,
      ∀ n : Nat, n ≥ 8 →
        ldt_comparisons algorithm_id n ≥ c * n * n / 8  -- mock constant

-- ── The 3SUM conjecture (open) ────────────────────────────────────────

/-- The 3SUM conjecture: for every ε > 0, no word-RAM algorithm achieves
    O(n^(2-ε)). Currently no unconditional lower bound; this is a
    *conjecture* used as a hypothesis in fine-grained reductions. -/
def Open_3SUM_conjecture : Prop :=
  ∀ epsilon : Float, epsilon > 0 →
    ¬ ∃ algorithm_id : String,
      ∃ C : Nat,
        ∀ n : Nat, n ≥ 100 →
          let exponent : Float := 2.0 - epsilon
          time_word_ram algorithm_id n ≤
            C * (Float.ofNat n ^ exponent).toUInt32.toNat

-- ── Sub-question 1: empirical scaling on adversarial inputs ──────────

/-- Empirical scaling exponent of a 3SUM algorithm on an input class. -/
opaque empiricalExponent (algorithm_id input_class : String) : Float

/-- Sub-Q1: the empirical exponent of the BDP algorithm on adversarial
    inputs is in [1.95, 2.0], not the asymptotic 2 − ε predicted by the
    O(n²/log² n) analysis. -/
def SubQ1_bdp_empirical_exponent_near_2 : Prop :=
  let e := empiricalExponent "baran_demaine_patrascu" "adversarial_bdp_hostile"
  e ≥ 1.95 ∧ e ≤ 2.0

-- ── Sub-question 3: distribution-specific speedups ───────────────────

/-- Sub-Q3: there is no natural input distribution (uniform, Gaussian,
    arithmetic-progression-rich) on which a sub-quadratic average-case
    algorithm is known empirically. -/
def SubQ3_no_natural_distribution_sub_quadratic : Prop :=
  ∀ distribution_id : String,
    distribution_id ∈ ["uniform", "gaussian", "ap_rich"] →
    empiricalExponent "textbook_sort_two_pointer" distribution_id ≥ 1.90

end ThreeSumFineGrained
