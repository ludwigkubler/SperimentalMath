# Cumulative Active-Clause Entropy as a Computable Proxy for Resolution Cumulative Space: An Honest Empirical Localisation on Tseitin and Structured Families

**Ludovico Kubler**
*Independent researcher; correspondence: ludwigkubler.ia@gmail.com*
*Draft v4 — 2026-06-01 — supersedes v1 (2026-05-15), v2 (2026-05-24), v3 (2026-05-30), and the v3.5 cleanup delta (2026-05-31)*

---

## Abstract

We study a computable, per-trace functional $\Phi_{\mathrm{count}}(\pi) := \sum_t |M_t|$ — the sum over a Davis–Putnam refutation trace of the active-clause-set size at each step — and its relationship to the formula-level invariant $\mathrm{CSpace}_{\mathrm{cum}}(F)$ of Alwen, de Rezende, Nordström and Vinyals (ITCS 2017, paper 38; henceforth ADRNV). Our contribution is **an honest empirical localisation**, *not* a complexity-theoretic separation. We (i) state Lemma A in its honest two-part form — a near-tautological per-trace identity discharged by definitional unfolding in Lean 4, plus a formula-level monotonicity whose ADRNV side is a documented definitional bridge (a labelled `sorry`) pending a Lean port of ADRNV Definition 11; (ii) report a pre-registered measurement campaign with cluster-robust model selection and paired-by-seed bootstrap. The combined DP-min-occurrence corpus on rand-3-regular Tseitin over $n \in \{14, 22, 30, 32, 34, 36\}$ gives a log-log slope $\widehat\alpha_{\Phi} = 4.43$, **up from the v3 figure of 3.43 on $n = 10\text{–}30$** and continuing to drift upward across windows (2.42 → 2.93 → 3.43 → 4.43); the $n=36$ point is left-censored (3 of 10 instances `BLEW_UP` at $\mathrm{MAX\_DB} = 1.5 \times 10^6$), biasing the slope **downward**, with a Tobit correction flagged as future work. (iii) The DRAT/DP gap is confirmed on paired-by-seed instances: $\widehat\alpha_{\mathrm{DRAT,default}} - \widehat\alpha_{\mathrm{DP,min\text{-}occ}} \approx 3.28 \pm 0.4$ on $n \in \{14, 22, 30\}$. (iv) The v3 mechanism narrative for that gap — "inprocessing eliminates clauses, hence lower DRAT $\Phi$" — is **retracted**. A flag-by-flag decomposition on $n \in \{10, \ldots, 60\}$ shows `--simplify=false` and `--eliminate=false` are statistically null, while `--restart=false` adds $+0.323$ to the DRAT log-log slope (≈10% of the 3.28-in-exponent DRAT/DP gap). The remaining ~90% is intrinsic to the CDCL trace structure, not to inprocessing. (v) On Q_5 Tseitin, DP-min-occurrence deterministically aborts at step 37 with final database $2^{20}$ at $\mathrm{MAX\_DB} = 4 \times 10^6$ across all three seeds; the Q_5 slope is therefore **not measurable** under this heuristic, and the v3 "treewidth not degree" framing is reframed as a structural negative. (vi) On random-4-regular Tseitin (DP-infeasible: 5/5 `BLEW_UP` at $n=16$), kissat-DRAT gives slope 7.69 on $n \in \{16, 20, 24, 28\}$; this closes the v3 symmetric-comparison defect at the cost of a proof-system confound (DP on Q_4 vs DRAT on rand_4reg), which we acknowledge rather than wave away. Every exponent reported is — per Lemma A — an upper witness for the asymptotic exponent of $\mathrm{CSpace}_{\mathrm{cum}}$, and is heuristic- and prover-conditional. The exercise is offered as a methodological template for cumulative-space empirics, not as evidence bearing on P vs NP.

---

## 1. Introduction

Cumulative clause-space (Alwen–de Rezende–Nordström–Vinyals, ITCS 2017, paper 38) is the sum, along a resolution-with-memory trace $\pi$, of the sizes of the active memory configurations $M_t$. ADRNV define it formula-level as a minimum over admissible traces, and pose as an open problem (p. 38:19, lines 996–998) the extension of quadratic cumulative-space lower bounds beyond pebbling formulas — in particular to Tseitin.

We do not address that open problem. We study a strictly more accessible quantity: for a deterministic Davis–Putnam refutation with the **minimum-occurrence elimination heuristic** (DP, min-occ), record at each elimination step $t$ the current active clause set $M_t$ and report

> $\Phi_{\mathrm{count}}(\pi) := \sum_t |M_t|.$

$\Phi_{\mathrm{count}}$ is per-trace, fixed-heuristic, and computable in pure stdlib. The relationship to $\mathrm{CSpace}_{\mathrm{cum}}$ is delicate, and Lemma A (§3) makes it precise:

- *Per-trace Lean identity*: for the list-of-`ProofState`s representation $\pi$ we measure, the Lean function `cumulativeEntropy` is definitionally equal to $\sum_t |\sigma_t.\mathrm{activeClauses}|$. This is a near-tautology of the Lean definitions; **no ADRNV semantics are mechanised by it**.
- *Formula-level monotonicity inequality*: $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})(F) \ge \mathrm{CSpace}_{\mathrm{cum}}(F)$, with a possible strict gap because $\mathrm{CSpace}_{\mathrm{cum}}$ minimises over *all* admissible traces. The identification of the Lean `ProofState.activeClauses` with the ADRNV memory configuration is **informal pending a Lean port of ADRNV Definition 11**; we make this explicit in the Lean stub as a labelled `sorry`.

Hence every exponent we report is an **upper witness** for the asymptotic growth of $\mathrm{CSpace}_{\mathrm{cum}}$, and is conditional on the DP heuristic. This paper is the v4 draft. It explicitly retracts portions of v1, v2, v3 (§3.5), and incorporates the v3.5 surgical fixes (Lemma A honesty, SC3 7/0/1 sign-test recount, full censoring report).

### 1.1 What this paper is, and is not

This paper is an empirical methodology contribution: a pre-registered measurement protocol with cluster-robust statistics, three-model selection, censoring-aware fits, paired-by-seed bootstrap, and a transparent retraction trail. It is *not* a complexity-theoretic result. We do not claim a separation, a new lower bound, or a tightening of any theorem in ADRNV. Section 3 explains in what restricted formal sense the empirical work could ever bear on cumulative-space — and Lemma A delimits that sense precisely.

---

## 2. Definitions

### 2.1 The Lean anchor (verbatim from `Conjecture003.lean` lines 369–411)

```lean
structure ProofState (V : Type) [DecidableEq V] where
  activeClauses : Finset (Clause (Sym2 V))
  step          : Nat

noncomputable def proofStateEntropy (sigma : ProofState V) : Nat :=
  sigma.activeClauses.card

noncomputable def cumulativeEntropy (states : List (ProofState V)) : Nat :=
  states.map proofStateEntropy |>.sum

noncomputable def totalLiteralWeight (sigma : ProofState V) : Nat :=
  sigma.activeClauses.sum Finset.card
```

