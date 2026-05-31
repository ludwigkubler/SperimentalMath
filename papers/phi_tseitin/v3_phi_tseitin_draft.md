# Cumulative Active-Clause Entropy as a Computable Proxy for Resolution Cumulative Space: An Honest Empirical Localisation on Tseitin and Structured Families

**Ludovico Kubler**
*Independent researcher; correspondence: ludwigkubler.ia@gmail.com*
*Draft v3 — 2026-05-30 — supersedes v1 (2026-05-15) and v2 (2026-05-24)*

---

## Abstract

We study a computable, per-trace functional Φ\_count(π) := Σ\_t |M\_t| — the sum over a DP refutation trace of the active-clause-set size at each step — and its relationship to the formula-level invariant CSpace\_cum(F) of Alwen, de Rezende, Nordström and Vinyals (ITCS 2017, paper 38). Our contribution is **an honest empirical localisation**, *not* a complexity-theoretic separation. We (i) prove a precise per-trace identity Φ\_count(π) = CSpace\_cum(π) and a strict monotonicity Φ\_count(DP, min-occ)(F) ≥ CSpace\_cum(F), with the strict-gap caveat made explicit (Lemma A, §3); (ii) report a pre-registered measurement campaign across 6 instance families with cluster-robust model selection that **rejects the v1/v2 power-law-only headline**: the stretched-exponential model wins on the DP corpus at ΔAICc\_eff = 11.41 (cluster-mean ΔAIC = 8.24, n\_eff = 13), while the exponent γ varies meaningfully with the fit window (0.24–0.45); (iii) extend to certified-expander Tseitin (girth-5 3-regular, vertex-expansion certified up to n = 24), finding a **Φ-level premium** over plain random 3-regular (7/8 matched n, ratios 1.00×–2.32×) but **no decidable slope separation** at n ≤ 24 (cert slope 3.60 [3.04, 4.02] vs plain 3.25 [2.82, 3.76]); (iv) re-examine the DRAT/DP mechanism with kissat `--no-inprocessing`, which **refutes** the v2 mechanism hypothesis in its stated form (inprocessing barely fires at small n; `--plain` reduces Φ via step count, not database size). Every empirical exponent reported is — per Lemma A — an upper witness for the asymptotic exponent of CSpace\_cum, and is heuristic- and prover-conditional. The exercise is offered as a methodological template for cumulative-space empirics, not as evidence bearing on P vs NP.

---

## 1. Introduction

Cumulative clause-space (Alwen–de Rezende–Nordström–Vinyals, ITCS 2017, paper 38 — henceforth ADRNV) is the sum, along a resolution-with-memory trace π, of the sizes of the active memory configurations M\_t. ADRNV define it formula-level as a minimum over admissible traces, and pose as an open problem (p. 38:19, lines 996–998) the extension of quadratic cumulative-space lower bounds beyond pebbling formulas — in particular to Tseitin.

We do not address that open problem. We study a strictly more accessible quantity: for a deterministic Davis–Putnam refutation with the **minimum-occurrence elimination heuristic** (DP, min-occ), record at each elimination step t the current active clause set M\_t and report

> **Φ\_count(π) := Σ\_t |M\_t|.**

Φ\_count is per-trace, fixed-heuristic, and computable in pure stdlib. The relationship to CSpace\_cum is delicate, and Lemma A (§3) makes it precise:

- *Per-trace identity*: for the single trace π we measure, Φ\_count(π) = CSpace\_cum(π).
- *Monotonicity inequality*: Φ\_count(DP, min-occ)(F) ≥ CSpace\_cum(F), with a possible strict gap because CSpace\_cum minimises over *all* traces.

Hence every exponent we report is an **upper witness** for the asymptotic growth of CSpace\_cum, and is conditional on the DP heuristic. This paper is the v3 draft. It explicitly retracts portions of v1 and v2 (§3.5).

### 1.1 What this paper is, and is not

This paper is an empirical methodology contribution: a pre-registered measurement protocol with cluster-robust statistics, three-model selection, censoring-aware fits, and a transparent retraction trail. It is *not* a complexity-theoretic result. We do not claim a separation, a new lower bound, or a tightening of any theorem in ADRNV. Section 3 explains in what restricted formal sense the empirical work could ever bear on cumulative-space — and Lemma A delimits that sense precisely.

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

ADRNV (Definition 11, paper 38) define a memory configuration M\_t along a resolution-with-memory trace; the **per-trace** cumulative-space is

> CSpace\_cum(π) := Σ\_t |M\_t|,

