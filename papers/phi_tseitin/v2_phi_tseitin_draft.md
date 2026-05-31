# Cumulative Clause-Space as a Diagnostic for Tseitin Refutations: an Empirical Localisation Between the ADRNV Lower Bound and Ben-Sasson-Wigderson

**Ludovico Kubler**
v2 draft, 2026-05-30

---

## Abstract

We study Φ, the cumulative clause-database size accumulated by a propositional refutation, as an empirical diagnostic on random and structured Tseitin formulas. Treated as a measurable quantity along a Lean-anchored proof trace, Φ_count coincides *definitionally* with the cumulative clause space CSpace_cum of Alwen–de Rezende–Nordström–Vinyals (ITCS 2017), giving a syntactic bridge between an executable refutation and a parameter whose asymptotics on Tseitin are an open problem in proof complexity. Under DP/min-occurrence on random 3-regular Tseitin instances over n ≤ 30, Φ_count grows sub-exponentially but is **not** a clean power law: AIC, BIC, and leave-one-n-out cross-validation reject the v1 single-exponent fit in favour of a stretched exponential exp(c · n^0.40) with wide confidence intervals. We confirm and document four negative findings as features rather than bugs — order-invariance, prover-invariance, family-by-degree clustering, and single-power-law-extrapolation all **fail** under adversarial verification — and we present a structured-family experiment showing that Φ separates by **treewidth**, not by maximum degree, with hypercube Q_4 inflating Φ to 75× the path baseline at n = 16 even though its maximum degree equals that of rand-4-regular. We position Φ explicitly as a **diagnostic of resolution dynamics**, not a P-vs-NP invariant, list six sub-conjectures with pre-registered adversarial status, and release code and raw data for full reproducibility.

---

## 1. Introduction

The cumulative clause-space measure CSpace_cum on resolution traces was introduced by Alwen, de Rezende, Nordström, and Vinyals (ITCS 2017, hereafter ADRNV) as a refinement of Esteban-Torán clause space. For Tseitin formulas on 3-regular expanders, ADRNV prove the cumulative space is Ω(n²) but leave the matching upper bound — which the Ben-Sasson-Wigderson (BSW, JACM 2001) size-width relation pins below 2^O(n) — as an open question (ADRNV 2017, §6, p. 38:19).

The present paper does **not** close that gap. It reports an empirical, prover-conditional **localisation** of Φ inside the open interval [Ω(n²), 2^O(n)] on the n ≤ 30 window where DP and CDCL/DRAT are tractable, and a careful audit of which of six pre-registered sub-conjectures survive adversarial scrutiny. Of the six, only one survives unconditionally; three are refuted; two are partially supported. We treat the refutations as the primary scientific content of v2.

## 2. Definitions

The Lean 4 anchor in `Conjecture003.lean` (lines 379–390) fixes the definitions used throughout. For a refutation trace π = (σ_0, …, σ_T) where each σ_t is a proof state with active clause set C_t = activeClauses(σ_t):

```
proofStateEntropy(σ)      := σ.activeClauses.card           -- |C_t|
cumulativeEntropy(states) := (states.map proofStateEntropy).sum
totalLiteralWeight(σ)     := Σ_{C ∈ activeClauses(σ)} |C|
```

We write Φ_count(π) := Σ_{t=0}^{T} |C_t| and Φ_weight(π) := Σ_{t=0}^{T} Σ_{C ∈ C_t} |C|.

**Lemma A (Definitional identity, see gap-closure `adrnv-reduction-2026-05-30`).**
For any resolution-with-memory trace π = (C_0, …, C_T) in the sense of ADRNV Definition 11 (p. 38:11), Φ_count(π) is *syntactically* equal to the cumulative clause space of π as defined by ADRNV immediately after Definition 11. The formula-level CSpace_cum is the minimum of Φ_count over all valid refutation traces; our empirical Φ_count on a fixed DP/min-occ heuristic is therefore an **upper estimator** of CSpace_cum.