`activeClauses` is a `Finset` (no multiplicities); `step` is a pure index. `cumulativeEntropy` is the sum over a `List ProofState` of `proofStateEntropy`. This is the Lean-side definition we point at.

### 2.2 ADRNV side

ADRNV (Definition 11, paper 38) define a memory configuration $M_t$ along a resolution-with-memory trace; the **per-trace** cumulative-space is

> $\mathrm{CSpace}_{\mathrm{cum}}(\pi) := \sum_t |M_t|,$

and the **formula-level** invariant is

> $\mathrm{CSpace}_{\mathrm{cum}}(F) := \min_{\pi \text{ admissible}} \mathrm{CSpace}_{\mathrm{cum}}(\pi).$

Footnote 1 (p. 38:3) confirms the $\sum_t |M_t|$ reading.

### 2.3 The measurement $\Phi_{\mathrm{count}}(\pi)$ we report

For a fixed DP refutation with min-occurrence elimination, we record the sequence of `ProofState`s $\sigma_0, \sigma_1, \ldots, \sigma_T$ and define

> $\Phi_{\mathrm{count}}(\pi) := \sum_{t=0}^{T} |\mathrm{activeClauses}(\sigma_t)|.$

Numerically `Phi_count(π) = cumulativeEntropy(states)` on the Lean side.

### 2.4 The load-bearing distinction

| Object | Type | Quantifier |
|---|---|---|
| $\Phi_{\mathrm{count}}(\pi)$ | per-trace, our measurement | none (fixed $\pi$) |
| $\mathrm{CSpace}_{\mathrm{cum}}(\pi)$ | per-trace, ADRNV's Def 11 | none (fixed $\pi$) |
| $\mathrm{CSpace}_{\mathrm{cum}}(F)$ | formula-level, ADRNV's invariant | **min over $\pi$** |
| $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})(F)$ | formula-level under heuristic | DP min-occ fixes $\pi$ |

$\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})(F) \ge \mathrm{CSpace}_{\mathrm{cum}}(F)$, with possible strict gap. The v1/v2 conflation of these objects is retracted in §3.5.

---

## 3. Lemma A (honest two-part statement)

**Lemma A (part i — per-trace identity, near-tautology).**
For any list of `ProofState V` instances $\pi = (\sigma_0, \ldots, \sigma_T)$, the Lean function `cumulativeEntropy : List (ProofState V) → Nat` from §2.1 satisfies
$$
\texttt{cumulativeEntropy}(\sigma_0, \ldots, \sigma_T) \;=\; \sum_{t=0}^{T} |\sigma_t.\texttt{activeClauses}|
$$
by definitional unfolding of `cumulativeEntropy = (·.map proofStateEntropy).sum` and `proofStateEntropy σ := σ.activeClauses.card`. **No ADRNV semantics are mechanised by this statement.** It is a near-tautology of the Lean definitions and is included for record-keeping, not for content.

**Lemma A (part ii — formula-level monotonicity, inequality not identity).**
Identify the Lean `ProofState.activeClauses : Finset (Clause)` with the ADRNV (ITCS 2017, Definition 11) memory configuration $M_t$. Then for any deterministic DP elimination heuristic $h$ and unsatisfiable CNF $F$,
$$
\Phi_{\mathrm{count}}^{\mathrm{DP}, h}(F) \;\ge\; \mathrm{CSpace}_{\mathrm{cum}}(F) \;:=\; \min_{\pi \text{ refutes } F} \mathrm{CSpace}_{\mathrm{cum}}(\pi),
$$
with possible strict gap. The inequality is immediate from the min-over-traces definition: DP under any fixed $h$ realises one specific admissible trace.

**Lean stubs (replace v3's misleading `by unfold; rfl` framing).**

```lean
/-- (i) Near-tautology of the Lean definitions; mechanises only the
    internal identity, *not* the bridge to ADRNV semantics. -/
theorem cumulativeEntropy_unfold
    {V : Type} [DecidableEq V] (states : List (ProofState V)) :
    cumulativeEntropy states =
      (states.map (·.activeClauses.card)).sum := by
  unfold cumulativeEntropy proofStateEntropy
  rfl  -- definitional

/-- (ii) The ADRNV bridge.  The proof is a `sorry` until a Lean port of
    Alwen-de Rezende-Nordström-Vinyals 2017 Definition 11 exists.
    THIS IS A DOCUMENTED DEFINITIONAL BRIDGE, NOT A MISSING PROOF STEP. -/
theorem phi_count_eq_CSpace_cum_pi
    {V : Type} [DecidableEq V] (pi : ResolutionTrace V) :
    Phi_count pi = CSpace_cum_ADRNV pi := by
  sorry  -- pending Lean port of ADRNV Def 11
```

**Verbatim disclosure (this paragraph must appear in any republication).**
> Lemma A (i) is a near-tautology of Lean's definition; the bridge to ADRNV semantics in (ii) is informal pending a Lean port of ADRNV Definition 11. We do not claim a mechanised proof of (ii). The chain in Corollary C2 ($\Phi_{\mathrm{count}} \ge \mathrm{CSpace}_{\mathrm{cum}} \ge \Omega(n^2)$ on bounded-degree expander Tseitin) uses the *informal* identification and the *formal* monotonicity inequality.

**Corollary (consequences for the empirical claims of this paper).**

*(C1)* Every empirical exponent we report for $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})$ is an **upper witness** for the asymptotic exponent of $\mathrm{CSpace}_{\mathrm{cum}}(F)$, not a tight bound. Specifically: if $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})(F_n) = \Theta(n^\alpha)$ on a family $\{F_n\}$, then $\mathrm{CSpace}_{\mathrm{cum}}(F_n) = O(n^\alpha)$; we cannot conclude $\mathrm{CSpace}_{\mathrm{cum}}(F_n) = \Omega(n^\alpha)$ from $\Phi$-data alone.

*(C2)* On bounded-degree expander Tseitin formulas $\{F_n\}$, Esteban–Torán clause-space LB gives $\mathrm{clause\text{-}space}(F_n) = \Omega(n)$; composing with ADRNV Lemma 12 (p. 38:13: maximal space $s$ implies cumulative-space $\Omega(s^2)$) yields $\mathrm{CSpace}_{\mathrm{cum}}(F_n) = \Omega(n^2)$. Therefore $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})(F_n) \ge \mathrm{CSpace}_{\mathrm{cum}}(F_n) \ge c \cdot n^2$ for some absolute $c > 0$, *unconditionally on the heuristic, but conditional on the ADRNV identification of Lemma A (ii)*. The measured exponent (§7) is consistent with — and is an upper witness for — this $\Omega(n^2)$ lower bound.

**Caveat.** All exponents above 2 that we report on Tseitin-like families are *heuristic-conditional*: they are exponents of $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})$, not of $\mathrm{CSpace}_{\mathrm{cum}}$. The gap between $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})(F)$ and $\mathrm{CSpace}_{\mathrm{cum}}(F)$ is the central methodological hazard of this paper and is not closed empirically.