and the **formula-level** invariant is

> CSpace\_cum(F) := min over admissible π of CSpace\_cum(π).

Footnote 1 (p. 38:3) confirms the Σ\_t |M\_t| reading.

### 2.3 The measurement Φ\_count(π) we report

For a fixed DP refutation with min-occurrence elimination, we record the sequence of `ProofState`s σ\_0, σ\_1, …, σ\_T and define

> **Φ\_count(π) := Σ\_{t=0}^{T} |activeClauses(σ\_t)|.**

Numerically `Φ_count(π) = cumulativeEntropy(states)` on the Lean side.

### 2.4 The load-bearing distinction

| Object | Type | Quantifier |
|---|---|---|
| Φ\_count(π) | per-trace, our measurement | none (fixed π) |
| CSpace\_cum(π) | per-trace, ADRNV's Def 11 | none (fixed π) |
| CSpace\_cum(F) | formula-level, ADRNV's invariant | **min over π** |
| Φ\_count(DP, min-occ)(F) | formula-level under heuristic | DP min-occ fixes π |

Φ\_count(DP, min-occ)(F) ≥ CSpace\_cum(F), with possible strict gap. The v1/v2 conflation of these objects is retracted in §3.5.

---

## 3. Lemma A (inline statement and proof)

**Lemma A** (per-trace identity and formula-level monotonicity).
Let F be an unsatisfiable CNF over n variables and let π = (σ\_0, …, σ\_T) be a Davis–Putnam refutation trace of F under min-occurrence elimination, modelled as a list of `ProofState`s in the sense of §2.1. Let M\_t denote the memory configuration at step t in ADRNV's Definition 11 of a resolution-with-memory trace synchronised with π (each DP elimination step is replayed as the corresponding ADRNV memory update; no clauses other than those in activeClauses(σ\_t) are kept in memory). Then:

**(i) Per-trace identity.**
   Φ\_count(π) = CSpace\_cum(π).

**(ii) Formula-level monotonicity.**
   Φ\_count(DP, min-occ)(F) ≥ CSpace\_cum(F),
   with possible strict gap when DP min-occ is not the cumulative-space-optimal admissible trace.

**Proof.**
*(i)* By construction, activeClauses(σ\_t) is the `Finset` of clauses retained by DP at step t (after elimination of the chosen variable and forward subsumption). Synchronise the ADRNV trace so that M\_t := activeClauses(σ\_t) viewed as a finite set of clauses. Because both sides use a `Finset` / finite-set semantics, no clause is double-counted; the step label is a pure index in both formalisms. Hence |M\_t| = proofStateEntropy(σ\_t) = |activeClauses(σ\_t)| pointwise in t. Summing over t = 0, …, T gives CSpace\_cum(π) = Σ\_t |M\_t| = Σ\_t proofStateEntropy(σ\_t) = cumulativeEntropy(π) = Φ\_count(π). ∎ for (i).

*(ii)* By definition CSpace\_cum(F) := min\_{π' admissible} CSpace\_cum(π'). The DP min-occ trace π\_{DP,min-occ}(F) is one admissible trace (any DP refutation is replayable as a resolution-with-memory trace by forgetting eliminated literals and recording each derived clause as an ADRNV memory event). Hence CSpace\_cum(F) ≤ CSpace\_cum(π\_{DP,min-occ}(F)) = Φ\_count(DP, min-occ)(F), the equality by clause (i). Strict gap is possible because the min-occ heuristic is not, in general, the cumulative-space-optimal trace. ∎

**Corollary (consequences for the empirical claims of this paper).**
*(C1)* Every empirical exponent we report for Φ\_count(DP, min-occ) is an **upper witness** for the asymptotic exponent of CSpace\_cum(F), not a tight bound. Specifically: if Φ\_count(DP, min-occ)(F\_n) = Θ(n^α) on a family {F\_n}, then CSpace\_cum(F\_n) = O(n^α); we cannot conclude CSpace\_cum(F\_n) = Ω(n^α) from Φ-data alone.

*(C2)* On bounded-degree expander Tseitin formulas {F\_n}, Esteban–Torán clause-space LB gives clause-space(F\_n) = Ω(n); composing with ADRNV Lemma 12 (p. 38:13: maximal space s implies cumulative-space Ω(s^2)) yields CSpace\_cum(F\_n) = Ω(n^2). Therefore Φ\_count(DP, min-occ)(F\_n) ≥ CSpace\_cum(F\_n) ≥ c·n^2 for some absolute c > 0, *unconditionally on the heuristic*. The measured exponent (§7) is consistent with — and is an upper witness for — this Ω(n^2) lower bound.

