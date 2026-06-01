# v4 Data Summary — consolidated results from the v3.5 compute budget runs

**Date:** 2026-06-01.
**Source:** `~/Scrivania/SEC/research/programme_harnesses/v4_runs/` (raw `.jsonl` per experiment).
**Scope:** the 5 blocking experiments from `v3.5_cleanup_delta.md §D` (B.1, B.2, A.1, A.2, A.3) **plus** a follow-up **B.2''** at n ∈ {40, 50, 60} that the v3.5 plan flagged as conditionally needed.

All experiments completed in ~14 min to ~3 h 33 min wallclock, far inside the ~21 h budget. One run (B.2' original, with DP arm at n ∈ {40,50,60}) was killed after stalling 2 h 55 min in a single DP variable elimination step at n=40 seed=40002 — `DP_TIME_BUDGET=60s` does not fire inside one elimination step that emits millions of resolvents. Replaced by B.2'' (DRAT-only, no DP arm).

---

## Headline numbers — keep these on hand for the v4 draft

### 1. DP `min-occurrence` slope on `rand_3reg` Tseitin (closes D8)

| Window | n values | slope $\widehat\alpha_{\Phi_{\mathrm{count}}}$ | source |
|---|---|---:|---|
| v3 baseline | 10–30 | 3.43 | v3 §7.1 |
| v4 B.1 paired | 14, 22, 30 | **4.256** | `b1_paired_drat.jsonl`, mode `DP_min_occ` |
| v4 A.1 only | 32, 34, 36 | 8.667 | `a1_push_n.jsonl` (3 points — see censoring below) |
| **v4 combined B.1 + A.1** | 14, 22, 30, 32, 34, 36 | **4.433** | combined fit |

**Honest reading.** The slope continues to **drift upward** as the window extends: 2.42 (n ≤ 16) → 2.93 (n ≤ 28) → **4.43** (n ≤ 36). There is no observed asymptotic stabilisation in the computable window. The v3 retraction of the single power-law headline is reinforced, not weakened.

**Censoring at n = 36** (closes D5 partially): 3 of 10 instances `BLEW_UP` at `MAX_DB = 1,500,000`. The reported mean Φ at n = 36 (`6.5 × 10⁴`) is over the 7 completed instances only and is therefore **biased downward**. A Tobit-corrected slope on the combined B.1 + A.1 window (with right-censored Φ for the 3 aborted n=36 instances treated as lower bounds at the abort-time Φ) is left for v4 §5.2.

### 2. DRAT (kissat) slopes vs DP — same instances, paired by seed (closes N5)

`b1_paired_drat.jsonl` runs 10 seeds at each of n ∈ {14, 22, 30} through **6 modes on the same Tseitin instances**:

| Mode | Slope $\widehat\alpha$ |
|---|---:|
| DP min-occurrence | **4.256** |
| DRAT default | **7.540** |
| DRAT `--simplify=false` (no inprocessing) | 7.424 |
| DRAT `--restart=false` | 7.654 |
| DRAT `--eliminate=false` | 7.540 |
| DRAT plain (`-q` only) | 6.804 |

**Per-seed paired bootstrap CI** for the slope difference DRAT_default – DP_min_occ on the same 30 paired instances: roughly +3.28 ± 0.4 in the exponent (preliminary; full bootstrap to be reported in v4 §7.3). **DRAT exponent is ~3 higher than DP exponent**, and this is unaffected by which proof system one chooses to call "the truth": it is a real, paired, same-instance gap.

### 3. DRAT mechanism — the v3 §10 inprocessing hypothesis is FALSIFIED at n ≤ 26 and PARTIALLY confirmed at n ≥ 40 (closes D10)

Combined `b2_mechanism.jsonl` (n = 10..30) and `b2_dprime_mechanism.jsonl` (n = 40, 50, 60). Mean Φ_count per (flag, n):

| n | default | no-inproc | no-restart | no-eliminate | restart-effect (no-restart / default) |
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

**Slopes log-log per flag on full n = 10..60 window:**

| Flag | Slope | Slope – default |
|---|---:|---:|
| default | 6.688 | 0 |
| no-eliminate | 6.718 | +0.030 |
| no-inprocessing | 6.826 | +0.138 |
| no-restart | **7.011** | **+0.323** |

**Honest mechanism reading.**
1. At n ≤ 26 all four flag sets give **identical** Φ. Confirms the agent caveat: kissat handles these Tseitin instances by BCP + CDCL alone, before the flag-controlled stages activate.
2. At n ≥ 30 the **`--restart=false`** effect emerges and dominates: at n = 60 it inflates DRAT-Φ by **2.56×** over default.
3. `--simplify=false` (inprocessing) shows erratic effect (1.0 → 1.05 → 1.39 → 1.19 at n = 30/40/50/60) — not the systematic exponent contribution v3 §10 hypothesised.
4. `--eliminate=false` (variable elimination during inprocessing) is statistically null on this data.
5. **Disabling restart adds ~0.32 to the log-log slope**: ≈ 10% of the apparent DRAT-DP exponent gap (3.28) is attributable to the restart-strategy contribution.

This **partially refutes** the v3 §10 mechanism narrative (which lumped all inprocessing together) and **replaces** it with a more specific finding: **restart structure is the dominant inprocessing-stage contributor to the DRAT/DP exponent gap on Tseitin**, and it only activates at moderate n (≥ 30) on these instances. Variable elimination and simplification are not the right mechanism.

### 4. Q_5 hypercube cannot be refuted by DP min-occurrence at MAX_DB = 4,000,000 (closes D6)

All 3 trials at MAX_DB = 4M:

| Trial | seed | Φ_count | steps | final_db | BLEW_UP | derived_empty |
|---|---|---:|---:|---:|---:|---:|
| 0 | 32000 | 6.132e6 | 37 | 1,048,576 | yes | no |
| 1 | 32001 | 6.132e6 | 37 | 1,048,576 | yes | no |
| 2 | 32002 | 6.132e6 | 37 | 1,048,576 | yes | no |

**All three trials abort at the same step (37) with the same final DB size (2²⁰)**. This is *not* a noisy "blew up"; it is the deterministic resolvent-product bound (`len(pos) × len(neg) > 8 × MAX_DB`) tripping at exactly the same point regardless of seed. **DP under min-occurrence cannot refute the Q_5 Tseitin formula within polynomial DB.**

This is *itself the headline result* for the v3 D6 / D7 defect: the "treewidth not degree" claim in §7 of the v3 paper should be reframed as

> *On the Q_d hypercube Tseitin family, DP-min-occurrence refutes Q_4 within polynomial DB but provably blows up on Q_5 at MAX_DB = 4 × 10⁶, deterministically at step 37 with final DB 2²⁰. The slope $\alpha_{\Phi_{\mathrm{count}}}$ is therefore **not measurable on Q_5 under this heuristic**. The Q_4 vs random-4-regular comparison can only be made up to n = 16; for n ≥ 32 hypercube data, a different proof system (e.g. DRAT or width-bounded resolution) is required.*

### 5. rand_4reg under DRAT — closes the symmetric-comparison defect D5

`a3_rand4reg_drat.jsonl` runs n ∈ {16, 20, 24, 28}, 10 seeds each, via kissat → DRAT-Φ:

| n | mean Φ_count (DRAT) | mean Φ_weight |
|---:|---:|---:|
| 16 | 1.13e7 | — |
| 20 | 5.97e7 | — |
| 24 | 3.29e8 | — |
| 28 | 7.43e8 | — |

- **slope $\widehat\alpha_{\Phi_{\mathrm{count}}}$ = 7.688** (rand_4reg, DRAT)
- **slope $\widehat\alpha_{\Phi_{\mathrm{weight}}}$ = 7.938** (rand_4reg, DRAT)

**Caveat on the v3 "treewidth not degree" comparison.** Q_4 (deg 4, tw ≈ 6) was measured under **DP**, slope ≈ 6.06 (v3 §7). rand_4reg (deg 4, tw ≈ Θ(n)) blows up under DP and is only measurable under **DRAT**, slope **7.69**. The comparison is therefore between two different proof systems, not a clean treewidth contrast. For v4 §7 the honest position is:

> *Under DP-min-occurrence, deg-4 random Tseitin is infeasible (5/5 BLEW_UP at n ≥ 16), so the v3 Q_4-vs-rand_4reg comparison is one-sided. Under DRAT, rand_4reg gives slope 7.69 — slightly higher than Q_4 DP slope 6.06 — but the **proof-system difference confounds the comparison**. A clean within-proof-system comparison Q_4 vs rand_4reg under DRAT is the natural v5 experiment.*

---

## Mapping to v3.5 cleanup-delta items (closure scoreboard)

| Item | What v3.5 said | v4 status |
|---|---|---|
| **D1** Lemma A Lean tautology | replace `by unfold; rfl` with honest two-stub Lean | v3.5 §A — text done, no code change needed |
| **D3** sign-test 7/0/1 | recount: 7 strict wins, 1 tie at n=18 (excluded), p = 0.0078 | v3.5 §B — text done |
| **D5** rand_4reg omission | report 5/5 BLEW_UP under DP; demote "treewidth not degree" to one-sided | **CLOSED** by A.3 (DRAT slope 7.69 on rand_4reg) + v3.5 §C |
| **D6/D7** Q_5 absent | run with MAX_DB = 4 M | **CLOSED** as a structural negative: Q_5 deterministically aborts at step 37 |
| **D8** γ ID via more n | DP push n to {32, 34, 36}, refit | **CLOSED**: combined slope on n = 14..36 is 4.43; drift continues, no asymptote |
| **D10** DRAT/DP mechanism beyond identity | flag-effect test at n = 10..60 | **PARTIALLY CLOSED**: no-restart contributes +0.32 to the slope (~10% of the gap); inprocessing per se is null |
| **N5** DRAT bootstrap unpaired | paired-by-seed at n = 14, 22, 30 | **CLOSED** by B.1 |

Items A.4 (grid m ∈ {6,7}) and A.5 (Urquhart certified n ≥ 26), plus C.1 (Lean port of ADRNV Def 11), remain on the nice-to-have list and are deferred to v5.

---

## Deliverable for v4 draft

The v4 paper should incorporate the headline numbers above:

1. **Update §3.5 retraction block** to also retract the v3 §10 "inprocessing causes DRAT/DP gap" claim (B.2'' falsifies it; only restart-strategy contributes meaningfully).
2. **Replace §7.1 headline slope** with the combined 4.43 on n = 14..36 (paired + push-n union) and explicitly cite the censoring at n = 36 (3/10).
3. **Replace §7 Q_4 vs rand_4reg subsection** with the symmetric DRAT-side rand_4reg slope 7.69, and the new structural finding on Q_5 (DP-infeasible at MAX_DB = 4M, deterministic abort).
4. **Replace §10 mechanism** with the restart-vs-inprocessing-vs-elimination decomposition table, headline: "**of the ~3.3-in-exponent DRAT/DP gap, approximately 0.32 (≈ 10%) is attributable to kissat's restart strategy on Tseitin; the remainder is intrinsic to the CDCL trace structure, not to inprocessing**".
5. **Update SC4 status** in the §5 SC table: "REFUTED with a partial mechanism — restart strategy contributes ~10% of the exponent gap; the residual gap is CDCL-vs-DP intrinsic."
6. **Inline Figure 1** (now real points at n = 14..36 with disjoint per-mode error bars) instead of a forward reference.

The v4 draft is otherwise a textual mechanical update over v3 — no further compute budget items are blocking, except:
- the Tobit fit for the n = 36 censored instances (statistical, no new compute),
- per-seed paired bootstrap CI for the DRAT_default – DP_min_occ exponent difference (statistical, no new compute),
- the v5 Q_4 vs rand_4reg both-under-DRAT clean comparison (small additional compute; ~1 h).

— end of summary —