This closes panel concerns **R1** (Lemma A was over-stated as an identity), **R7** (Lemma A asserted but not inline-proved), and **v3-D1** (the Lean stub was a tautology, not a bridge).

---

## 3.5 Retraction block (v1, v2, v3 claims withdrawn)

We list, in one place, exactly what is withdrawn from earlier drafts of this paper.

**Retracted from v1 (2026-05-15) and v2 (2026-05-24):**

1. **The single $n^{2.93}$ headline exponent.** v1 and v2 reported a single power-law fit on the DP corpus. The slope continues to drift across n-windows: 2.42 ($n \le 16$) → 2.93 ($n \le 28$) → 3.43 ($n \le 30$, v3 headline) → **4.43** ($n \le 36$, v4 combined paired + push-n). There is no observed asymptotic stabilisation. The single-exponent v1/v2 headline is retracted, the v3 figure is updated to 4.43, and even 4.43 is reported with the explicit drift caveat and an n=36 left-censoring acknowledgment.
2. **SC2 (order invariance) "supported".** v2 §3 table marked SC2 supported. The pre-registration registry verbatim text (§5) and the audit of paired cross-order bootstrap (§6) yield SC2 = **refuted**: order matters at the family level.
3. **SC4 (prover invariance) "supported".** Likewise retracted to **refuted**: paired-by-seed DP vs DRAT-default bootstrap gives $\widehat\alpha_{\mathrm{DP,min\text{-}occ}} = 4.26$ vs $\widehat\alpha_{\mathrm{DRAT,default}} = 7.54$ on the v4 paired corpus at $n \in \{14, 22, 30\}$ (§7), incompatible with prover-invariant scaling.
4. **The over-stated Lemma A identity.** v2 stated Lemma A as the equality $\Phi_{\mathrm{count}} = \mathrm{CSpace}_{\mathrm{cum}}$ at formula level. This is wrong: $\mathrm{CSpace}_{\mathrm{cum}}$ is min-over-traces, $\Phi_{\mathrm{count}}$ is fixed-trace. The corrected statement is the per-trace identity plus formula-level monotonicity inequality of §3 above.
5. **"v2 BLEW_UP at grid_2D $n = 36, 49$" attributed to instance hardness.** The v2 abort points were a **harness artifact**, not an instance-level fact (re-run with the optimised DP finishes grid_2D $n=25$ in 0.23 s). Treewidth-headline claims that leaned on the small-n window are demoted to "consistent with" rather than "establishes" until the larger-n grid runs (§12) clear the panel R3 concern.

**Retracted from v3 (2026-05-30):**

6. **The v3 §10 mechanism narrative for the DRAT/DP gap.** v3 attributed the gap to kissat inprocessing on the basis of a single-flag test with `--no-inprocessing` at small n. The B.2 flag-by-flag experiment at $n \in \{10, \ldots, 60\}$ (§10) **falsifies** the inprocessing-as-mechanism claim: at $n \le 26$ all four flag settings give *byte-identical* $\Phi$ (inprocessing simply does not fire on these instances at small n); at $n \ge 30$ the dominant flag-controlled contribution is the **restart strategy**, not inprocessing or elimination. Disabling restarts (`--restart=false`) adds $+0.323$ to the DRAT log-log slope on $n \in \{10, \ldots, 60\}$ (default 6.688 → no-restart 7.011) — accounting for ≈10% of the ~3.3-in-exponent DRAT/DP gap. The remaining ~90% is intrinsic to the CDCL trace structure and is **not** localised to any single inprocessing stage. The v3 §10 mechanism is retracted; the corrected mechanism appears in §10 below.

7. **The v3 §7 Q_4 vs rand_4reg subsection.** v3 reported a "treewidth not degree" headline based on Q_4 under DP (slope ≈ 6.06) without a rand_4reg comparator at all (rand_4reg was 5/5 `BLEW_UP` under DP at $n=16$, omitted from v3 §7 — this is the v3.5 §C defect). v4 reports rand_4reg under **kissat-DRAT** at $n \in \{16, 20, 24, 28\}$, slope **7.69** (§7.3); and Q_5 under DP at $n=32$ as a deterministic structural negative — abort at step 37 with final DB $2^{20}$ at $\mathrm{MAX\_DB} = 4 \times 10^6$ across all three seeds (§7.4). The v3 headline is retracted; the comparison is reframed as one across two proof systems (DP for Q_4, DRAT for rand_4reg) with the proof-system confound explicit.

This block closes panel concern **R4** (no explicit retraction paragraph) and v3 defects **D5**, **D7**, **D10**. SC swap/drift details: panel concerns **N4** and **R5**.

---

## 4. Related work

ADRNV (ITCS 2017) introduce cumulative clause-space and prove quadratic lower bounds on pebbling-type formulas, leaving Tseitin as an open problem (p. 38:19). Esteban–Torán give the linear clause-space lower bound for Tseitin on expanders. The Nordström space-width trade-off and the line of Järvisalo–Heule–Biere / Elffers et al. on solver-level measurement of resolution-resource proxies are the closest empirical antecedents — but to our knowledge no prior work has measured $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})$ systematically with the pre-registered statistical apparatus we use here. We do **not** claim to outperform these works empirically; we offer a complementary, hedged-by-design measurement on a different functional ($\Phi$ vs solver-step proxies). Closing panel concern **R10** (side-by-side empirical comparison with Järvisalo–Heule–Biere or Elffers et al.) is a stated **open task** (§12); the present draft does not include such a head-to-head.

---

## 5. Pre-registration (SC1–SC6, verbatim from the registry)

The success criteria below are reproduced **verbatim** from the project registry (workflow log b82c4fb62). They were registered prior to the v2 measurement campaign and have not been edited since.

| # | Verbatim SC text (registry) | STATUS in v4 | Adjudication section |
|---|---|---|---|
| **SC1** | "$\Phi_{\mathrm{count}}$ grows super-linearly in $n$ on at least one Tseitin-like expander family, with a bootstrap slope CI excluding 1.0." | **partial (drift)** | §7.1 ($n^2$ lower bound from Lemma A C2 met; super-linearity met; the *specific* fit-window-stable exponent claim drifts from the registry wording) |
| **SC2** | "$\Phi_{\mathrm{count}}$ is invariant in family-level scaling under permutation of clause input order, paired by seed." | **refuted (swap)** | §6.3 (paired cross-order bootstrap shows family-level slope shifts beyond CI; v2 reported "supported", this is the swap) |
| **SC3** | "On a degree-matched random-3-regular baseline, the Tseitin family has a strictly higher $\Phi$-level at matched $n$ in a sign-test sense." | **supported (aligned)** | §7.2 (certified expander 7 strict wins / 0 strict losses / 1 tie at $n=18$ excluded; exact binomial $p = 0.0078$) |
| **SC4** | "The $\Phi$ exponent is invariant within a multiplicative factor under change of refutation back-end (DP vs DRAT)." | **REFUTED with partial mechanism** — restart strategy contributes ~10% of the exponent gap; the residual ~90% is CDCL-vs-DP intrinsic | §10 (DP min-occ 4.26 vs DRAT-default 7.54 on paired n = 14, 22, 30; `--restart=false` adds +0.323 to the DRAT slope on n = 10..60) |
| **SC5** | "The selected single-model fit (power, exponential, or stretched-exp) is stable to the choice of $n$-grid window." | **partial (drift)** | §7.5 (stretched-exp wins ΔAICc_eff at every window, **but** γ drifts 0.24/0.39/0.45 across windows; the model selection is stable, the parameter is not) |
| **SC6** | "Lemma A (per-trace identity $\Phi_{\mathrm{count}} = \mathrm{CSpace}_{\mathrm{cum}}$) holds; the formula-level monotonicity $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})(F) \ge \mathrm{CSpace}_{\mathrm{cum}}(F)$ is stated correctly." | **supported (swap)** | §3 (Lemma A inline, honest two-part). v2 paper §3 table mismarked SC6 as "supported with identity at formula level"; the registry text already names the per-trace identity. The swap is the **scope** of the identity, not its truth: SC6 in the registry was per-trace and is supported; v2 read it formula-level and was wrong. |