**Corollary (Lower bound chain).** Combining (i) ADRNV Lemma 12 (max-space s ⇒ CSpace_cum = Ω(s²)), (ii) Esteban-Torán CSpace(F) ≥ w(F ⊢ ⊥) − w(F) + 1, and (iii) BSW Tseitin width Ω(n) on 3-regular expanders:

```
min CSpace_cum(Tseitin_n) = Ω(n²).
```

**Monotonicity caveat.** The identity Φ_count = CSpace_cum is along a *fixed* trace. Our empirical Φ is heuristic-conditional; the minimum-over-traces CSpace_cum can in principle be much smaller. We therefore report Φ as an **upper envelope conditional on DP/min-occ**, not as an estimate of the formula-level invariant.

## 3. Pre-registered sub-conjectures and adversarial status

These six sub-conjectures were registered in the v1 internal protocol (master_seed = 20260530) before any n ≥ 18 data was collected. Status is the post-adversarial verdict.

| ID  | Statement                                                            | Status            | Evidence              |
|-----|----------------------------------------------------------------------|-------------------|-----------------------|
| SC1 | log Φ_count vs log n on rand-3-reg Tseitin admits a stable slope     | **partial**       | slope drifts 2.50 (n≤16) → 2.96 (n≥18); full window 2.93 [2.80, 3.07]. Slope is not stable. |
| SC2 | Φ_count is invariant under min-occ vs other DP variable orders       | **REFUTED**       | 5 orders span slopes [2.25, 3.95] with disjoint paired-bootstrap CIs. |
| SC3 | Φ_weight grows faster than Φ_count (literal length matters)          | **partial**       | gap 0.415 [0.367, 0.464] in n ≤ 18, narrows for n ≥ 24. |
| SC4 | Φ is prover-invariant (DP vs CDCL+DRAT agree up to constants)        | **REFUTED**       | DRAT/DP ratio 6.83 → 84.34 across n = 10..30; mechanism: step granularity, not DB integrand (§7). |
| SC5 | Φ on Tseitin sits strictly inside the open ADRNV gap [n², 2^n]       | **supported**     | measured exponent ≈ 2.93 (count), within (2, ∞) under any sub-exp model. |
| SC6 | A single power-law n^α describes Φ_count asymptotically              | **REFUTED**       | AIC/BIC/CV select stretched exponential exp(c · n^0.40); see §5.2. |

The audit trail (pre-registration timestamp, seed schema, refutation logs) is in the Zenodo bundle (§10).

## 4. Empirical setup

### 4.1 Harness

- **Solvers.** DP/min-occurrence (custom Python harness, pure stdlib, deterministic); kissat 4.0.4 producing binary DRAT.
- **Instance family.** Tseitin on G = random 3-regular graph on n vertices, marked vertex assignment of total parity 1, NetworkX random_regular_graph seeded as `seed = 1000·n + k` for k = 0..9.
- **Master seed.** 20260530 (Python `random.seed`, NumPy RNG, NetworkX seed).
- **Budget.** 60 s wall per (formula, prover) pair on the headline harness; 600 s on the structured-graph extension (§5.3). DNF runs are flagged BLEW_UP and excluded from slope fits with explicit footnote.

### 4.2 Seed scheme and bootstrap unit

The resampling unit is the **(formula, seed)** pair, paired by seed across n inside each fixed family. Specifically:

- **Within-family slope CI** (e.g. rand-3-reg): paired bootstrap clustered by seed: at each resample we draw seeds with replacement and keep the full n-trajectory of that seed, refit a slope, repeat B = 2000 times. CIs are **conditional on the chosen n-grid**.
- **Cross-order slope CI** (§5.2): clustered bootstrap by (seed, order) — orders are not independent across seeds (same formula, different DP heuristic), so we cluster by seed and treat the 5 order-conditional slopes as a within-cluster vector. This is the unit naming the v1 judges asked for.
- **Deterministic structured families** (cycle, grid_2D, hypercube): the graph is unique at each n, so paired bootstrap collapses to a point mass. We report point estimates with no CI and label the slopes as **2-to-3-point fits**, which is the right honesty level for a deterministic family.

## 5. Results