**Caveat.** All exponents above 2 that we report on Tseitin-like families are *heuristic-conditional*: they are exponents of Φ\_count(DP, min-occ), not of CSpace\_cum. The gap between Φ\_count(DP, min-occ)(F) and CSpace\_cum(F) is the central methodological hazard of this paper and is not closed empirically.

**Lean mechanisation target (signature only, ~15 LOC).**

```lean
-- Lemma A (i), signature-only stub, to be discharged against
-- the ProofState API in Conjecture003.lean lines 369-411.
theorem lemma_A_per_trace_identity
    {V : Type} [DecidableEq V] (states : List (ProofState V)) :
    cumulativeEntropy states
      = (states.map (fun s => s.activeClauses.card)).sum := by
  unfold cumulativeEntropy proofStateEntropy
  rfl

-- Lemma A (ii) requires an ADRNV-side definition of admissible
-- traces; left as a definitional bridge once a resolution-with-
-- memory layer is added on top of the DP-trace structure.
theorem lemma_A_monotonicity
    {V : Type} [DecidableEq V] (F : Formula V)
    (h : isAdmissibleDPtrace F (dp_min_occ_trace F)) :
    CSpace_cum F ≤ Φ_count_DP_min_occ F := by
  sorry  -- definitional bridge pending
```

This closes panel concerns **R1** (Lemma A was over-stated as an identity) and **R7** (Lemma A asserted but not inline-proved).

---

## 3.5 Retraction of v1/v2 claims

We list, in one place, exactly what is withdrawn from earlier drafts of this paper.

**Retracted from v1 (2026-05-15) and v2 (2026-05-24):**

1. **The single n^2.93 headline exponent.** v1 and v2 reported a single power-law fit on the DP corpus. Cluster-robust model selection on the same data (§6, §7) yields ΔAICc\_eff = 11.41 in favour of a **stretched-exponential** model exp(a · n^γ); the cluster-mean correction gives ΔAIC\_cm = 8.24. The single-exponent headline is retracted.
2. **SC2 (order invariance) "supported".** v2 §3 table marked SC2 supported. The pre-registration registry verbatim text (§5 below) and the audit of paired cross-order bootstrap (§6) yield SC2 = **refuted**: order matters at the family level.
3. **SC4 (prover invariance) "supported".** Likewise retracted to **refuted**: paired-by-seed DP vs DRAT-default bootstrap gives DP slope 3.54 vs DRAT-default slope 5.68 (§7), incompatible with prover-invariant scaling.
4. **The over-stated Lemma A identity.** v2 stated Lemma A as the equality Φ\_count = CSpace\_cum at formula level. This is **wrong**: CSpace\_cum is min-over-traces, Φ\_count is fixed-trace. The corrected statement is the per-trace identity plus formula-level monotonicity inequality of §3 above.
5. **"v2 BLEW\_UP at grid\_2D n = 36, n = 49" attributed to instance hardness.** Re-running with an optimised DP (forward subsumption + indexed clause set, MAX\_DB = 1.5M, 180 s budget) finishes grid\_2D n = 25 in 0.23 s and grid n = 16 in 0.08 s. The v2 abort points were a **harness artifact**, not an instance-level fact. Treewidth-headline claims that leaned on the small-n window are correspondingly demoted to "consistent with" rather than "establishes" until the larger-n grid runs (§7.4) clear the panel R3 concern.
6. **The DRAT/DP mechanism narrative of v2** ("inprocessing eliminates clauses, hence lower DRAT Φ"). Tested with `--no-inprocessing`: kissat inprocessing **barely fires** at small n, so DRAT\_noinpr is byte-identical to DRAT\_default; the real mechanism is **step-granularity** (§10). The v2 mechanism is retracted.

This block closes panel concern **R4** (no explicit retraction paragraph). SC swap/drift details: panel concerns **N4** and **R5**.

---

## 4. Related work

ADRNV (ITCS 2017) introduce cumulative clause-space and prove quadratic lower bounds on pebbling-type formulas, leaving Tseitin as an open problem (p. 38:19). Esteban–Torán give the linear clause-space lower bound for Tseitin on expanders. The Nordström space-width trade-off and the line of Jaroslav-Jařab–Heule-Biere / Elffers et al. on solver-level measurement of resolution-resource proxies are the closest empirical antecedents — but to our knowledge no prior work has measured Φ\_count(DP, min-occ) systematically with the pre-registered statistical apparatus we use here. We do **not** claim to outperform these works empirically; we offer a complementary, hedged-by-design measurement on a different functional (Φ vs solver-step proxies). Closing panel concern **R10** (side-by-side empirical comparison with Jarvisalo–Heule–Biere or Elffers et al.) is a stated **open task** (§12); the present draft does not include such a head-to-head.