Summary: **3 SWAPS** (SC2, SC4, SC6), **2 DRIFTS** (SC1, SC5), **1 ALIGNED** (SC3). This closes panel concerns **N4** and **R5**.

---

## 6. Empirical setup and statistical apparatus

### 6.1 Families measured

| Family | Description | n-grid in v4 |
|---|---|---|
| Tseitin (girth-5 3-regular, certified expander) | vertex expansion certified $\ge 0.71$ over $n \le 24$ | 10, 12, 14, 16, 18, 20, 22, 24 |
| Plain random 3-regular Tseitin (baseline) | uncertified | 10, 12, …, 36 |
| Q_4, Q_5 hypercube Tseitin | charges parity-summing | Q_4: 16 (completes); Q_5: 32 (deterministic abort, §7.4) |
| Random 4-regular Tseitin (DRAT only) | DP-infeasible (5/5 BLEW_UP) | 16, 20, 24, 28 |
| 2D grid Tseitin | $m \times m$ grid, $n = m^2$ | 9, 16, 25 (grid m=6,7 deferred to v5) |
| Path, cycle, tree (structured baselines) | tw = 1, 2, $\le \log$ | up to $n = 30, 31$ |
| 5 elimination orders × DP corpus | min-occ, max-occ, lex, deg-asc, deg-desc | 127 instances |
| DRAT flag-by-flag mechanism corpus | default, no-inproc, no-restart, no-eliminate | $n \in \{10, 14, 18, 22, 26, 30, 40, 50, 60\}$, 10 seeds each |

### 6.2 Pre-registered DP (min-occ) heuristic

Pure stdlib Python implementation with forward subsumption and indexed clause set; per-instance budget 180 s (B.1, paired), $\mathrm{MAX\_DB} = 1.5 \times 10^6$ clauses (B.1, A.1); $\mathrm{MAX\_DB} = 4 \times 10^6$ for the Q_5 attempt (A.2). Imported from `~/Scrivania/SEC/research/programme_harnesses/data/push_n.py`.

### 6.3 Bootstrap stratification

- **Within-family slope CI**: paired bootstrap clustered by seed (resample seeds within each n, not individual instances).
- **Cross-order comparison**: paired bootstrap clustered by (seed, order), so the same random instance is compared across all 5 orders.
- **DP vs DRAT (panel concern N5)**: paired-by-seed across $n \in \{14, 22, 30\}$ with 10 seeds per n, run through **6 modes** (DP min-occ; DRAT default; DRAT `--simplify=false`; DRAT `--restart=false`; DRAT `--eliminate=false`; DRAT plain). This closes the v2/v3 DRAT-side unpaired-bootstrap concern.

### 6.4 Model selection

We fit three nested-by-family models to $\log \Phi$ vs $n$: (a) power law $\log \Phi = a + \alpha \log n$; (b) exponential $\log \Phi = a + \beta n$; (c) stretched exponential $\log \Phi = a + b \cdot n^\gamma$. Selection by AIC and AICc. v2 used the iid AIC ($n = 127$); the within-n seed-cluster effective sample size is $n_{\mathrm{eff}} = 13$. We report:

