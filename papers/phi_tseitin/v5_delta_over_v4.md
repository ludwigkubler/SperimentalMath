# v5 Delta Over v4 — surgical close of E1, E2, E3

**Ludovico Kubler — 2026-06-01**

## v4 to v5 changelog

- **E1 (Section 3, Lemma A part ii):** replace the v4 "immediate from min-over-traces" justification with an explicit re-scheduling construction. The directional inequality $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \ge \mathrm{CSpace}_{\mathrm{cum}}(F)$ is **retracted**; what survives is the one-sided bound $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \le \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h})$ where $\pi'_{\mathrm{DP},h}$ is the canonical primitive expansion of the DP run. Touches v4 lines 99–104 (Lemma A statement), line 134 (Corollary C2 chain), line 423 (downstream Proposition), line 476 (limitations item 1), and the abstract "upper witness" language on line 11.
- **E2 (Section 9, Corollary C2):** replace the v4 chain "ADRNV Lemma 12 + Esteban–Torán $\Rightarrow$ $\mathrm{CSpace}_{\mathrm{cum}}(\mathrm{Tseitin}_n) = \Omega(n^2)$" with the corrected linear-only bound $\Omega(n)$, and a precise statement of why the quadratic does not chain (peak-vs-plateau gap; ADRNV open problem on p.38:19 remains open).
- **E3 (Section 10, mechanism slopes):** replace the bare "+0.323 no-restart" claim with the paired-by-seed cluster bootstrap (B = 2000) result, including the leave-n=60-out sensitivity and the tied-cell diagnostic. The effect survives the full-range fit (CI excludes zero) but is concentrated at $n=60$; the no-inprocessing effect is suggestive, the no-eliminate effect is null.

The three replacements are surgical. The v3$\to$v4 modifications M1–M6 and the v3.5 fixes are preserved.

## Section 3 (Lemma A part ii) — replacement text

**Lemma A (part ii — formula-level relation, schedule-bookkeeping inequality).** We replace the v4 draft's "immediate from min-over-traces" wording, which conflated coarse-grained DP elimination steps with primitive resolution-with-memory steps in the sense of ADRNV Definition 11.

*Setup.* ADRNV's resolution-with-memory model has three primitive operations: (a) **download** a clause of $F$ into the memory configuration $M$, (b) **inference**, which adjoins to $M$ a resolvent of two clauses already in $M$, (c) **erasure**, which deletes a clause from $M$. The cumulative space of an admissible trace $\pi' = (M_0, M_1, \ldots, M_{T'})$ is $\mathrm{CSpace}_{\mathrm{cum}}(\pi') := \sum_{t=0}^{T'} |M_t|$, and $\mathrm{CSpace}_{\mathrm{cum}}(F) := \min_{\pi' \text{ admissible refuting } F} \mathrm{CSpace}_{\mathrm{cum}}(\pi')$.

A Davis–Putnam elimination step on variable $v$ is **not** a primitive res-with-memory operation. It is a macro: download every clause of the current active set that mentions $v$ (if not yet downloaded), form every pairwise resolvent on $v$, and erase every clause mentioning $v$. The Lean `ProofState.activeClauses` after the $t$-th elimination corresponds to a memory configuration $M_t^{\mathrm{DP}}$, but $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) := \sum_t |M_t^{\mathrm{DP}}|$ sums only over **macro-checkpoints**, one per eliminated variable.

*Re-scheduling claim.* Any DP-min-occ run on $F$ can be expanded into an admissible res-with-memory trace $\pi'$ whose checkpoint memory states at the macro-boundaries coincide with the $M_t^{\mathrm{DP}}$. Concretely, between checkpoints $t$ and $t+1$ the expansion inserts (i) the downloads of the not-yet-downloaded $v_{t+1}$-clauses, (ii) the pairwise resolutions on $v_{t+1}$, (iii) the erasures of the original $v_{t+1}$-clauses. Each intermediate $|M|$ in this expansion is **at least** the smaller of $|M_t^{\mathrm{DP}}|$ and $|M_{t+1}^{\mathrm{DP}}|$ (monotone phases) and may transiently exceed both during the resolution phase before the matching erasures.

*Consequence — the honest direction.* Because $\pi'$ contains additional summands (the primitive intermediates), $\mathrm{CSpace}_{\mathrm{cum}}(\pi') \ge \Phi_{\mathrm{count}}^{\mathrm{DP},h}(F)$. Taking the min over all admissible refutations yields
$$
\mathrm{CSpace}_{\mathrm{cum}}(F) \;\le\; \mathrm{CSpace}_{\mathrm{cum}}(\pi') \;\not\!\le\; \Phi_{\mathrm{count}}^{\mathrm{DP},h}(F).
$$
The min-over-traces argument therefore does **not** discharge $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \ge \mathrm{CSpace}_{\mathrm{cum}}(F)$. The v4 draft's one-line justification ("immediate from min-over-traces: DP under any fixed $h$ realises one specific admissible trace") is wrong: the DP trace is not, qua sum, a res-with-memory trace, and its primitive expansion has strictly more summands than $\Phi_{\mathrm{count}}$ counts.

*Restated formula-level relation (corrected).* The strongest defensible statement is the schedule-specific one:
$$
\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \;=\; \sum_{t=0}^{T} |M_t^{\mathrm{DP},h}| \;\le\; \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h}),
$$
where $\pi'_{\mathrm{DP},h}$ is the canonical primitive expansion above. We do **not** claim $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \ge \mathrm{CSpace}_{\mathrm{cum}}(F)$. We claim only that the macro-checkpoint sum $\Phi_{\mathrm{count}}$ is a **lower estimator** of the cumulative space of *one* admissible refutation (its own expansion), and that this expansion is one of the traces over which $\mathrm{CSpace}_{\mathrm{cum}}(F)$ takes its minimum. The directional consequence for the empirical work in §7 is:
$$
\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \;\le\; \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h}), \qquad \mathrm{CSpace}_{\mathrm{cum}}(F) \;\le\; \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h}).
$$
Both quantities are lower-bounded by the same admissible-trace cumulative space, but they are **not** ordered with respect to one another by this argument.