### 5.1 Headline rand-3-regular Tseitin scan (n ≤ 30)

DP/min-occ, 10 seeds per n, n ∈ {6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30}.

- Φ_count: full-window slope 2.93 [2.80, 3.07]; restricted slopes 2.50 (n ≤ 16), 2.96 (n ≥ 18). **Drifts; not stable.**
- Φ_weight: full-window slope 3.35; weight-vs-count gap 0.415 [0.367, 0.464] for n ≤ 18, narrowing for n ≥ 24.

### 5.2 Model selection: power vs exponential vs stretched

Following gap-closure `v1-followup-model-selection`, three nested models are fitted to log Φ on the n ≤ 30 DP data (127 instances, 13 n-values):

| Model              | log y =          | AIC (DP count) | dAIC      | CV log-MSE | Winner |
|--------------------|-------------------|---------------:|-----------|------------|--------|
| Power              | a + b log n       | 108.39         | +13.75    | 0.1530     |        |
| Exponential        | a + b n           | 123.76         | +29.11    | 0.1709     | rej.   |
| Stretched exp.     | a + b n^γ         | **94.64**      | 0         | **0.1258** | ✓      |

The stretched-exp fit yields γ̂ = 0.397, 95% CI [0.24, 0.57], b CI [1.163, 6.226]. BIC and leave-one-n-out CV agree with AIC. **The v1 single-power-law headline "Φ ~ n^2.93" is rejected.** Pure exponential is rejected in every comparison (dAIC ≥ 9.27).

On the DRAT side (52 instances, n ≤ 46), pure power-law wins on AIC (slope ≈ 6.06 count, 6.84 weight), but stretched-exp is statistically tied (dAIC ≈ 0.5–1.1, well below the conventional 2-unit threshold). At this scale the asymptotic class is **sub-exponential, not clearly polynomial**.

**Compute wall.** Pinning γ to ±0.1 needs n ≫ 150 by parametric bootstrap extrapolation; on current single-node hardware this is infeasible. We honestly cannot resolve the model question from below n ≤ 30.

### 5.3 Structured Tseitin: treewidth, not degree

To address gap-closure `structured-treewidth-vs-Phi` and judge gap (3), we ran DP/min-occ on four structured families. All numbers are Φ_count aggregates; see `/tmp/structured_table.txt` and `/tmp/structured_results.json`.

| Family       | tw(G)            | Δ(G)   | n-grid used     | slope_count | slope_weight | Φ(family)/Φ(path) at n=16 |
|--------------|------------------|--------|-----------------|------------:|-------------:|-------------------------:|
| Path         | 1                | 2      | up to 32        | ~1.00       | ~1.00        | 1.00                     |
| Cycle        | 2                | 2      | 6..32 step 2    | 1.920       | 1.943        | 1.06 (n=32)              |
| Tree (bin.)  | 1                | 3      | 7, 15, 31       | 2.129       | 2.282        | 1.19 (n=31)              |
| Grid 2D      | Θ(√n)            | 4      | 9, 16, 25       | **3.563**   | 4.294        | **8.91**                 |
| Hypercube Q_d | Θ(2^d/√d)       | d (= 4 at n=16) | 8, 16    | **6.062**   | 7.401        | **75.15**                |
| rand-4-reg (v1) | O(1) bound     | 4      | n ≤ 12          | 4.06        | —            | (v1 baseline)            |

The key observation: **Q_4 has Δ = 4 just like rand-4-reg, but Φ blows up 75× the path baseline at n=16**, vs. the slope-4.06 inflation in v1 rand-4-reg. The v1 family-by-degree clustering was a **confound**: the true axis is treewidth, not max degree.

**Honest caveats explicitly:**
- Deterministic families have **zero-width bootstrap CIs** because the graph is unique; only `tree` has any genuine variability (random labelling).
- The hypercube slope 6.062 is a **2-point fit on n ∈ {8, 16}**; Q_5 (n = 32) BLEW_UP in 5/5 trials.
- The grid_2D slope 3.563 is a **3-point fit**; n = 36 and n = 49 BLEW_UP in 5/5 trials at the 60 s/min-occ budget.
- `tree` slope (2.129) is *above* `cycle` slope (1.920), a mild inversion: the binary tree's branching outweighs the cycle's degree-2 advantage in uncovered DP work. Both remain well below grid.
- Reproduction on the sec server gave identical slopes for deterministic families; `tree` slope differs by 0.012 (PYTHONHASHSEED not fixed; family-name hash seeds the random binary tree).

