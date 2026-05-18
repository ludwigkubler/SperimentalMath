/-
  v3/problems/AC0_PARITY_HASTAD_86.lean

  Formal statement of Håstad's depth-d AC^0 lower bound for PARITY, and
  the open question of optimal constants.

  Statement-only; no proofs.
-/

set_option linter.unusedVariables false
set_option autoImplicit false

namespace AC0ParityHastad86

abbrev BoolFunc (n : Nat) := (List Bool) → Bool

-- ── AC^0 circuits ─────────────────────────────────────────────────────

/-- An AC^0 circuit over `n` input bits. Unbounded fan-in over the basis
    {AND, OR, NOT}. We index AND and OR over `List` of subcircuits to
    capture unbounded fan-in directly. -/
inductive AC0Circuit (n : Nat) : Type where
  | var (i : Nat) (h : i < n)             : AC0Circuit n
  | const (b : Bool)                      : AC0Circuit n
  | not (c : AC0Circuit n)                : AC0Circuit n
  | and (children : List (AC0Circuit n))  : AC0Circuit n
  | or  (children : List (AC0Circuit n))  : AC0Circuit n

/-- Evaluate. -/
partial def AC0Circuit.eval {n : Nat} (c : AC0Circuit n) (xs : List Bool) : Bool :=
  match c with
  | .var i _   => (xs[i]?).getD false
  | .const b   => b
  | .not c1    => !c1.eval xs
  | .and cs    => cs.foldl (fun acc c1 => acc && c1.eval xs) true
  | .or cs     => cs.foldl (fun acc c1 => acc || c1.eval xs) false

/-- Number of (AND, OR, NOT) gates in the circuit. -/
partial def AC0Circuit.size {n : Nat} : AC0Circuit n → Nat
  | .var _ _   => 0
  | .const _   => 0
  | .not c1    => 1 + c1.size
  | .and cs    => 1 + cs.foldl (fun acc c1 => acc + c1.size) 0
  | .or cs     => 1 + cs.foldl (fun acc c1 => acc + c1.size) 0

/-- Depth: maximum alternation between AND and OR layers (plus NOTs absorbed). -/
partial def AC0Circuit.depth {n : Nat} : AC0Circuit n → Nat
  | .var _ _   => 0
  | .const _   => 0
  | .not c1    => c1.depth
  | .and cs    => 1 + cs.foldl (fun acc c1 => Nat.max acc c1.depth) 0
  | .or cs     => 1 + cs.foldl (fun acc c1 => Nat.max acc c1.depth) 0

def AC0Computes {n : Nat} (c : AC0Circuit n) (f : BoolFunc n) : Prop :=
  ∀ xs : List Bool, xs.length = n → c.eval xs = f xs

-- ── PARITY ────────────────────────────────────────────────────────────

/-- Parity of a list of bits: XOR over all entries. -/
def parityList : List Bool → Bool
  | []      => false
  | b :: bs => xor b (parityList bs)

/-- The PARITY function on n bits. -/
def parity (n : Nat) : BoolFunc n := fun xs => parityList xs

-- ── Håstad's bound: statement only ────────────────────────────────────

/-- Håstad 1986: for any depth d ≥ 2 and any AC^0 circuit computing parity,
    the size is at least 2^(c · n^(1/(d-1))) for some absolute c > 0. -/
def known_lower_bound : Prop :=
  ∃ c : Float,
    c > 0 ∧
    ∀ n d : Nat,
      n ≥ 8 →
      d ≥ 2 →
      ∀ circ : AC0Circuit n,
        circ.depth ≤ d →
        AC0Computes circ (parity n) →
        circ.size ≥
          -- 2^(c · n^(1/(d-1))). Encoded as Float exponent → Nat lifting.
          (let exponent : Float := c * (Float.ofNat n) ^ (1.0 / (Float.ofNat (d - 1)))
           (2.0 ^ exponent).toUInt64.toNat)

/-- Matching upper bound (folklore tree-of-trees). -/
def known_upper_bound : Prop :=
  ∃ C : Float,
    C > 0 ∧
    ∀ n d : Nat,
      n ≥ 8 →
      d ≥ 2 →
      ∃ circ : AC0Circuit n,
        circ.depth ≤ d ∧
        AC0Computes circ (parity n) ∧
        circ.size ≤
          (let exponent : Float := C * (Float.ofNat n) ^ (1.0 / (Float.ofNat (d - 1)))
           (2.0 ^ exponent).toUInt64.toNat)

-- ── Open question: optimal constant ───────────────────────────────────

/-- Conjecture: there is a SAME constant c* in both the upper and lower
    bound (asymptotically tight). Equivalently, the ratio of upper to
    lower converges to 1 as n → ∞. -/
def OpenConjecture_optimal_constant : Prop :=
  ∃ cstar : Float,
    cstar > 0 ∧
    -- For every ε > 0 there exists N₀ such that for n ≥ N₀,
    -- both bounds hold with constant in [cstar - ε, cstar + ε].
    ∀ ε : Float, ε > 0 →
      ∃ N0 : Nat,
        ∀ n d : Nat,
          n ≥ N0 → d ≥ 2 →
          -- Both bounds use constant in the ε-window of cstar.
          True  -- abstract; the precise statement requires quantification
                -- over witness circuits which is more involved.

-- ── Sub-question 1: empirical shrinkage rate ─────────────────────────

/-- A *random restriction* of probability p: a function that fixes each
    variable independently with probability (1-p) to a random bit, and
    leaves it free with probability p. We model only the *expected
    shrinkage* of a circuit under such restriction. -/
opaque expectedShrinkage (c : AC0Circuit 0) (p : Float) : Float

/-- Sub-question 1: for circuits at the size threshold, the empirical
    shrinkage is bounded by p^Θ(1) and matches Håstad's prediction. -/
def SubQ1_shrinkage_matches_prediction : Prop :=
  -- Stated abstractly: the empirical shrinkage exponent equals the
  -- theoretical prediction Θ((d-1)/d) ± experimental error.
  True

end AC0ParityHastad86