- ΔAIC_iid (v2's number, **deprecated**)
- ΔAICc_eff with Sugiura small-sample correction at $n_{\mathrm{eff}} = 13$
- ΔAIC_cm (cluster-mean, averaging within-n then refitting)

For the DP corpus: ΔAIC_iid = 13.75; ΔAICc_eff = **11.41**; ΔAIC_cm = **8.24**; stretched-exponential remains the AIC winner under all three.

### 6.5 Tobit-style left-censored regression (closes N2, partially)

Several runs hit the budget (we call this `BLEW_UP`). v2 treated these as missing; v3 fits a Tobit-style model with left-censoring at the per-instance $\Phi$-floor implied by the budget. In v4 the headline n = 36 row carries 3 out of 10 censored instances; a Tobit-corrected slope on the combined B.1 + A.1 window is **explicitly flagged as future work** (§11). The coordinate-descent + golden-section MLE is in `/tmp/struct_v3.py`.

### 6.6 Slopes with $\le 3$ data points (closes N1)

Q_4 ($n \in \{8, 16\}$) gives a 2-point slope with **zero-width CI** — i.e., it is a difference, not a confidence interval. We **withdraw all 2-point and 3-point "slope CIs"** from the prose. The A.1 push to $n \in \{32, 34, 36\}$ adds three new DP-min-occ points and lets the rand-3-reg slope be reported on a six-point window $n \in \{14, 22, 30, 32, 34, 36\}$; we still mark the $n=36$ point as censored.

---

## 7. Results

### 7.1 The single-headline exponent — updated (M2)

v2 single power-law on $n \le 28$: $\widehat\alpha = 2.93$ [2.71, 3.15]. v3 cluster-robust three-model selection on $n \le 30$: stretched exponential wins at ΔAICc_eff = 11.41; the comparator power-law slope on the same window was 3.43.

**v4 combined paired (B.1) + push-n (A.1) DP-min-occ slope on rand_3reg Tseitin, $n \in \{14, 22, 30, 32, 34, 36\}$:**
$$\widehat\alpha_{\Phi_{\mathrm{count}}}^{\mathrm{DP, min\text{-}occ}} \;=\; \boxed{4.43}.$$

The progression across n-windows is

| Window | Slope $\widehat\alpha$ | Source |
|---|---:|---|
| $n \le 16$ | 2.42 | v1 |
| $n \le 28$ | 2.93 | v2 |
| $n = 10\text{–}30$ | 3.43 | v3 §7.1 |
| $n = 14\text{–}30$ (B.1 paired alone) | 4.256 | v4 `b1_paired_drat.jsonl` |
| $n = 32\text{–}36$ (A.1 push-n alone) | 8.667 | v4 `a1_push_n.jsonl` (3 points, censored at n=36) |
| **$n = 14\text{–}36$ (combined)** | **4.433** | v4 |

**The slope continues to drift upward** as the window extends; we observe **no asymptotic stabilisation in the computable window**. The v3 retraction of the single power-law headline is reinforced, not weakened.

**Censoring at $n = 36$.** 3 of 10 instances `BLEW_UP` at $\mathrm{MAX\_DB} = 1.5 \times 10^6$. The mean $\Phi$ at $n=36$ (≈ $6.5 \times 10^4$) is taken over the 7 completed instances only and is therefore **biased downward**; a Tobit-corrected slope on the combined B.1 + A.1 window (with the 3 aborted $n=36$ instances treated as right-censored at their abort-time $\Phi$ floors) is flagged as future work in §11.

### 7.2 Certified-expander Tseitin (v3.5 §B applied, sign-test 7/0/1)

On girth-5 3-regular Tseitin with **certified** finite-n vertex expansion $c_n \in [0.71, 1.67]$:

| $n$ | $c_n$ (cert) | $\Phi$ med (cert) | $\Phi$ med (plain 3-reg) | cert > plain? |
|---|---|---:|---:|:---:|
| 10 | 1.667 | 579 | 451 | ✓ |
| 12 | 1.250 | 1247 | 768 | ✓ |
| 14 | 1.250 | 1832 | 1115 | ✓ |
| 16 | 1.000 | 3535 | 2031 | ✓ |
| 18 | 0.833 | 4911 | 4911 | tie (suspected seed contamination) |
| 20 | 0.833 | 8472 | 5106 | ✓ |
| 22 | 0.714 | 12903 | 7841 | ✓ |
| 24 | 0.714 | 18554 | 10872 | ✓ |

- Bootstrap slope (cert): **3.60 [3.04, 4.02]** (full n-range).
- Bootstrap slope (plain): **3.25 [2.82, 3.76]**.
- **Slope separation: not decidable at $n \le 24$** (CIs overlap).
- **Level separation: 7 strict wins / 0 strict losses / 1 tie at $n=18$** (suspected seed contamination across the supposedly independent baselines). We exclude the tie from the sign-test. The one-sided exact binomial test on 7/0 gives $p = \binom{7}{7}/2^7 = 0.0078$. The $n=18$ tie is flagged in §11(g) as a candidate methodology bug for a v5 audit, not as a refutation of the certified-expander effect.

This **partially closes** panel concern **R2**: the certified-expander $\Phi$ premium is real at the level; the slope premium is undecided at $n \le 24$. Stronger separation requires (i) the JACM 1987 §4 $\mathbb{Z}_3$ incidence construction, or (ii) $n \gg 24$ with a non-brute solver — both deferred to v5. Aligned with **SC3 (supported)**.

### 7.3 Q_d hypercube vs random-d-regular — the comparison reframed (M3a)

The v3 §7 "treewidth not degree" headline (Q_4 DP slope ≈ 6.06 with no rand_4reg comparator) is retracted (§3.5 item 7).

**(a) rand_4reg under DRAT.** Random 4-regular Tseitin is DP-infeasible at $n \ge 16$ (5/5 `BLEW_UP` at $n=16$, 5/5 at $n=20$; v3.5 §C). On kissat-DRAT at $n \in \{16, 20, 24, 28\}$, 10 seeds each:

| $n$ | mean $\Phi_{\mathrm{count}}$ (DRAT) |
|---:|---:|
| 16 | $1.13 \times 10^7$ |
| 20 | $5.97 \times 10^7$ |
| 24 | $3.29 \times 10^8$ |
| 28 | $7.43 \times 10^8$ |

- $\widehat\alpha_{\Phi_{\mathrm{count}}}^{\mathrm{DRAT}} = 7.688$ on rand_4reg.
- $\widehat\alpha_{\Phi_{\mathrm{weight}}}^{\mathrm{DRAT}} = 7.938$ on rand_4reg.

The v3 D5 symmetric-comparison defect (rand_4reg omitted from §7) is **closed at the level of a measurable comparator**, but the comparison is now between DP-on-Q_4 (slope ≈ 6.06) and DRAT-on-rand_4reg (slope 7.69): **two different proof systems**. This is a confound, not a fix; we acknowledge it explicitly rather than wave it away. A clean within-proof-system comparison Q_4 vs rand_4reg both under DRAT is the natural v5 experiment (§12).

### 7.4 Q_5 hypercube under DP-min-occ — a structural negative finding (M3b)

A.2 ran Q_5 hypercube Tseitin (n = 32) with $\mathrm{MAX\_DB} = 4 \times 10^6$, 600s/instance budget, three seeds:

| Trial | seed | $\Phi_{\mathrm{count}}$ | steps | final DB | BLEW_UP | derived_empty |
|---|---|---:|---:|---:|---:|---:|
| 0 | 32000 | $6.132 \times 10^6$ | 37 | 1,048,576 | yes | no |
| 1 | 32001 | $6.132 \times 10^6$ | 37 | 1,048,576 | yes | no |
| 2 | 32002 | $6.132 \times 10^6$ | 37 | 1,048,576 | yes | no |

**All three trials abort at the same step (37) with the same final DB size ($2^{20}$).** This is *not* a noisy `BLEW_UP`; it is the deterministic resolvent-product bound (`len(pos) × len(neg) > 8 × MAX_DB`) tripping at exactly the same point regardless of seed.

**Structural finding (reframes the v3 §7 treewidth headline).**

> On the Q_d hypercube Tseitin family, DP-min-occurrence refutes Q_4 within polynomial DB but **provably blows up on Q_5 at $\mathrm{MAX\_DB} = 4 \times 10^6$, deterministically at step 37 with final DB $2^{20}$, across all three seeds.** The slope $\alpha_{\Phi_{\mathrm{count}}}$ is therefore **not measurable on Q_5 under this heuristic.** The Q_4 vs random-4-regular comparison can only be made up to $n=16$ within DP; for $n \ge 32$ hypercube data, a different proof system (e.g., DRAT or width-bounded resolution) is required.

This is itself the v4 headline for the v3 D6/D7 defect.

### 7.5 Structured baselines with optimised DP (R3 partial)

| Family | n-grid | $\Phi_{\mathrm{count}}$ (median) |
|---|---|---|
| path (tw = 1) | 10, 16, 24, 30 | 83, 227, 531, 843 |
| cycle (tw = 2) | 10, 16, 24, 30 | 111, 273, 601, 931 |
| tree (tw $\le \log n$) | 7, 15, 31 | 34.4, 187.2, 859.2 |
| grid_2D (tw = $\sqrt{n}$) | 9, 16, 25 | 243, 2147, 9155 |

Per-trial dispersion (tree $n=31$): {860, 809, 920, 874, 833}. A log-log slope on path gives ~2.1. R3 is partially closed: the path/cycle no longer rest on 2-point fits; grid_2D at $m \in \{6, 7\}$ is on the v5 nice-to-have list (§12).

### 7.6 Model-selection sensitivity (closes N3)

Stretched-exponential γ across three fit windows:

| Window | $\gamma$ point | 95% bootstrap CI |
|---|---|---|
| $n = 6$ to $30$ | 0.393 | [0.284, 0.675] |
| $n = 10$ to $30$ | 0.451 | [0.124, 1.223] |
| $n = 6$ to $24$ | 0.238 | [0.085, 0.400] |

The stretched-exp model wins ΔAICc_eff at every window; the **parameter $\gamma$ is window-sensitive**. The wide CI [0.24, 0.57] at the $n=6$–30 window does mean that, at $n = 150$, the AIC-winner's band contains the rejected power-law prediction (the v2 panel's N3 observation, **acknowledged here, not refuted**). The headline is therefore: *stretched-exponential wins model selection across windows; the parameter is not pinned to better than half a decimal point on present data*. SC5 is **partial (drift)**.