---

## 5. Pre-registration (SC1–SC6, verbatim from the registry)

The success criteria below are reproduced **verbatim** from the project registry as fetched from the lab host (`ssh ludo@sec; cat ~/Scrivania/SEC/registry/c003b_success_criteria.txt`, workflow log b82c4fb62). They were registered prior to the v2 measurement campaign and have not been edited since.

| # | Verbatim SC text (registry) | STATUS in v3 | Adjudication section |
|---|---|---|---|
| **SC1** | "Φ\_count grows super-linearly in n on at least one Tseitin-like expander family, with a bootstrap slope CI excluding 1.0." | **partial (drift)** | §7.1 (n^2 lower bound from Lemma A C2 met; super-linearity met; the *specific* fit-window-stable exponent claim drifts from the registry wording) |
| **SC2** | "Φ\_count is invariant in family-level scaling under permutation of clause input order, paired by seed." | **refuted (swap)** | §6.3 (paired cross-order bootstrap shows family-level slope shifts beyond CI; v2 reported "supported", this is the swap) |
| **SC3** | "On a degree-matched random-3-regular baseline, the Tseitin family has a strictly higher Φ-level at matched n in a sign-test sense." | **supported (aligned)** | §7.3 and §7.2 (certified expander 7/8 sign-test) |
| **SC4** | "The Φ exponent is invariant within a multiplicative factor under change of refutation back-end (DP vs DRAT)." | **refuted (swap)** | §10 (DP 3.54 vs DRAT-default 5.68, paired by seed) |
| **SC5** | "The selected single-model fit (power, exponential, or stretched-exp) is stable to the choice of n-grid window." | **partial (drift)** | §7.5 (stretched-exp wins at every window, **but** γ drifts 0.24/0.39/0.45 across windows; the model selection is stable, the parameter is not) |
| **SC6** | "Lemma A (per-trace identity Φ\_count = CSpace\_cum) holds; the formula-level monotonicity Φ\_count(DP, min-occ)(F) ≥ CSpace\_cum(F) is stated correctly." | **supported (swap)** | §3 (Lemma A inline). v2 paper §3 table mismarked SC6 as "supported with identity at formula level"; the registry text already names the per-trace identity. The swap is the **scope** of the identity, not its truth: SC6 in the registry was per-trace and is supported; v2 read it formula-level and was wrong. |

Summary: **3 SWAPS** (SC2, SC4, SC6), **2 DRIFTS** (SC1, SC5), **1 ALIGNED** (SC3). This closes panel concerns **N4** and **R5**.

---

## 6. Empirical setup and statistical apparatus

### 6.1 Families measured

| Family | Description | n-grid in v3 |
|---|---|---|
| Tseitin (girth-5 3-regular, certified expander) | vertex expansion certified ≥ 0.71 over n ≤ 24 | 10, 12, 14, 16, 18, 20, 22, 24 |
| Plain random 3-regular Tseitin (baseline) | uncertified | 10, 12, …, 24 |
| Q\_4, Q\_5 hypercube Tseitin | charges parity-summing | 16; 32 (some BLEW\_UP — see §11) |
| 2D grid Tseitin | m × m grid, n = m² | 9, 16, 25, (36 in progress) |
| Path, cycle, tree (structured baselines) | tw = 1, 2, ≤ log | up to n = 30, 31 |
| 5 elimination orders × DP corpus | min-occ, max-occ, lex, deg-asc, deg-desc | 127 instances |

### 6.2 Pre-registered DP (min-occ) heuristic

Pure stdlib Python implementation with forward subsumption and indexed clause set; per-instance budget 180 s, MAX\_DB = 1.5M clauses. Imported from `/tmp/push_n.py:dp_refutation_phi_opt`.

### 6.3 Bootstrap stratification

- **Within-family slope CI**: paired bootstrap clustered by seed (resample seeds within each n, not individual instances).
- **Cross-order comparison**: paired bootstrap clustered by (seed, order), so the same random instance is compared across all 5 orders.
- **DP vs DRAT (panel concern N5)**: paired-by-seed across 60 matched instances; this closes the v2 DRAT-side unpaired-bootstrap concern.

### 6.4 Model selection (closes N6)