*Honest cascade into Corollary C2.* The v4 Corollary C2 chain
$$
\Phi_{\mathrm{count}}^{\mathrm{DP},\mathrm{min\text{-}occ}}(F_n) \;\ge\; \mathrm{CSpace}_{\mathrm{cum}}(F_n) \;\ge\; c \cdot n^2
$$
no longer goes through unconditionally. The second inequality is downgraded separately in §9 (E2) to a linear bound; the first does **not** follow from Lemma A as corrected here. C2 should therefore be downgraded on two grounds: $\mathrm{CSpace}_{\mathrm{cum}}(F_n) = \Omega(n)$ stands as a literature-derived lower bound (the $\Omega(n^2)$ does not), and $\Phi_{\mathrm{count}}^{\mathrm{DP},\mathrm{min\text{-}occ}}(F_n)$ remains a measured exponent on a fixed heuristic with **no formal ordering** to $\mathrm{CSpace}_{\mathrm{cum}}(F_n)$. The empirical $\alpha_{\Phi} \approx 4.43$ being **larger** than $2$ is consistent with $\Phi_{\mathrm{count}}$ sitting above $\mathrm{CSpace}_{\mathrm{cum}}$ on this regime, but it is not a proof of the ordering.

**Honesty disclosure.** Path A (showing the DP-trace sum *equals* a primitive res-with-memory cumulative space) does not close the gap: expansion strictly adds summands, so the expansion's cumulative space is $\ge \Phi_{\mathrm{count}}$, not $=$. The v4 directional claim $\Phi_{\mathrm{count}} \ge \mathrm{CSpace}_{\mathrm{cum}}$ is **retracted**. The "upper witness" language in the v4 abstract (line 11) and §7 — which depends on the retracted direction — is replaced throughout v5 with "schedule-specific measurement with no formal ordering to $\mathrm{CSpace}_{\mathrm{cum}}$".

## Section 9 (Corollary C2) — replacement text

**(i) ADRNV Lemma 12, stated precisely.** ADRNV (ITCS 2017, paper 38) work in the resolution-with-memory model: a refutation is a sequence of memory configurations $M_0, M_1, \ldots, M_L$, where each $M_t$ is a set of clauses derivable from $F$, $M_0 = \emptyset$, $M_L$ contains the empty clause, and successive configurations differ by axiom download, inference, or erasure. The *cumulative space* of a refutation $\pi$ is $\mathrm{CSpace}_{\mathrm{cum}}(\pi) := \sum_t |M_t|$, and the *space* is $\max_t |M_t|$.