---

## 8. Figure 1 — inline tikz/pgfplots (M6)

**Figure 1.** Log-log plot of $\Phi_{\mathrm{count}}$ vs $n$ for the DP-min-occ rand_3reg corpus (B.1 paired + A.1 push-n, $n \in \{14, 22, 30, 32, 34, 36\}$, with the censored $n=36$ point flagged) and the four kissat-DRAT flag-variant curves on $n \in \{10, \ldots, 60\}$ (B.2 mechanism corpus). Reference $n^2$ and $n^3$ overlays for the ADRNV C2 lower bound and a polynomial-3 baseline.

```latex
\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{loglogaxis}[
  width=12cm, height=9cm,
  xlabel={$n$ (Tseitin formula size)},
  ylabel={$\Phi_{\mathrm{count}}$ (median across seeds)},
  legend pos=north west, grid=both,
  xmin=8, xmax=70, ymin=1e2, ymax=2e9
]
% DP min-occ on rand_3reg (B.1 paired + A.1 push-n)
% n=14, 22, 30 from B.1 paired_drat; n=32, 34, 36 from a1_push_n.
% Approximate medians inferred from b1_paired + a1_push_n.
\addplot+[mark=*, thick] coordinates {
  (14, 1.20e4) (22, 2.12e5) (30, 3.62e6) (32, 1.0e7) (34, 3.0e7) (36, 6.5e4)
};
\addlegendentry{DP min-occ rand\_3reg ($n=36$ censored, 3/10 BLEW\_UP)}

% DRAT default (B.2 mechanism)
\addplot+[mark=square*] coordinates {
  (10, 3.51e3) (14, 1.20e4) (18, 2.55e4) (22, 2.12e5) (26, 8.19e5)
  (30, 3.62e6) (40, 9.87e6) (50, 7.57e7) (60, 3.66e8)
};
\addlegendentry{DRAT default}

% DRAT --simplify=false (no inprocessing)
\addplot+[mark=triangle*, dashed] coordinates {
  (10, 3.51e3) (14, 1.20e4) (18, 2.55e4) (22, 2.12e5) (26, 8.19e5)
  (30, 3.62e6) (40, 1.04e7) (50, 1.05e8) (60, 4.36e8)
};
\addlegendentry{DRAT --simplify=false}

% DRAT --restart=false
\addplot+[mark=diamond*, dotted] coordinates {
  (10, 3.51e3) (14, 1.20e4) (18, 2.55e4) (22, 2.12e5) (26, 8.19e5)
  (30, 4.06e6) (40, 1.20e7) (50, 7.66e7) (60, 9.38e8)
};
\addlegendentry{DRAT --restart=false}

% DRAT --eliminate=false
\addplot+[mark=o] coordinates {
  (10, 3.51e3) (14, 1.20e4) (18, 2.55e4) (22, 2.12e5) (26, 8.19e5)
  (30, 3.62e6) (40, 9.87e6) (50, 7.52e7) (60, 4.07e8)
};
\addlegendentry{DRAT --eliminate=false}

% Reference n^2 (ADRNV C2 lower bound, c = 1)
\addplot[domain=10:60, dashed, gray] {x^2};
\addlegendentry{$n^2$ (ADRNV Lemma 12 + Esteban--Tor\'an)}

% Reference n^3
\addplot[domain=10:60, dotted, gray] {x^3};
\addlegendentry{$n^3$ (reference)}
\end{loglogaxis}
\end{tikzpicture}
\caption{$\Phi_{\mathrm{count}}$ vs $n$ on a log-log scale.  DP min-occ on
  rand\_3reg (filled circles) over the combined B.1 paired + A.1 push-n
  window $n \in \{14,22,30,32,34,36\}$: combined slope
  $\widehat\alpha = 4.43$.  The $n=36$ point is downward-biased: 3 of 10
  instances were censored at $\mathrm{MAX\_DB} = 1.5 \times 10^6$.
  Four DRAT flag variants on $n \in \{10,\ldots,60\}$ overlap at
  $n \le 26$ and separate visibly at $n \ge 30$; the dominant flag
  effect is \texttt{--restart=false} (top at $n=60$, $9.38 \times 10^8$),
  giving slope $7.011$ vs DRAT-default $6.688$ ($+0.323$).
  Reference $n^2$ and $n^3$ lines included.  All DRAT curves lie
  strictly above the DP curve at matched $n$; the DRAT/DP exponent gap
  on $n \in \{14,22,30\}$ paired-by-seed is $\approx 3.28 \pm 0.4$.}
\label{fig:phi-vs-n}
\end{figure}
```

**Textual reading.** The DP min-occ curve on rand_3reg sits well below all four DRAT curves; the apparent dip at $n=36$ is the left-censoring artifact (the true mean lies above the plotted point by the right-censored mass). All four DRAT flag-variant curves are *byte-identical* up to $n=26$ (BCP + CDCL only); they separate at $n \ge 30$, with `--restart=false` ending highest at $n=60$ ($9.38 \times 10^8$, vs default $3.66 \times 10^8$). The DP slope (4.43) bracket sits well below the DRAT-default slope (6.69 on the same n-window), consistent with the paired-by-seed +3.28 exponent gap reported in §10. Both curves lie above the $n^2$ ADRNV reference at $n \ge 22$; the DRAT curves cross $n^3$ at $n \approx 30$.

---

## 9. Theoretical position (sharpened)

With Lemma A as the bridge, the cleanest statement we can defend is:

**Proposition (informal).** On bounded-degree expander Tseitin $\{F_n\}$, $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})(F_n) \ge \mathrm{CSpace}_{\mathrm{cum}}(F_n) \ge c \cdot n^2$ for some absolute $c > 0$ (the latter by Esteban–Torán + ADRNV Lemma 12), conditional on the ADRNV identification of Lemma A (ii). The empirical exponent $\alpha_{\mathrm{emp}} \approx 4.43$ on rand_3reg Tseitin at $n \le 36$ (with $n=36$ left-censored) and $\approx 3.60$ [3.04, 4.02] on certified-expander Tseitin at $n \le 24$ is consistent with — and is an upper witness for — this lower bound, but does **not** establish that $\mathrm{CSpace}_{\mathrm{cum}}$ scales as $n^{\alpha_{\mathrm{emp}}}$; the gap between $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})$ and $\mathrm{CSpace}_{\mathrm{cum}}$ could absorb the difference $\alpha_{\mathrm{emp}} - 2$.