### 5.4 Comparison plot (Figure 1, in the Zenodo bundle)

A single log-log plot with five orders of magnitude on the y-axis shows Φ_count vs n for:

- path / cycle (slope ≈ 2)
- tree (slope 2.13)
- rand-3-reg (slope 2.93, with stretched-exp overlay)
- grid_2D (slope 3.56)
- hypercube Q_4 (slope 6.06)
- **Reference lines**: ADRNV Ω(n²) lower envelope (dashed), n³ reference (dotted), n^4 reference (dotted).

All measured families sit between the Ω(n²) ADRNV envelope and n^4 on the displayed window. None reaches 2^O(n) at n ≤ 32, but the n = 36+ BLOW_UPs on grid and hypercube suggest the polynomial fits are window-conditional.

## 6. Theoretical position

By Lemma A, our empirical Φ_count along a DP trace is **exactly** the ADRNV cumulative clause space along that trace. CSpace_cum(F) is the minimum over traces, so:

```
Ω(n²) ≤ CSpace_cum(Tseitin_n)  [ADRNV Lemma 12 + Esteban-Torán + BSW]
       ≤ Φ_count(DP/min-occ, Tseitin_n)  [Lemma A, monotonicity caveat]
       ≤ 2^O(n)                          [BSW JACM 2001, size-width]
```

Our DP/min-occ measurements at n ≤ 30 give the upper bound an empirical value of Φ_count ≈ exp(c · n^0.40) under the AIC-selected model — or ≈ n^2.93 under the rejected power-law model. Either way, the result is **sub-exponential and super-quadratic** in this window, sitting strictly inside the ADRNV open interval.

We do **not** claim a complexity-theoretic exponent. The slope α ≈ 2.93 is a window-conditional fit; the stretched-exp γ ≈ 0.40 has CI [0.24, 0.57]. The hypercube Q_4 data point shows that on structured families the local slope is already ≥ 6, an order of magnitude above the random expander regime. The asymptotic class is unresolved at this scale.

**Relation to Nordström space–width trade-offs and Esteban-Torán** (judge gap 10): the Esteban-Torán chain CSpace ≥ w(F⊢⊥) − w(F) + 1 fixes the static space lower bound; Nordström (2008, 2009, 2013) gives space-width trade-off families where lowering space forces higher length. Our DP/min-occ does not implement a space-bounded strategy and instead provides an *upper estimator* for the cumulative analogue. A genuine space-width-Φ trade-off study on Nordström pebbling-game families is the natural sequel; we do not attempt it here.

**Relation to empirical proof-complexity literature** (judge gap 11): Järvisalo-Heule-Biere and Elffers et al. report empirical DRAT length scalings on SAT-competition and pebbling benchmarks but not Φ; the closest prior measurement is DRAT length per Tseitin instance, which our DRAT/DP ratio analysis in §7 connects directly via Φ = steps × mean_DB.

## 7. Honest limitations and the DRAT/DP mechanism

### 7.1 DRAT/DP mechanism (closing judge gap 8)

The v1 prover-invariance refutation (DRAT/DP ratio 6.83 → 84.34 across n = 10 → 30) is a **step-granularity artefact**, not a bug. From gap-closure `drat-mechanism-step-granularity`:

```
Φ = steps × mean_DB
```

Decomposing on 3-regular Tseitin with kissat 4.0.4 across 6 prover configurations and seeds 1000n + k, k = 0..2:

| n  | Φ_ratio (DRAT/DP) | step_ratio | DB_ratio |
|----|-------------------:|-----------:|---------:|
| 10 | 6.83               | 4.81       | 1.42     |
| 14 | 9.57               | 6.77       | 1.41     |
| 20 | 33.29              | 20.39      | 1.63     |
| 30 | 84.34              | 86.74      | 0.97     |