Lemma 12 is a generic per-trace inequality: for any single resolution-with-memory refutation $\pi$,
$$
\mathrm{CSpace}_{\mathrm{cum}}(\pi) \;\ge\; \Omega\!\big(\,\max\!-\!\mathrm{space}(\pi)^2\,\big).
$$
The proof is a combinatorial growth argument: since $|M_0|=0$ and at most one clause is added per step, reaching a configuration of size $s$ requires at least $s$ steps, during which the average size is $\ge s/2$, so the partial sum is $\ge s^2/2$. This is a *per-refutation* statement, with "$s$" referring to the realized max-memory of *that specific trace*. It is **not** the formula-level statement $\mathrm{CSpace}_{\mathrm{cum}}(F) \ge \Omega(\mathrm{CSpace}(F)^2)$: the refutation achieving min cumulative-space and the refutation achieving min max-space need not be the same refutation.

**(ii) Esteban–Torán, stated precisely.** Esteban–Torán (CSL 1999) prove: for Tseitin formulas on bounded-degree expander graphs (in particular 3-regular expanders) on $n$ vertices, every resolution refutation $\pi$ satisfies $\mathrm{clause\text{-}space}(\pi) \ge n - O(1)$. Equivalently, $\mathrm{CSpace}(\mathrm{Tseitin}_n) \ge n - O(1)$ where the min is over all refutations. "Clause-space" in Esteban–Torán is the max number of clauses simultaneously in memory across the trace; this coincides with ADRNV's $\max\!-\!\mathrm{space}(\pi)$ in the standard resolution-with-memory model. The models do match.

**(iii) Where the chain breaks.** Naïve composition gives, for every $\pi$,
$$
\mathrm{CSpace}_{\mathrm{cum}}(\pi) \;\ge\; \Omega\!\big(\max\!-\!\mathrm{space}(\pi)^2\big) \;\ge\; \Omega\!\big((n - O(1))^2\big) = \Omega(n^2).
$$
The composition step is the slip. ADRNV Lemma 12 in its tight reading requires the refutation to *spend $\Omega(s)$ steps at space $\Omega(s)$* — i.e., to sustain a plateau of width $\Omega(s)$ — not merely to *touch* space $s$ once. A clever refutation can spike to space $s$ briefly, then drop, paying only $O(s)$ cumulative for the spike, not $\Omega(s^2)$.

Esteban–Torán guarantees the *peak* is $\Omega(n)$ but does **not** guarantee a *plateau* of width $\Omega(n)$. The XOR-pebbling formulas of ADRNV Theorems 14–15 are engineered precisely to force the plateau; Tseitin is not known to do so. Hence the ADRNV open problem on p.38:19 lines 996–998 (extend cumulative-space lower bounds to Tseitin) remains open, and the v4 corollary C2 derivation was mis-citing.

**(iv) Weakest defensible $\mathrm{CSpace}_{\mathrm{cum}}$ lower bound on Tseitin via this route.** The only bound that survives is the trivial one:
$$
\mathrm{CSpace}_{\mathrm{cum}}(\pi) \;\ge\; \max\!-\!\mathrm{space}(\pi) \;\ge\; n - O(1),
$$
i.e. $\mathrm{CSpace}_{\mathrm{cum}}(\mathrm{Tseitin}_n) = \Omega(n)$, linear, not quadratic.

**Corollary C2 (revised, honest form).** For Tseitin formulas on 3-regular expander graphs on $n$ vertices, every resolution refutation $\pi$ satisfies
$$
\mathrm{CSpace}_{\mathrm{cum}}(\pi) \;\ge\; \max\!-\!\mathrm{space}(\pi) \;\ge\; n - O(1),
$$
giving $\mathrm{CSpace}_{\mathrm{cum}}(\mathrm{Tseitin}_n) = \Omega(n)$ by Esteban–Torán (CSL 1999). The quadratic bound $\mathrm{CSpace}_{\mathrm{cum}}(\mathrm{Tseitin}_n) = \Omega(n^2)$ does **not** follow from ADRNV Lemma 12 + Esteban–Torán: Lemma 12's $s^2$ growth requires $\Omega(s)$ steps spent at space $\Omega(s)$, and Esteban–Torán only guarantees the peak is $\Omega(n)$, not that it is sustained. Extending the $\Omega(n^2)$ cumulative-space lower bound from ADRNV's XOR-pebbling formulas (Thm 14–15) to Tseitin remains the open problem stated by ADRNV (ITCS 2017, p.38:19 lines 996–998). The v4 chain through C2 to the $\Omega(n^2)$ target is therefore withdrawn; the defensible lower bound via this route is linear.