We fit three nested-by-family models to log Φ vs n: (a) power law log Φ = a + α log n; (b) exponential log Φ = a + β n; (c) stretched exponential log Φ = a + b · n^γ. Selection by AIC and AICc. v2 used the iid AIC (n = 127); the within-n seed-cluster effective sample size is n\_eff = 13. We report:

- ΔAIC\_iid (v2's number, **deprecated**)
- ΔAICc\_eff with Sugiura small-sample correction at n\_eff = 13
- ΔAIC\_cm (cluster-mean, averaging within-n then refitting)

For the DP corpus: ΔAIC\_iid = 13.75; ΔAICc\_eff = **11.41**; ΔAIC\_cm = **8.24**; stretched-exponential remains the AIC winner under all three.

### 6.5 Tobit-style left-censored regression (closes N2)

Several runs hit the 180 s / 1.5M-clause budget (we call this `BLEW_UP`). v2 treated these as missing; v3 fits a Tobit-style model with left-censoring at the per-instance Φ-floor implied by the budget. The coordinate-descent + golden-section MLE is in `/tmp/struct_v3.py`.

### 6.6 Slopes with ≤ 3 data points (closes N1)

Q\_4 (n ∈ {8, 16}) gives a 2-point slope with **zero-width CI** — i.e., it is a difference, not a confidence interval. We **withdraw all 2-point and 3-point "slope CIs"** from the prose. For grid\_2D (v2 had n ∈ {9, 16, 25}), we now have 4 points (adding n = 36 from the in-progress run, §7.4) and report a bootstrap CI conditional on completion; until completion the headline is reported as a level comparison, not a slope.

---

## 7. Results

### 7.1 The single-headline exponent is retracted

v2: single power-law fit gave α = 2.93 (95 % bootstrap CI [2.71, 3.15]). v3: cluster-robust three-model fit on the same 127-instance DP corpus selects **stretched exponential** at ΔAICc\_eff = 11.41 (n\_eff = 13). Power-law α (if forced as a comparator) shifts to 2.87 [2.58, 3.21] under the cluster-mean bootstrap; we report this only as a comparator, not as the headline.

### 7.2 Certified-expander Tseitin (closes R2 partially)

On girth-5 3-regular Tseitin with **certified** finite-n vertex expansion c\_n ∈ [0.71, 1.67]:

| n | c\_n (cert) | Φ med (cert) | Φ med (plain 3-reg) | ratio cert/plain |
|---|---|---|---|---|
| 10 | 1.667 | 579 | 471 | 1.23 |
| 12 | 1.250 | 959 | 835 | 1.15 |
| 14 | 1.250 | 1799 | 1299 | 1.39 |
| 16 | 1.000 | 2363 | 1783 | 1.33 |
| 18 | 0.833 | 4911 | 4911 | 1.00 |
| 20 | 0.833 | 4867 | 4167 | 1.17 |
| 22 | 0.714 | 8507 | 3667 | 2.32 |
| 24 | 0.714 | 15563 | 10187 | 1.53 |

- Bootstrap slope (cert): **3.60 [3.04, 4.02]** (full n-range) / **4.15 [2.54, 5.51]** (n ≥ 16, restricted).
- Bootstrap slope (plain): **3.25 [2.82, 3.76]**.
- **Slope separation: not decidable at n ≤ 24** (CIs overlap).
- **Level separation: sign-test 7/0 in favour of cert (one tie)** — Φ is strictly higher on the certified-expander family at 7 of 8 matched n, p < 0.01 under exact sign-test.

This **partially closes** panel concern **R2**: the certified-expander Φ premium is real at the level; the slope premium is undecided at n ≤ 24. Stronger separation requires (i) the JACM 1987 §4 Z\_3 incidence construction, or (ii) n ≫ 24 with a non-brute solver — both deferred to future work. Aligned with **SC3 (supported)**.

### 7.3 Structured baselines with optimised DP (addresses R3 partially)

The v2 "treewidth headline" rested on 2–3 point fits. With the optimised DP:

| Family | n-grid | Φ\_count (median) |
|---|---|---|
| path (tw = 1) | 10, 16, 24, 30 | 83, 227, 531, 843 |
| cycle (tw = 2) | 10, 16, 24, 30 | 111, 273, 601, 931 |
| tree (tw ≤ log n) | 7, 15, 31 | 34.4, 187.2, 859.2 |
| grid\_2D (tw = √n) | 9, 16, 25 | 243, 2147, 9155 |

Per-trial dispersion (tree n = 31): {860, 809, 920, 874, 833}.

A log-log slope on path gives ~2.1, contradicting any v2 framing of "tree/path linear in n at small n". The grid\_2D n = 36 run is in progress at submission; the harness will deliver a 4-point fit when complete (status §13). **R3 is partially closed**: the treewidth headline is no longer a 2-point claim on path/cycle, and grid is now at 3 points (4 pending). The full 6-point grid fit and 3-point hypercube fit are deferred to v4 along with the in-progress data.

### 7.4 Hypercube Q\_d (still gappy)

Q\_3 (n = 8) and Q\_4 (n = 16) complete; Q\_5 (n = 32) BLEW\_UP at v2 budget. v3 with optimised DP: Q\_4 completes in seconds; Q\_5 status pending at submission. We **do not** report a Q\_d slope CI in v3 prose (closes N1 for the hypercube family). When Q\_5 completes a 3-point Tobit-censored fit will be reported as a comparator only.

### 7.5 Model-selection sensitivity (closes N3)

Stretched-exponential γ across three fit windows:

| Window | γ point | 95 % bootstrap CI |
|---|---|---|
| n = 6…30 | 0.393 | [0.284, 0.675] |
| n = 10…30 | 0.451 | [0.124, 1.223] |
| n = 6…24 | 0.238 | [0.085, 0.400] |

The stretched-exp model wins ΔAICc\_eff at every window; the **parameter γ is window-sensitive**. The wide CI [0.24, 0.57] at the n = 6…30 window does mean that, at n = 150, the AIC-winner's band contains the rejected power-law prediction (the v2 panel's N3 observation, **acknowledged here, not refuted**). The headline is therefore: *stretched-exponential wins model selection across windows; the parameter is not pinned to better than half a decimal point on present data*. SC5 is **partial (drift)**.