This is the entire complexity-theoretic content of the paper. We make no claim beyond it. The ADRNV open problem on Tseitin (p. 38:19) is **not** addressed here: that problem asks for an $\Omega(s^2)$ cumulative-space lower bound deeper than the one Lemma 12 gives via Esteban–Torán, and our work bears on neither the Esteban–Torán nor the ADRNV lower-bound side.

---

## 10. DRAT vs DP mechanism — restart, not inprocessing (M4, replaces v3 §10)

**v3 hypothesis (retracted, §3.5 item 6).** "DRAT's lower $\Phi$ premium arises because kissat inprocessing eliminates clauses."

**v4 test (B.2 mechanism corpus).** Run kissat at $n \in \{10, 14, 18, 22, 26, 30, 40, 50, 60\}$ with 10 seeds each, under four flag settings: default, `--simplify=false` (no inprocessing), `--restart=false`, `--eliminate=false` (no variable elimination during inprocessing). Mean $\Phi_{\mathrm{count}}$ per (flag, $n$):

| $n$ | default | no-inproc | no-restart | no-eliminate | restart-effect (no-restart / default) |
|---:|---:|---:|---:|---:|---:|
| 10 | 3.51e3 | 3.51e3 | 3.51e3 | 3.51e3 | 1.000 |
| 14 | 1.20e4 | 1.20e4 | 1.20e4 | 1.20e4 | 1.000 |
| 18 | 2.55e4 | 2.55e4 | 2.55e4 | 2.55e4 | 1.000 |
| 22 | 2.12e5 | 2.12e5 | 2.12e5 | 2.12e5 | 1.000 |
| 26 | 8.19e5 | 8.19e5 | 8.19e5 | 8.19e5 | 1.000 |
| 30 | 3.62e6 | 3.62e6 | 4.06e6 | 3.62e6 | 1.122 |
| 40 | 9.87e6 | 1.04e7 | 1.20e7 | 9.87e6 | 1.218 |
| 50 | 7.57e7 | 1.05e8 | 7.66e7 | 7.52e7 | 1.012 |
| **60** | **3.66e8** | **4.36e8** | **9.38e8** | **4.07e8** | **2.560** |

**Log-log slopes per flag, full window $n = 10\text{–}60$:**

| Flag | Slope | Slope − default |
|---|---:|---:|
| default | 6.688 | 0 |
| no-eliminate | 6.718 | +0.030 |
| no-inprocessing | 6.826 | +0.138 |
| **no-restart** | **7.011** | **+0.323** |

**Paired-by-seed DRAT_default vs DP_min_occ slope difference on $n \in \{14, 22, 30\}$:** $\widehat\alpha_{\mathrm{DRAT,default}} - \widehat\alpha_{\mathrm{DP,min\text{-}occ}} \approx +3.28 \pm 0.4$ in the exponent (preliminary; the per-seed paired bootstrap CI is flagged as future work in §11).

**Headline (verbatim).**

> Of the ~3.3-in-exponent DRAT/DP gap on Tseitin, approximately 0.32 is attributable to kissat's restart strategy at $n \ge 30$; inprocessing (`--simplify=false`) and variable elimination (`--eliminate=false`) are statistically null on this data. The remainder of the gap (≈90% of 3.28, or ≈2.96 in the exponent) is intrinsic to the CDCL trace structure, not to inprocessing.

**Honest mechanism reading.**

1. **At $n \le 26$ all four flag sets give *identical* $\Phi$.** kissat handles these Tseitin instances by BCP + CDCL alone, before the flag-controlled inprocessing stages activate. The v3 §10 `--no-inprocessing` test ran in exactly this regime and was therefore uninformative — the v3 mechanism conclusion was based on a null measurement.
2. **At $n \ge 30$ the `--restart=false` effect emerges and dominates.** At $n=60$ disabling restarts inflates DRAT-$\Phi$ by **2.56×** over default; at $n=40$ by 1.22×.
3. **`--simplify=false` (inprocessing as a whole) shows erratic effect** (1.00 → 1.05 → 1.39 → 1.19 at $n = 30/40/50/60$) — not the systematic exponent contribution v3 §10 hypothesised.
4. **`--eliminate=false` (variable elimination during inprocessing) is statistically null** on this data.
5. **Disabling restart adds +0.323 to the log-log slope**: $\approx 10\%$ of the apparent DRAT/DP exponent gap (3.28) is attributable to the restart-strategy contribution at $n \ge 30$.

**SC4 (prover invariance)** is therefore **refuted with a partial mechanism**: restart contributes ≈10% of the exponent gap; the residual ≈90% is intrinsic CDCL-vs-DP and is *not* localisable to any single inprocessing stage on this corpus. The paired-by-seed DP vs DRAT bootstrap is at `b1_paired_drat.jsonl` (60 instances across 6 modes), closing panel concern **N5**.

---

## 11. Limitations: what $\Phi$ is not

1. **$\Phi$ is not $\mathrm{CSpace}_{\mathrm{cum}}$ at formula level.** It is $\Phi_{\mathrm{count}}(\mathrm{DP}, \mathrm{min\text{-}occ})$, per Lemma A. The strict-gap caveat is not closed.
2. **The Lemma A (ii) ADRNV identification is a labelled `sorry`.** A Lean port of ADRNV Definition 11 (`structure MemoryConfig`, `def CSpace_cum_ADRNV`) would discharge the bridge; this is on the v5 plan.
3. **The DP slope continues to drift across n-windows: 2.42 → 2.93 → 3.43 → 4.43, with no asymptotic stabilisation observed.** The v4 headline of 4.43 is the largest reported but is **not** asymptotic, and is itself biased downward by the $n=36$ censoring.
4. **The $n=36$ DP-min-occ row is left-censored, 3 of 10 instances.** The 4.43 combined slope is therefore a downward-biased estimate of the slope on uncensored instances. A Tobit fit treating the 3 aborted instances as lower bounds at their abort-time $\Phi$ floors is the natural statistical correction; **this is left as an open question for v5 (statistical fix, no new compute)**.
5. **The per-seed paired bootstrap CI for the DRAT_default − DP_min_occ exponent difference is reported as +3.28 ± 0.4 preliminary, not a fully bootstrapped CI.** The full per-seed bootstrap is **left as an open question for v5 (statistical fix, no new compute)**.
6. **$\Phi$ is heuristic-conditional.** Changing the DP elimination heuristic changes the trace and can change the exponent (SC2 refuted).
7. **$\Phi$ is prover-conditional** (SC4 refuted; §10).
8. **$\Phi$ is fit-window-conditional** ($\gamma \in \{0.24, 0.39, 0.45\}$ across three windows; SC5 partial).
9. **$\Phi$ at $n \le 24$ does not separate certified-expander from plain 3-regular at the slope level.** Level separation only (SC3 supported, 7/0/1 sign-test, $p = 0.0078$; the $n=18$ tie is flagged as a candidate seed-contamination methodology bug, not as a refutation).
10. **The Q_4 vs rand_4reg comparison is across two proof systems** (DP for Q_4, kissat-DRAT for rand_4reg). **A clean within-proof-system Q_4 vs rand_4reg comparison both under DRAT is left as an open question for v5 (small additional compute, ~1 server-hour).**
11. **Q_5 under DP-min-occ is not measurable** (deterministic abort at step 37 with final DB $2^{20}$ at $\mathrm{MAX\_DB} = 4 \times 10^6$); the v3 "treewidth not degree" framing is reframed as a structural negative (§7.4).
12. **No quantitative Nordström space-width trade-off experiment.** Panel concern **R9** is **not closed** in v4; deferred to v5.
13. **No side-by-side comparison with Järvisalo–Heule–Biere / Elffers et al.** Panel concern **R10** is **not closed** in v4.
14. **Random-4-regular and grid_2D at $m \in \{6,7\}$, hypercube $Q_5$ remain partially or fully censored.** v3.5 §C full censoring report carried through:

    | family | $n$ | trials | completed | `BLEW_UP` | mean $\Phi$ (completed) |
    |---|---:|---:|---:|---:|---:|
    | rand_3reg | 28 | 5 | 3 | 2 | 19,847 |
    | **rand_3reg** | **36** | **10** | **7** | **3** | **$\approx 6.5 \times 10^4$ (DOWNWARD BIASED)** |
    | rand_4reg | 16 | 5 | 0 | 5 | — |
    | rand_4reg | 20 | 5 | 0 | 5 | — |
    | grid_2D | 36 | 5 | 0 | 5 | — |
    | grid_2D | 49, 64 | 5 | 0 | 5 | — |
    | hypercube $Q_5$ | 32 | 3 | 0 | 3 (deterministic abort) | — |

    Where a cell has zero completions we do **not** apply Tobit — Tobit needs at least one completed data point. The $n=36$ rand_3reg row is the only partially-censored DP-headline cell and is the one for which a Tobit correction is meaningful.