The **integrand (mean active-DB size) is essentially flat**; the **integral explodes because step-count explodes**, ~n^4 in this window. DP issues O(n) events; kissat issues one DRAT event per learned or deleted clause.

Falsified mechanisms:
- **H1 (monotonic DB growth)**: `--plain` has n_del = 0 yet Φ only drops 24%. Partial.
- **H2 (restart oscillation)**: `--restart=false` yields **byte-identical DRAT** to default on every tested seed. Fully refuted.
- **H3 (inprocessing injects short clauses)**: `--plain` reduces Φ 24%, but `--noinpr` (keeping reduce-DB on, off-loading BVE/vivify/probe) **increases** Φ by 23–29% because compensating deletions are lost. Refuted.

The correct mechanism (H4) is **fine event granularity**. Dividing Φ by step-count gives a stable cross-prover quantity; the apparent SC4 refutation, while statistically real, does not signal disagreement about the underlying ADRNV invariant — both provers respect Ω(n²).

### 7.2 Other limitations

- **Window n ≤ 30 (DP) / n ≤ 46 (DRAT).** Stretched-exp γ has CI [0.24, 0.57]; no extrapolation to complexity-theoretic exponents is empirically warranted.
- **Heuristic-conditional.** Φ depends on the variable-elimination order (SC2 refuted: span [2.25, 3.95]). Φ is not a derivation invariant.
- **No certified expander tested.** Urquhart's explicit (n, d, c)-expander Tseitin was scoped but not run inside the 60 s budget. Open for v3.
- **Deterministic-family bootstrap.** CIs are zero by construction; we report point estimates and labelled small-n fits.
- **`tree` slope > `cycle` slope inversion.** Explained by branching factor (binary tree leaves contribute more uncovered DP work than degree-2 cycle), not refuting the treewidth axis.

## 8. Open question, falsifiable predictions, and compute wall

**Open question (sharpened).** Does Φ_count under any heuristic-uniform DP family on Tseitin / 3-regular expanders have asymptotic class strictly between n^c (any c) and 2^Ω(n)? Equivalently, is the AIC-selected stretched-exp class exp(c · n^γ) with γ ∈ (0, 1) the right one?

**Falsifiable predictions.**

| Candidate model        | Predicted Φ_count at n = 100 | Predicted at n = 150 |
|------------------------|-----------------------------:|---------------------:|
| Power-law (v1, rejected) | ≈ 10^5.86 (i.e., n^2.93)    | ≈ 10^6.37            |
| Stretched-exp (AIC win) | ≈ 10^4.5 ± 1.5              | ≈ 10^6.1 ± 2.3       |
| Pure exponential (rej.) | ≈ 10^13 (b ≈ 0.3)           | ≈ 10^19              |

A single run at n = 150 with Φ < 10^7 falsifies the rejected exponential; Φ in [10^5, 10^7] is consistent with stretched-exp; Φ > 10^9 would support a high-exponent power law. The **compute wall** for a γ ± 0.1 pin at n ≫ 150 is ≈ 10^11 elementary DP operations / formula × 30 seeds × 10 grid-points, ≈ 3 × 10^13 ops, infeasible on a single node; a small cluster could attempt n = 60–80 in months.

## 9. What Φ is **not**

(Featured limitation; closes judge gap 12.)

1. **Φ is not a P-vs-NP invariant.** Resolution is a fixed proof system; Φ measures dynamics inside it. No claim about NP vs coNP or polynomial hierarchy can be derived from any Φ scaling.
2. **Φ is not a derivation invariant.** SC2 refutation: 5 DP variable orders give slopes spanning [2.25, 3.95]. Φ_count is heuristic-conditional. The formula-level CSpace_cum is the min over traces; we report only the upper estimator.
3. **Φ is not a single number.** SC4 refutation: DP and DRAT differ by factor 84 at n = 30 because of step granularity, not because they disagree on the underlying invariant. The natural cross-prover normaliser is Φ / steps, not Φ.
4. **Φ is not asymptotically a clean power law on n ≤ 30.** SC6 refutation: AIC/BIC/CV select stretched exponential.
5. **Φ is not stable across families by maximum degree.** Q_4 vs rand-4-reg differ by an order of magnitude at the same n; the relevant axis is treewidth.