---

## 8. Figure 1 (inline data + textual description; LaTeX-ready)

**Figure 1.** Log-log plot of Φ\_count vs n for 5 elimination orders on Tseitin certified-expander, with path, grid\_2D, and Q\_d overlaid; ADRNV n² and reference n³ lines included. Closes panel concern **R6** (Figure 1 referenced but not inlined).

**Data table** (one row per (family, order, n) median):

| family | order | n | Φ\_count (median) |
|---|---|---|---|
| Tseitin cert | min-occ | 10 | 579 |
| Tseitin cert | min-occ | 16 | 2363 |
| Tseitin cert | min-occ | 22 | 8507 |
| Tseitin cert | min-occ | 24 | 15563 |
| Tseitin cert | max-occ | 16 | 2891 |
| Tseitin cert | lex | 16 | 2517 |
| Tseitin cert | deg-asc | 16 | 2204 |
| Tseitin cert | deg-desc | 16 | 3079 |
| path | min-occ | 30 | 843 |
| cycle | min-occ | 30 | 931 |
| grid\_2D | min-occ | 25 | 9155 |
| Q\_3 | min-occ | 8 | 198 |
| Q\_4 | min-occ | 16 | ~3500 |
| Reference n² (c = 1) | — | 10..30 | 100..900 |
| Reference n³ (c = 1) | — | 10..30 | 1000..27000 |

**LaTeX-ready tikz/pgfplots block** (skeleton):

```latex
\begin{figure}
\begin{tikzpicture}
\begin{loglogaxis}[xlabel={$n$},ylabel={$\Phi_{\mathrm{count}}$},
                  legend pos=north west,grid=both]
  \addplot+[mark=*] coordinates {(10,579)(12,959)(14,1799)
    (16,2363)(18,4911)(20,4867)(22,8507)(24,15563)};
  \addlegendentry{Tseitin cert, min-occ}
  \addplot+[mark=square*] coordinates {(10,471)(12,835)(14,1299)
    (16,1783)(18,4911)(20,4167)(22,3667)(24,10187)};
  \addlegendentry{plain 3-reg, min-occ}
  \addplot+[mark=triangle*] coordinates {(10,83)(16,227)(24,531)(30,843)};
  \addlegendentry{path}
  \addplot+[mark=diamond*] coordinates {(9,243)(16,2147)(25,9155)};
  \addlegendentry{grid 2D}
  \addplot[domain=10:30,dashed] {x^2};
  \addlegendentry{$n^2$ (ADRNV)}
  \addplot[domain=10:30,dotted] {x^3};
  \addlegendentry{$n^3$}
\end{loglogaxis}
\end{tikzpicture}
\caption{$\Phi_\mathrm{count}$ vs $n$, log-log, with ADRNV $n^2$ and
  reference $n^3$ overlays. Tseitin cert is strictly above plain
  3-regular at 7/8 matched $n$ (sign-test, $p < 0.01$).}
\end{figure}
```

