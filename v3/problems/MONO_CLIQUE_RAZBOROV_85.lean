/-
  v3/problems/MONO_CLIQUE_RAZBOROV_85.lean

  Formal statement of the Razborov–Alon–Boppana monotone CLIQUE lower
  bound and the open question (closing the gap from k ≤ (log n)^(1/2)
  to k = n^δ).

  This file is a *statement-only* record; we do not prove the known
  lower bound here, nor the open conjecture. The purpose is to make the
  statement precise enough that downstream `Strategy` records and
  `Finding` records can refer to a unique formal object.

  Conventions:
    - No Mathlib dependency. Stdlib only.
    - Bool functions are encoded as `List Bool → Bool` so that they can
      be evaluated on graphs encoded as edge-indicator lists.
    - Monotone circuit size is encoded abstractly via the inductive type
      `MonotoneCircuit` below.

  Build: lean (no lake config needed; this file is self-contained).
-/

set_option linter.unusedVariables false
set_option autoImplicit false

namespace MonoCliqueRazborov85

-- ── Boolean functions and inputs ──────────────────────────────────────

/-- Boolean function on n bits. -/
abbrev BoolFunc (n : Nat) := (List Bool) → Bool

-- ── Monotone circuits ─────────────────────────────────────────────────

/-- A monotone Boolean circuit over `n` input bits.
    Constructors: input variable, AND, OR. Note the *absence* of NOT. -/
inductive MonotoneCircuit (n : Nat) : Type where
  | var (i : Nat) (h : i < n) : MonotoneCircuit n
  | const (b : Bool)          : MonotoneCircuit n
  | and (c1 c2 : MonotoneCircuit n) : MonotoneCircuit n
  | or  (c1 c2 : MonotoneCircuit n) : MonotoneCircuit n

/-- Evaluate a monotone circuit on a length-n input. -/
def MonotoneCircuit.eval {n : Nat} (c : MonotoneCircuit n) (xs : List Bool) : Bool :=
  match c with
  | .var i _      => (xs[i]?).getD false
  | .const b      => b
  | .and c1 c2    => c1.eval xs && c2.eval xs
  | .or  c1 c2    => c1.eval xs || c2.eval xs

/-- Circuit size: number of internal AND/OR gates. -/
def MonotoneCircuit.size {n : Nat} : MonotoneCircuit n → Nat
  | .var _ _      => 0
  | .const _      => 0
  | .and c1 c2    => 1 + c1.size + c2.size
  | .or  c1 c2    => 1 + c1.size + c2.size

/-- A monotone circuit `c` computes a function `f` if they agree on all inputs. -/
def Computes {n : Nat} (c : MonotoneCircuit n) (f : BoolFunc n) : Prop :=
  ∀ xs : List Bool, xs.length = n → c.eval xs = f xs

/-- The minimum monotone-circuit size for `f`. -/
def monoSize {n : Nat} (f : BoolFunc n) (s : Nat) : Prop :=
  (∃ c : MonotoneCircuit n, Computes c f ∧ c.size = s) ∧
  (∀ c : MonotoneCircuit n, Computes c f → s ≤ c.size)

-- ── The k-CLIQUE function ─────────────────────────────────────────────

/-- We encode a graph on `n` vertices as a list of `C(n,2)` edge bits.
    The pairing `(i, j) ↦ index` is left abstract here. -/
def edgeCount (n : Nat) : Nat := n * (n - 1) / 2

/-- The k-CLIQUE function: input is a graph on n vertices (as edge-indicator
    list of length `edgeCount n`); output is 1 iff the graph contains a
    k-clique. The body is left as a placeholder; a concrete encoding is
    instantiated by the experimental harness. -/
opaque kClique (n k : Nat) : BoolFunc (edgeCount n)

-- ── The known lower bound (Razborov 1985 + Alon-Boppana 1987) ────────

/-- The known monotone lower bound: for k ≤ (log n)^(1/2), there exists
    a constant c > 0 such that monoSize(k-CLIQUE, n) ≥ n^(c·k).

    This is a *statement* of the known theorem; the proof is in the
    cited papers and is NOT formalized here. -/
def known_lower_bound : Prop :=
  ∃ c : Float,
    c > 0 ∧
    ∀ n k : Nat,
      n ≥ 64 →
      -- The condition "k ≤ (log n)^(1/2)" is morally checked in the
      -- semantic intent; we encode it abstractly by quantifying over
      -- pairs (n, k) for which Alon-Boppana applies.
      k * k ≤ n.log2 →
      ∃ s : Nat,
        monoSize (kClique n k) s ∧
        s ≥ Nat.pow n ((c * Float.ofNat k).toUInt32.toNat)

-- ── The open conjecture (closing the gap to k = n^δ) ─────────────────

/-- The open question we want to investigate: can the Razborov-Alon-Boppana
    range be extended to k = n^δ for some fixed δ > 0?

    Conjectured TRUE by community lore; no proof and no disproof. -/
def OpenConjecture_extend_to_n_to_delta : Prop :=
  ∃ δ : Float,
    δ > 0 ∧ δ ≤ 1 ∧
    ∃ c : Float,
      c > 0 ∧
      ∀ n k : Nat,
        n ≥ 1024 →
        (Float.ofNat k) ≤ Float.ofNat n ^ δ →
        ∃ s : Nat,
          monoSize (kClique n k) s ∧
          s ≥ Nat.pow n ((c * Float.ofNat k).toUInt32.toNat)

-- ── Subquestion 1: empirical approximation-polynomial degree ─────────

/-- The minimum degree of a polynomial approximator agreeing with k-CLIQUE
    on the k-subsets of [n]. This is the central object measured by
    sub-question 1 (see TOML).

    Left opaque here; the experimental harness will compute it via
    explicit LP (Sherali–Adams hierarchy) for small n. -/
opaque approximatorDegree (n k : Nat) : Nat

/-- Sub-question 1 as a Prop: "Does approximatorDegree exhibit a phase
    transition at k ≈ (log n)^(1/2)?" -/
def SubQ1_degree_phase_transition : Prop :=
  -- We say a phase transition exists if there is a threshold function
  -- t(n) such that approximatorDegree grows polynomially below t(n) and
  -- superpolynomially above. For Lean-purpose we state this abstractly.
  ∃ threshold : Nat → Nat,
    (∀ n : Nat, n ≥ 32 →
       (∀ k : Nat, k ≤ threshold n → approximatorDegree n k ≤ k * k)) ∧
    (∀ n : Nat, n ≥ 32 →
       (∀ k : Nat, k > threshold n → approximatorDegree n k > n))

end MonoCliqueRazborov85