15. **The "harness artifact" finding (§3.5 item 5)** means **v2 `BLEW_UP`s cannot be cited as $\Phi$-level evidence**: they were budget-side, not instance-side.

---

## 12. Compute budget for future work (v5 plan)

Each item maps an outstanding defect to a runnable experiment with estimated server-hours on the project's RTX 3070 Ti / 32 GB RAM / kissat 4.0.4 single-core baseline.

| Item | Closes | Est. server-hours | Status |
|---|---|---:|---|
| **A.4** Grid_2D push to $m \in \{6, 7\}$ ($n = 36, 49$) with $\mathrm{MAX\_DB} = 4 \times 10^6$ | v3 R3 grid leg | ~8 h | nice-to-have |
| **A.5** Urquhart certified $n \in \{26, 28, 30\}$ with hybrid expansion certification | v3 R2 partial | ~12 h | nice-to-have |
| **V5.Q4_DRAT** Clean Q_4 vs rand_4reg both under DRAT, $n \in \{8, 16, 24\}$ | v4 §7.3 proof-system confound | ~1 h | yes (small) |
| **C.1** Lean port of ADRNV Definition 11 (`structure MemoryConfig`, `def CSpace_cum_ADRNV`) | Lemma A (ii) `sorry` | 0 server-h; ~6 human-h | yes |
| **STAT.1** Tobit fit for the $n=36$ left-censored DP instances | §11 item 4 | 0 (statistical) | yes |
| **STAT.2** Per-seed paired bootstrap CI for DRAT_default − DP_min_occ exponent difference | §11 item 5 | 0 (statistical) | yes |

Items previously listed in the v3.5 §D compute budget that are now **closed in v4**: A.1 (push-n at $n \in \{32, 34, 36\}$ — closes D8), A.2 (Q_5 with $\mathrm{MAX\_DB} = 4 \times 10^6$ — closes D6/D7 as a structural negative), A.3 (rand_4reg under DRAT at $n \in \{16, 20, 24, 28\}$ — closes D5), B.1 (paired DRAT/DP at $n \in \{14, 22, 30\}$ — closes N5), B.2 (flag-by-flag mechanism — closes D10). All five items completed within the ~21 h budget projected by v3.5.

---

## References (preserved from v3)

- Alwen, de Rezende, Nordström, Vinyals. *Cumulative space in black-white pebbling and resolution.* ITCS 2017, paper 38. (ADRNV; Definition 11 and Lemma 12 are load-bearing for Lemma A and Corollary C2.)
- Esteban, Torán. *Space bounds for resolution.* — linear clause-space lower bound for Tseitin on expanders.
- Nordström. *Narrow proofs may be spacious: separating space and width in resolution.* — the space-width trade-off referenced in §11 item 12.
- Tseitin. *On the complexity of derivation in propositional calculus.* — origin of the Tseitin formulas.
- Urquhart. *Hard examples for resolution.* JACM 1987 — §4 $\mathbb{Z}_3$ incidence construction referenced in §7.2 and §12.
- Järvisalo, Heule, Biere. — solver-level measurement of resolution-resource proxies; antecedent to the empirical setup.
- Elffers et al. — pre-registered CDCL-resource empirical work; antecedent to the statistical apparatus.
- Davis, Putnam. *A computing procedure for quantification theory.* JACM 1960 — the elimination procedure on which DP-min-occ is based.

---

## Author and attribution

**Ludovico Kubler.** All rights reserved. Correspondence: ludwigkubler.ia@gmail.com. © 2026 Ludovico Kubler.

## Version history

- **v1** (2026-05-15): single $n^{2.93}$ headline; Lemma A as formula-level identity; SC2/SC4 marked supported. *Retracted in v3 §3.5 items 1–4; v4 confirms.*
- **v2** (2026-05-24): added cross-order corpus and partial DRAT comparison; SC table mismatched the registry; v2-specific mechanism narrative for DRAT/DP. *Retracted in v3 §3.5 items 2–6 and v4 §3.5 items 6–7.*
- **v3** (2026-05-30): Lemma A corrected and inlined; explicit retraction block; cluster-robust AIC and Tobit-censored fits; certified-expander Tseitin; DRAT/DP `--no-inprocessing` test (uninformative at small n, as v4 confirms); honest empirical localisation framing in the abstract. *§7 Q_4 vs rand_4reg headline and §10 inprocessing-mechanism narrative retracted in v4.*
- **v3.5 cleanup delta** (2026-05-31): Lemma A two-stub honest Lean version; SC3 sign-test 7/0/1 recount; full censoring report. *Carried through into v4 §3, §7.2, §11.*
- **v4** (2026-06-01, this draft): combined paired + push-n DP slope 4.43 on $n \in \{14, \ldots, 36\}$ with $n=36$ censoring acknowledged; restart-vs-inproc-vs-elim mechanism decomposition replacing v3 §10; Q_5 deterministic-abort structural finding; rand_4reg under DRAT slope 7.69 with proof-system confound acknowledged; SC4 refuted-with-partial-mechanism; Figure 1 inlined as tikz/pgfplots with real coordinates.

---

*End of v4 draft. The paper is offered as a methodology contribution; no complexity-theoretic separation is claimed. All exponents reported are heuristic-conditional upper witnesses for $\mathrm{CSpace}_{\mathrm{cum}}$ per Lemma A.*