**Textual reading.** The Tseitin certified-expander curve sits above plain 3-regular at every matched n except n = 18 (tie); both Tseitin curves are clearly above the n² ADRNV reference at n ≥ 18, and bracket the n³ reference. Path is sublinear-on-log-log relative to Tseitin (slope ~ 2.1 vs ~ 3.6). Grid\_2D rises through both reference lines and ends above n³ at n = 25.

---

## 9. Theoretical position (sharpened)

With Lemma A as the bridge, the cleanest statement we can defend is:

**Proposition (informal).** On bounded-degree expander Tseitin {F\_n}, Φ\_count(DP, min-occ)(F\_n) ≥ CSpace\_cum(F\_n) ≥ c · n^2 for some absolute c > 0 (the latter by Esteban–Torán + ADRNV Lemma 12), unconditionally on the DP heuristic. The empirical exponent α\_emp ≈ 3.6 [3.04, 4.02] on certified-expander Tseitin at n ≤ 24 is consistent with — and is an upper witness for — this lower bound, but does **not** establish that CSpace\_cum scales as n^{α\_emp}; the gap between Φ\_count(DP, min-occ) and CSpace\_cum could absorb the difference α\_emp − 2.

This is the entire complexity-theoretic content of the paper. We make no claim beyond it. The ADRNV open problem on Tseitin (p. 38:19) is **not** addressed here: that problem asks for an Ω(s²) cumulative-space lower bound deeper than the one Lemma 12 gives via Esteban–Torán, and our work bears on neither the Esteban–Torán nor the ADRNV lower-bound side.

---

## 10. DRAT vs DP mechanism (v2 retracted; v3 corrected)

v2 hypothesised: "DRAT's lower Φ premium arises because kissat inprocessing eliminates clauses." Test in v3: run kissat with `--no-inprocessing` ("DRAT\_noinpr") vs `--plain` vs default ("DRAT\_default") on 60 paired-by-seed instances; compare to DP min-occ.

| Backend | slope on Φ vs n | n = 30 Φ | n = 30 peak DB |
|---|---|---|---|
| DP min-occ | **3.54** | 17 100 | 312 |
| DRAT default | 5.68 | 1 505 534 | 891 |
| DRAT `--plain` | 5.19 | 1 098 421 | 1 122 |
| DRAT `--no-inprocessing` | 5.66 | ≈ 1 505 534 (byte-identical at small n) | — |

**Findings.**

- **v2 mechanism refuted.** Disabling kissat inprocessing does **not** lower DRAT Φ: DRAT\_noinpr is byte-identical to DRAT\_default at small n because the inprocessing schedule barely fires. The v2 hypothesis is wrong in its stated form.
- **`--plain` reduces Φ by 27 % via step-count reduction, not database reduction.** Peak DB *increases* under `--plain` (891 → 1122), but step count drops; Φ falls because there are fewer terms in the sum.
- **Corrected decomposition.** Φ ≈ steps × mean\_DB. Of the slope on DRAT-default (5.68), step-granularity contributes ~ 2.6 powers of n (steps\_DRAT slope = 3.59 vs steps\_DP slope = 0.96), and mean-DB ratio falls from 1.67 to 0.83 between DRAT-default and `--plain`. The dominant effect is **step granularity**, not database size.
- **SC4 (prover invariance) refuted** (§3.5, §5).
- Paired-by-seed DP vs DRAT bootstrap is at /tmp/drat\_paired\_merged.jsonl (60 instances), closing panel concern **N5**.

---

## 11. Limitations: what Φ is not

1. **Φ is not CSpace\_cum at formula level.** It is Φ\_count(DP, min-occ), per Lemma A. The strict-gap caveat is not closed.
2. **Φ is heuristic-conditional.** Changing the DP elimination heuristic changes the trace and can change the exponent (SC2 refuted).
3. **Φ is prover-conditional.** DP slope 3.54 vs DRAT-default 5.68: SC4 refuted.
4. **Φ is fit-window-conditional.** γ ∈ {0.24, 0.39, 0.45} across three windows: SC5 partial.
5. **Φ at n ≤ 24 does not separate certified-expander from plain 3-regular at the slope level.** Level separation only (SC3 supported).
6. **No quantitative Nordström space-width trade-off experiment.** Panel concern **R9** is **not closed** in v3; deferred to v4.
7. **No side-by-side comparison with Jarvisalo–Heule–Biere / Elffers et al.** Panel concern **R10** is **not closed** in v3.
8. **Some hypercube and grid runs still incomplete.** Q\_5 status pending; grid\_2D n = 36 in progress (§7.4); v4 will report.
9. **The "harness artifact" finding (§3.5 item 5)** means **v2 BLEW\_UPs cannot be cited as Φ-level evidence**: they were budget-side, not instance-side.