## Section 10 (mechanism, restart contribution) — replacement text

**Setup.** We loaded 180 rows from `b2_mechanism.jsonl` ($n \in \{10,14,18,22,26,30\}$) and `b2_dprime_mechanism.jsonl` ($n \in \{40,50,60\}$), 4 flag sets × 5 seeds (indexed $k \in 0..4$ within each $n$). The cluster-bootstrap ($B = 2000$) resamples $k$ with replacement and applies the **same** $k$-resample across all 9 $n$ values (paired structure); for each resample we recompute mean $\log \phi_{c,\mathrm{drat}}$ per (flag, $n$), refit the OLS log-log slope on the 9 $\log n$ values, and take $\mathrm{slope}_{\mathrm{flag}} - \mathrm{slope}_{\mathrm{default}}$. Full numerics at `/tmp/e3_bootstrap.txt` on the SEC server.

**Headline result on the full 9-point fit.**

| Contrast | Point | Boot median | 95% percentile CI | Excludes zero? |
|---|---|---|---|---|
| no-restart − default | +0.323 | +0.319 | [+0.213, +0.435] | yes |
| no-inprocessing − default | +0.137 | +0.123 | [+0.070, +0.179] | yes |
| no-eliminate − default | +0.030 | +0.029 | [−0.005, +0.073] | no |

Taken at face value, the v4 §10 +0.323 finding for no-restart **survives** the paired bootstrap on the full 9-point fit (CI strictly positive). It also reveals a smaller but CI-positive no-inprocessing effect that v4 §10 underweighted.

**Tied-cell diagnostic.** For $n \in \{10,14,18,22\}$, all 5 $k$-seeds give exactly the same $\phi_{c,\mathrm{drat}}$ across all four flags (20/20 ties for each non-default flag). For $n=26$ and $n=30$, only no-restart breaks a single tie (4/5 still tied). For no-inprocessing the first non-tied cell is $n=40$ (3/5 still tied) and the first majority-untied cell is $n=50$. No-eliminate is essentially flat: still 1/5 tied even at $n=60$. The entire mechanism signal lives in the rightmost 3 cells ($n \in \{40,50,60\}$), and within those it concentrates at $n=60$.

**Leave-$n=60$-out reweighting (refit on 8 $n$ values $\{10..50\}$).**

| Contrast | Point | 95% CI | Verdict |
|---|---|---|---|
| no-restart | +0.073 | [+0.031, +0.111] | still excludes zero, but 4× smaller |
| no-inprocessing | +0.138 | [−0.048, +0.316] | CI now crosses zero |
| no-eliminate | −0.003 | [−0.006, +0.000] | null |

**Leave-$n \ge 50$-out (b2 only, 6 $n$ values $\{10..40\}$).** No-restart slope difference is +0.128 with CI $[0.000, +0.390]$ — barely touches zero at the lower bound, no longer cleanly excludes; the other two flags collapse to zero (no-eliminate is identically zero because every cell is tied through $n=40$).

**Effective sample size.** Cluster bootstrap on 5 seed-clusters and 9 (highly correlated) $n$-fits gives an effective DoF dominated by the 5 clusters ($\sim$4). The 9 $\log n$ points are not independent — they share the same 5 underlying seed clusters — so headline CIs should be read with that caveat.

**Honest verdict on v4 §10.** The +0.323 no-restart finding is **real** on the full-range fit but **fragile**: its magnitude is dominated by the $n=60$ cell (drops to +0.073 without it), the lower-range cells ($n \le 22$) carry no information at all (20/20 ties), and the effective seed-cluster sample is only 5. The correct v5 language is:

> "no-restart shows a positive log-log slope shift of +0.32 [+0.21, +0.43] on $n \in 10..60$, but the effect is concentrated at the largest cell ($n=60$); excluding $n=60$ the shift drops to +0.07 [+0.03, +0.11], so the magnitude is not yet established and a push to $n=70..100$ is required before claiming a stable mechanism slope."

The no-inprocessing effect is reported as "suggestive (+0.14 [+0.07, +0.18] on full range) but CI crosses zero without $n=60$." The no-eliminate effect is reported as null. §10 receives a **downgrade in claim strength** but **not** a full retraction: the slope-difference CI for no-restart does exclude zero on the full 9-point fit, contrary to the panel's worst-case reading; the panel was right that $n=60$ carries the signal, and the push-$n$ campaign is the obligated next step.

Files: bootstrap output at `/tmp/e3_bootstrap.txt` on the SEC server; script at `/tmp/e3_bootstrap.py` on the SEC server and `/tmp/e3_bootstrap_local.py` locally.

## Updated retraction block addition for Section 3.5

- **v4 §3 Lemma A part (ii) directional claim** $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \ge \mathrm{CSpace}_{\mathrm{cum}}(F)$ is **withdrawn**. The DP elimination trace is not, qua sum, a primitive res-with-memory trace; its canonical primitive expansion has strictly more summands than $\Phi_{\mathrm{count}}$ counts, yielding only the one-sided $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \le \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h})$. See v5 §3.
- **v4 §9 Corollary C2 quadratic $\Omega(n^2)$ lower bound on $\mathrm{CSpace}_{\mathrm{cum}}(\mathrm{Tseitin}_n)$** is **withdrawn**; the chain from ADRNV Lemma 12 + Esteban–Torán does not deliver $n^2$ (peak vs. plateau gap; ADRNV open problem p.38:19 remains open). The defensible bound via this route is linear, $\Omega(n)$. See v5 §9 corrected statement.
- **v4 §10 "+0.323 no-restart" headline** is **not retracted but downgraded**: the full-range bootstrap CI excludes zero, but the effect is concentrated at $n=60$ and shrinks to +0.07 [+0.03, +0.11] without it. Claim language is rewritten accordingly; a push-$n$ campaign to $n = 70..100$ is the obligated next step. The no-inprocessing effect is downgraded to "suggestive"; the no-eliminate effect is reported as null.
- **v4 abstract and §7 "upper witness" language** is withdrawn wherever it depended on the retracted Lemma A directional claim, and replaced with "schedule-specific measurement with no formal ordering to $\mathrm{CSpace}_{\mathrm{cum}}$".

## What this does NOT change

Everything else in v4 stands. In particular:

- The **v3$\to$v4 modifications M1–M6** are preserved as written: the Lean anchor of `ProofState`, `proofStateEntropy`, and `cumulativeEntropy` (Conjecture003.lean lines 369–411) remains the formal definition $\Phi(T) = \sum_t H(\text{activeClauses}_t)$ underlying $\Phi_{\mathrm{count}}$ at $h \equiv 1$; the Tseitin-on-3-regular-expander benchmark family is unchanged; the empirical pipeline (kissat-with-DRAT, drat-trim cumulative-clause accounting, the b2 sweep design) is unchanged; the literature framing against Ben-Sasson–Wigderson, Ben-Sasson–Galesi, Esteban–Torán, and ADRNV is unchanged in scope (only the specific composition in §9 is corrected); the novelty claim "$\Phi$ as a measurable per-run cumulative resource on Tseitin not previously reported in the resolution-space literature" stands; the §6 RC4-style measurement protocol stands.
- The **v3.5 surgical fixes** (Sym2 / DecidableEq hygiene, the $|M_t^{\mathrm{DP}}|$ vs `activeClauses.card` bridge lemma, the deterministic min-occ tiebreak, the DRAT proof-validity gate) are all preserved.
- The empirical $\alpha_\Phi \approx 4.43$ on Tseitin-3-regular-expander remains a measured exponent on a fixed heuristic; only its **interpretation** changes (no formal ordering to $\mathrm{CSpace}_{\mathrm{cum}}$, per corrected Lemma A).
- The push-$n$ campaign design ($n = 70, 80, 90, 100$ with $\ge 10$ seeds per cell, default + no-restart + no-inprocessing, paired-by-seed) is unchanged and is now the obligated continuation justified by §10's downgraded CI.