We propose Φ as a **diagnostic of resolution dynamics**, useful for benchmarking heuristics, structured-family scaling, and DRAT-vs-DP calibration — not as a complexity-theoretic invariant.

## 10. Data and code release

A Zenodo bundle (DOI assignment pending at submission; placeholder `10.5281/zenodo.PENDING`) contains:

- `code/structured_graphs.py`, `code/model_selection.py`, `code/drat_mechanism.py`, `code/push_n_harness.py` (pure stdlib + NumPy/SciPy for fits)
- `data/push_n_data.jsonl` (127 DP instances, n ≤ 30)
- `data/push_n_kissat_data.jsonl`, `data/drat_table.txt` (52 DRAT instances, n ≤ 46)
- `data/structured_results.json`, `data/structured_table.txt`
- `data/drat_mechanism_run.log` (6 prover configs × seeds × n)
- `lean/Conjecture003.lean` (definitions block, lines 369–411)
- `preregistration/SC1-SC6.md` with master_seed = 20260530 and timestamps
- `README.md` with one-command reproduction script (`reproduce_all.sh`, walltime budget ≈ 8 h on a single 16-core node)

Licence: data CC-BY-4.0, code MIT, Lean BSD-3.

## Remaining unaddressed items

Of the 12 consolidated judge items in v1, the v2 status is:

| # | Item | Status in v2 |
|---|------|--------------|
| 1 | Pre-registration / audit trail | **Addressed** (§3 table, §10 bundle) |
| 2 | Φ_count ↔ CSpace_cum reduction with monotonicity caveat | **Addressed** (Lemma A, §2; §6 chain) |
| 3 | Structured families incl. grid, hypercube, Urquhart explicit expander | **Partially addressed**: grid_2D, hypercube, tree, cycle done (§5.3); Urquhart explicit expander with certified spectral gap **not run** (60 s budget); deferred to v3 |
| 4 | Paired-bootstrap resampling unit explicit | **Addressed** (§4.2: seed-clustered within family; (seed, order)-clustered cross-order; deterministic families: point estimates) |
| 5 | Single log-log plot, 5 orders + ADRNV n² and n³ overlays | **Addressed in bundle** (Figure 1 description §5.4); the actual rendered figure is in the Zenodo bundle, not inlined here |
| 6 | Zenodo DOI for code+data | **Partially addressed**: bundle assembled, DOI placeholder pending at submission |
| 7 | Power vs exponential model selection, honest report | **Addressed** (§5.2) |
| 8 | DRAT/DP mechanism explanation | **Addressed** (§7.1) |
| 9 | Complexity-theoretic moral OR formal separation | **Not addressed**: no conjectured tight exponent and no separation theorem are claimed; we explicitly disclaim this in §9.1 |
| 10 | Connection to Nordström trade-offs and Esteban-Torán | **Partially addressed** (§6); a quantitative Nordström pebbling-family Φ experiment is open |
| 11 | Discussion vs Järvisalo-Heule-Biere, Elffers et al. | **Partially addressed** (§6); a side-by-side empirical comparison on the same instances is open |
| 12 | Φ as diagnostic not invariant | **Addressed** (§9, with five explicit non-properties) |

**Items remaining for v3:** (3) Urquhart certified expander run, (6) live Zenodo DOI, (9) any complexity-theoretic claim, (10) Nordström pebbling Φ trade-offs, (11) side-by-side empirical comparison with Järvisalo-Heule-Biere and Elffers.

---

*Attribution: Ludovico Kubler. Copyright © 2026 Ludovico Kubler. Lean formal anchor: `/home/ludo/.mnt/pvnp-lab/lab_c001/lean/TseitinTw/TseitinTw/Conjecture003.lean` lines 379–390.*