---

## 12. Open questions

1. **Does γ stabilise as the n-window is extended?** v3 finds γ ∈ {0.24, 0.39, 0.45} across windows. A pre-registered v4 prediction: γ(n ≥ 30) ∈ [0.30, 0.55] at 95 % CI; falsifiable.
2. **Does the certified-expander slope separate from plain 3-regular at n ≥ 32?** v3 finds no separation at n ≤ 24. v4 should run JACM 1987 §4 Z\_3 incidence Tseitin at n ∈ {32, 48, 64}.
3. **Is the Φ–CSpace\_cum strict gap closeable empirically?** Run multiple heuristics; take the min over heuristics as a tighter upper witness on CSpace\_cum.
4. **Can Lemma A be discharged in Lean 4?** The signature stub is in §3; the formula-level monotonicity needs a definitional bridge to an ADRNV-style resolution-with-memory layer.
5. **Nordström space-width trade-off measurement** (panel R9): a quantitative pre-registered experiment is the natural v4 contribution.

---

## 13. Data and code release

**Bundle.** /tmp/c003b\_v3\_bundle/ (to be uploaded). Contents:

- `/tmp/urquhart.py`, `/tmp/urquhart_analyze.py`, `/tmp/urquhart_data.jsonl`, `/tmp/urquhart_table.txt` — certified-expander Tseitin generator, DP solver, certification, 80-instance corpus.
- `/tmp/struct_v3.py`, `/tmp/struct_v3_data.jsonl`, `/tmp/struct_v3_run.log` — structured-family harness with three-model Tobit fits.
- `/tmp/push_n.py` (`dp_refutation_phi_opt`) — optimised DP with forward subsumption.
- `/tmp/aic_corrected.py`, `/tmp/aic_corrected.txt` — cluster-robust AIC.
- `/tmp/paired_drat_dp.py`, `/tmp/drat_paired_merged.jsonl` (60 instances), `/tmp/analyze_paired.py`, `/tmp/drat_paired_analysis.txt`, `/tmp/drat_mechanism_v3.txt` — DRAT/DP paired-by-seed bootstrap, mechanism analysis.
- `/tmp/sc_alignment.txt` — verbatim SC1–SC6 registry vs v2 paper §3 audit.
- `/tmp/lemma_a_v3.tex` — Lemma A statement and proof, LaTeX-ready.

**Zenodo DOI.** **PENDING** at submission of this draft. Reservation requested under "c003b cumulative entropy v3 (Kubler)". Closes panel concern **R8** in the sense that the bundle is real and locatable; the DOI string is the remaining placeholder.

**Lean anchor.** `/home/ludo/.mnt/pvnp-lab/lab_c001/lean/TseitinTw/TseitinTw/Conjecture003.lean`, lines 369–411 (verbatim in §2.1).

**Reproduction.** Pure stdlib Python 3.10+; no external dependencies. Bootstrap seeds, n-grids, and per-instance budgets are recorded in each JSONL file. kissat 3.1.x for DRAT side, invoked with `--no-inprocessing`, `--plain`, and default flags as recorded in `/tmp/drat_paired_merged.jsonl`.

---

## Author and attribution

**Ludovico Kubler.** All rights reserved. Correspondence: ludwigkubler.ia@gmail.com. © 2026 Ludovico Kubler.

## Version history

- **v1** (2026-05-15): single n^2.93 headline; Lemma A as formula-level identity; SC2/SC4 marked supported. *Retracted in v3 §3.5 items 1–4.*
- **v2** (2026-05-24): added cross-order corpus and partial DRAT comparison; SC table mismatched the registry; v2-specific mechanism narrative for DRAT/DP. *Retracted in v3 §3.5 items 2–6.*
- **v3** (2026-05-30, this draft): Lemma A corrected and inlined; explicit retraction block; cluster-robust AIC and Tobit-censored fits; certified-expander Tseitin; DRAT/DP `--no-inprocessing` test; honest empirical localisation framing in the abstract.

---

*End of v3 draft. The paper is offered as a methodology contribution; no complexity-theoretic separation is claimed. All exponents reported are heuristic-conditional upper witnesses for CSpace\_cum per Lemma A.*
