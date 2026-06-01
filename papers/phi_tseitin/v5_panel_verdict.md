# v5 Panel Verdict — surgical close of E1/E2/E3 (workflow w9eo2fnta)

**Date:** 2026-06-01

**Trajectory:** v1 = B_arxiv_preprint -> v2 = MAJOR -> v3 = MAJOR -> v4 = MAJOR -> **v5 = ['MINOR_REVISION', 'ACCEPT', 'unclear']**

## 3 Adversarial Lens / Phase 1 fixes
*(saved separately as v5_fix_E1_admissibility.md, v5_fix_E2_ADRNV_chain.md, v5_fix_E3_bootstrap.md)*

## 3 Judge Verdicts

### Judge 1: Senior Empirical-Math Reviewer (Exp Math)

VERDICT: MINOR_REVISION

HEADLINE: A cumulative-entropy proxy Φ for resolution refutations on Tseitin formulas, with a measured exponent α_Φ ≈ 4.43 reported as a heuristic-specific quantity with no formal ordering to cumulative space, after surgical retractions of the v4 Lemma A direction and the Ω(n^2) Corollary C2 chain.

VENUE: arXiv (cs.CC / cs.LO) as a measurement-and-formalization preprint; not yet a CCC/SAT-class venue, but suitable as a short SAT 2026 tool/empirical paper or a Pragmatics-of-SAT workshop submission once the push-n data is in.

WHAT_IMPROVED_v4_to_v5:
- Lemma A (ii) is handled honestly: the v4 directional inequality Φ_count ≥ CSpace_cum is explicitly retracted, and the surviving one-sided bound Φ_count^{DP,h}(F) ≤ CSpace_cum(π'_{DP,h}) is derived via a clean primitive-expansion (download/inference/erasure) argument that correctly identifies DP-elimination as a macro, not a primitive op. This was exactly my v4 objection and it is closed.
- Corollary C2 is correctly downgraded: the peak-vs-plateau gap in ADRNV Lemma 12 is named explicitly, Esteban–Torán is restated as a peak (clause-space) bound only, the ADRNV open problem on p.38:19 is cited, and the defensible bound is now Ω(n), not Ω(n^2). The withdrawal is unambiguous and appears in the retraction block — this fully addresses my v4 citation-chain complaint.
- The +0.323 restart effect is neither over-claimed nor over-killed: the paired-by-seed cluster bootstrap (B=2000) is the right test, the full-range CI [+0.213, +0.435] is reported alongside the leave-n=60-out CI [+0.031, +0.111], the tied-cell diagnostic (20/20 ties at n≤22) is disclosed, and the effective DoF caveat (~5 seed clusters) is stated. The downgrade language ("real but fragile, magnitude not yet established, push to n=70..100 obligated") is exactly the calibration I asked for.
- Cascading honesty: abstract-level "upper witness" language is withdrawn wherever it depended on the retracted direction, no-inprocessing is promoted to "suggestive" and no-eliminate to null — neither was hidden to protect the headline.
- The retraction block in §3.5 is now a clean, machine-checkable list of what was withdrawn vs. what survives, which is exactly the form a referee can verify.

STILL_MISSING:
- The push-n campaign (n = 70..100, ≥10 seeds, paired) is promised but not yet executed; until those data land, the α_Φ ≈ 4.43 exponent and the no-restart slope shift are both single-regime measurements. The paper should state explicitly that α_Φ is reported on n ∈ {10..60} only and that no extrapolation to asymptotics is claimed.
- With Lemma A (ii) reduced to a one-sided schedule-specific inequality, the paper needs one short paragraph (in §3 or §7) saying plainly what Φ_count is *good for* now that it is not a CSpace_cum lower-bound witness — i.e., that it is a per-run cumulative-resource measurement on a fixed heuristic, comparable across flag sets but not across heuristics, and not a complexity-theoretic lower bound. Without this, a casual reader may still infer the retracted ordering from the empirical sections.
- The Lean anchor (Conjecture003.lean lines 369–411) defines Φ(T) = Σ H(activeClauses_t) but the bridge from H(activeClauses_t) to |M_t^{DP}| is via the h≡1 specialization; the v3.5 bridge lemma should be cited inline at the first appearance of Φ_count in §3, not only in the preservation list, so the formal/empirical correspondence is auditable in one read.

RISK: The remaining risk is interpretive rather than mathematical. After the v5 retractions, the paper's headline empirical quantity Φ_count is a heuristic-specific cumulative count with no proven ordering to any standard complexity measure on the formula, and its measured exponent lives on a six-point range whose signal is concentrated at the largest cell. A hostile reader can still ask "why should I care about Φ_count?" — the honest answer is "because it is a reproducible, DRAT-checked per-run resource curve that discriminates flag regimes," which is a fine empirical-tool answer but not a complexity-theoretic one. As long as the abstract and §7 frame the contribution as measurement + Lean-anchored definition + open conjecture, the risk is low; if any residual "upper witness" or "lower bound" phrasing leaked through the v4→v5 edit, the paper would again over-claim. A careful diff pass on the abstract, §7, and §9 is the cheap insurance.

ESTIMATED_PAGES: 18

---

### Judge 2: Complexity-Theory Reviewer (SAT 2026)

# JUDGE 2 REVIEW — COMPLEXITY THEORY

**Reviewer focus:** ADRNV Lemma 12, Esteban–Torán, the composition chain, and the honesty of the Corollary C2 walk-back.

---

## 1. The headline question: did v5 honestly walk back C2?

**Yes.** This is the strongest part of v5 and the part I came in most skeptical about.

The v4 chain was:

> Tseitin clause-space $\ge n - O(1)$ (Esteban–Torán) $\;\Rightarrow\;$ via ADRNV Lemma 12 $\;\Rightarrow\;$ $\mathrm{CSpace}_{\mathrm{cum}}(\mathrm{Tseitin}_n) = \Omega(n^2)$.

If true, this would resolve in the affirmative the open problem stated explicitly by ADRNV at ITCS 2017 (p.38:19, the "extend to Tseitin" question). That alone made v4 a MAJOR_REVISION: a draft that incidentally closes an ITCS open problem in three lines of composition is, in 100% of cases I have seen, wrong.

v5 §9 (iii) identifies the slip correctly and in the right vocabulary:

> "ADRNV Lemma 12 in its tight reading requires the refutation to *spend $\Omega(s)$ steps at space $\Omega(s)$* — i.e., to sustain a plateau of width $\Omega(s)$ — not merely to *touch* space $s$ once."

This is exactly the peak-vs-plateau distinction. The combinatorial growth argument (configurations grow by at most one clause per step, so reaching size $s$ takes $\ge s$ steps with average $\ge s/2$) gives $s^2/2$ **only for the trace that actually reaches $s$ and pays the climb**. A refutation that briefly spikes to $s$ and immediately erases pays $O(s)$ cumulative, not $\Omega(s^2)$. Esteban–Torán constrains the *max over all refutations of the peak*, not the *width of any plateau realized by the min-cumulative refutation*. The two minima are over potentially different traces. That is precisely why the ADRNV question remains open for Tseitin, while it is closed for the XOR-pebbling formulas of ADRNV Thm 14–15, which are engineered to force the plateau by construction.

The v5 corrected Corollary C2 — "$\mathrm{CSpace}_{\mathrm{cum}}(\mathrm{Tseitin}_n) \ge \max\text{-space}(\pi) \ge n - O(1)$, hence $\Omega(n)$" — is the correct, defensible, trivial bound that survives. It is honest. It also explicitly cites p.38:19 lines 996–998 as the unresolved open problem, which is the right archival move.

**Verdict on C2:** clean walk-back. The retraction language in §3.5 ("**withdrawn**", "the chain from ADRNV Lemma 12 + Esteban–Torán does not deliver $n^2$") is appropriately blunt. No hedging.

---

## 2. ADRNV Lemma 12: stated correctly?

v5 §9(i) states Lemma 12 as a **per-trace** inequality, $\mathrm{CSpace}_{\mathrm{cum}}(\pi) \ge \Omega(\max\text{-space}(\pi)^2)$, and explicitly flags that this is *not* the formula-level statement. This is correct. ADRNV Lemma 12 is per-refutation. The reader who confuses the formula-level minima sees a chain; the reader who keeps the quantifiers straight sees that the chain has a hidden plateau hypothesis.

One minor calibration note: the $s^2/2$ argument as v5 paraphrases it ("at most one clause added per step → reaching size $s$ requires $\ge s$ steps → average $\ge s/2$") is the right intuition but is informal; ADRNV's actual Lemma 12 is more careful about download vs inference accounting. This is a sketch, not a proof, and v5 presents it as such — adequate for a delta document.

---

## 3. Esteban–Torán: model-match verified?

v5 §9(ii) does the model-match check that v4 lacked: "Clause-space in Esteban–Torán is the max number of clauses simultaneously in memory across the trace; this coincides with ADRNV's $\max\text{-space}(\pi)$ in the standard resolution-with-memory model. The models do match."

This is correct. Both papers work in the same resolution-with-memory model with the same primitive operations (download/inference/erasure) and the same definition of memory size as clause count. Earlier resolution-space literature occasionally used "variable space" or other measures; v5 is right to make the model-match explicit, since this is precisely where naive citations break.

---

## 4. The Lemma A retraction (E1)

The v4 Lemma A part (ii) claim was $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \ge \mathrm{CSpace}_{\mathrm{cum}}(F)$, justified in one line as "immediate from min-over-traces."

v5 §3 walks this back correctly. The argument is:

1. DP elimination is a **macro** step, not a primitive resolution-with-memory step.
2. Expanding one DP macro step into primitives (download missing clauses → all pairwise resolutions on $v$ → erase originals) inserts intermediate memory configurations.
3. Each intermediate adds to the cumulative sum.
4. Therefore the primitive expansion $\pi'_{\mathrm{DP},h}$ has **more** summands than $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F)$, giving $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \le \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h})$ — the **opposite** of what v4 claimed.

This is right. The "min over all traces" argument in v4 was confused about which side of the inequality the min lives on. The min-over-traces gives you $\mathrm{CSpace}_{\mathrm{cum}}(F) \le \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h})$, not $\mathrm{CSpace}_{\mathrm{cum}}(F) \le \Phi_{\mathrm{count}}^{\mathrm{DP},h}(F)$. Both quantities are upper-bounded by the same expansion's cumulative space; they are not ordered with respect to each other.

The honesty disclosure ("Path A does not close the gap: expansion strictly adds summands") is the correct framing. The retraction propagates correctly to §7 ("upper witness" language) and to the abstract.

**One technical caveat worth flagging.** The v5 expansion claim — "Each intermediate $|M|$ in this expansion is **at least** the smaller of $|M_t^{\mathrm{DP}}|$ and $|M_{t+1}^{\mathrm{DP}}|$ (monotone phases) and may transiently exceed both during the resolution phase before the matching erasures" — needs a closer look in the eventual full v5 manuscript. The "at least" claim during the download phase is straightforward (you only add clauses); the "may transiently exceed" during inference is also straightforward; but the *exact* bound on the intermediate sum depends on the scheduling of inferences vs erasures and on how many pairwise resolvents are formed before any erasures begin. The directional conclusion ($\mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h}) \ge \Phi_{\mathrm{count}}^{\mathrm{DP},h}(F)$) survives regardless of the exact scheduling, because every intermediate is non-negative and there are strictly more of them. So the retraction direction is safe even if the intermediate-bound sketch needs tightening.

---

## 5. What is left standing — and is it enough?

After E1 and E2, the formal structure of the paper is:

- $\Phi$ is a well-defined per-run quantity with a Lean anchor (M1–M6 preserved, good).
- $\Phi_{\mathrm{count}}^{\mathrm{DP},h}(F) \le \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h})$ — one-sided, schedule-specific.
- $\mathrm{CSpace}_{\mathrm{cum}}(\mathrm{Tseitin}_n) = \Omega(n)$ — trivial via Esteban–Torán.
- $\Phi_{\mathrm{count}}$ and $\mathrm{CSpace}_{\mathrm{cum}}$ are **not formally ordered** with respect to one another.
- Empirically $\alpha_\Phi \approx 4.43$ on Tseitin-3-regular-expander — a measured exponent on a fixed heuristic, no longer claimed as an upper or lower witness to $\mathrm{CSpace}_{\mathrm{cum}}$.

That is a much more modest paper than v4 advertised. The novelty claim is now squarely "$\Phi$ as a measurable per-run cumulative resource on Tseitin not previously reported," which is defensible as an empirical contribution but should not be oversold. The v5 explicitly says exactly this, which is the right call. The empirical $\alpha_\Phi \approx 4.43$ being *larger* than $2$ "is consistent with $\Phi_{\mathrm{count}}$ sitting above $\mathrm{CSpace}_{\mathrm{cum}}$ on this regime, but it is not a proof of the ordering" — this is the correct level of restraint.

---

## 6. E3 (mechanism slopes) — outside my remit but a sanity check

§10 is not in the complexity-theory wheelhouse, but the structural concern from my standpoint is whether the retraction discipline holds. It does: v5 reports the full-range CI honestly (excludes zero), reports the leave-$n=60$-out as 4× smaller, reports the tied-cell diagnostic showing the entire signal lives in the $n=40,50,60$ cells with concentration at $n=60$, and reports the effective sample size as $\sim 4$ clusters. The verdict "downgraded but not retracted, push-$n$ campaign obligated" is consistent with the data shown. I defer to Judge 1 on statistical specifics, but the *honesty discipline* matches the rest of v5.

---

## 7. Residual concerns

1. **The §3 re-scheduling intermediate-bound sketch** (noted in §4 above) should be tightened in the eventual full v5 manuscript. Not load-bearing for the retraction direction, but load-bearing for any future attempt to recover a one-sided bound in the *other* direction.

2. **The novelty claim "$\Phi$ as a measurable per-run cumulative resource on Tseitin not previously reported in the resolution-space literature"** is plausible but I would want to see an explicit check against Razborov's pebbling-based cumulative-space papers (2016, 2018) and the follow-up work after ADRNV. Cumulative space *as such* is in ADRNV; "per-run measured on Tseitin under a specific solver heuristic" is what v5 is claiming as new. The framing should be precise about this distinction.

3. **The abstract and §7 propagation** is mentioned in v5 ("'upper witness' language is replaced throughout"), but the full v5 manuscript needs to be checked line-by-line that no remnant of $\Phi_{\mathrm{count}} \ge \mathrm{CSpace}_{\mathrm{cum}}$ survives. The delta document promises this; the manuscript must deliver.

---

## VERDICT

**ACCEPT (with the residual concerns above as minor revisions, not blocking).**

v4's MAJOR_REVISION verdict was driven by exactly one structural problem: Corollary C2 would resolve an ITCS 2017 open problem in three lines, which is a near-certain signal of error. v5 identifies the error correctly (peak-vs-plateau in ADRNV Lemma 12), withdraws the quadratic claim, downgrades to the trivial linear bound, and cites the ADRNV open question in the right place. The Lemma A retraction is also honest and correctly identifies which direction of the inequality the min-over-traces argument actually delivers.

The paper that survives is significantly more modest than v4 advertised. That is the correct outcome. A paper claiming to close an ADRNV open problem should be either bulletproof or withdrawn; v5 chose withdrawal, which is the right move.

The complexity-theory chain is now honest. I would accept v5 on this axis.

---

### Judge 3: Honest-Negative Reviewer

# JUDGE 3 — HONEST-NEGATIVE REVIEW OF v5

## Verdict: ACCEPT

The v4 panel's central worry on §10 was that the +0.323 no-restart effect was a single-cell artifact dressed up as a slope. v5 does the paired-by-seed cluster bootstrap the panel demanded, reports the full numeric table, runs the leave-n=60-out sensitivity, and — crucially — rewrites the headline claim language to match what the data actually support. The CI question and the honesty-of-downgrade question both receive defensible answers. Below I read v5 against the three things a hostile reviewer would check.

## 1. Did the paired bootstrap give an honest CI?

Yes. The design described is the correct one for this data structure: 5 seeds form the cluster unit, the same k-resample is applied across all 9 n values (preserving the paired-by-seed structure that gives the contrast its power), B=2000 is adequate for percentile CIs at the 95% level, and the contrast is computed at the right level (slope-of-flag minus slope-of-default per resample, not difference-of-means per n). Three details give me confidence this was actually executed honestly rather than reverse-engineered to a target:

- The no-eliminate CI **[−0.005, +0.073]** crosses zero and is reported as such. A motivated-reasoning bootstrap would have found a way to nudge this to "marginal." It didn't.
- The no-inprocessing effect is **surfaced**, not hidden — v4 §10 underweighted it, v5 elevates it to "suggestive." This is the opposite of confirmation bias: the bootstrap revealed an effect the prior draft missed, and v5 reports it even though it complicates the narrative.
- The tied-cell diagnostic is brutal and self-incriminating: **20/20 ties for n ≤ 22**, only 1 tie broken at n=26,30, the entire signal living in the rightmost 3 cells and concentrating at n=60. This is exactly what a reviewer would compute to attack the paper; v5 computes it and puts it on the table.

The effective-sample-size disclosure ("~4 DoF dominated by 5 clusters, 9 log n points not independent") is the right caveat and is rare to see voluntarily disclosed. The percentile CI is the appropriate choice here (BCa would require more clusters to be stable).

One residual concern: the report does not state whether the cluster-bootstrap was the only bootstrap run, or whether other resampling schemes were tried and the cluster version selected post hoc. A one-line pre-registration note ("cluster-by-seed chosen ex ante as the only paired structure that respects the seed-as-replicate design") would close this. Not a blocker.

## 2. The CI includes zero in the right places. Was the headline honestly downgraded?

This is the crux. The full-range CI **[+0.213, +0.435]** for no-restart does exclude zero, so the panel's worst-case framing ("CI includes zero") is technically not what the data show — but v5 does not exploit this technicality. Instead it:

- Reports the leave-n=60-out CI **[+0.031, +0.111]** which still excludes zero but is **4× smaller** in magnitude, and explicitly says "the magnitude is not yet established."
- Reports the leave-n≥50-out CI **[0.000, +0.390]** which "barely touches zero at the lower bound, no longer cleanly excludes." The word "barely" is doing real epistemic work here and is the correct word.
- Rewrites the headline claim verbatim as a quoted block: **"the effect is concentrated at the largest cell (n=60); excluding n=60 the shift drops to +0.07 [+0.03, +0.11], so the magnitude is not yet established and a push to n=70..100 is required before claiming a stable mechanism slope."** This is the right sentence. It does not claim a stable slope, it commits to the obligation to extend n.
- Frames the §10 update as "downgrade in claim strength but not full retraction," with explicit reasoning for why (CI does exclude zero on full range) and explicit reasoning for why the downgrade is still required (n=60 carries the signal).

The honesty test for a downgrade is: does the rewritten language still let the casual reader walk away with the v4 impression? Here the answer is no. The quoted replacement sentence cannot be read as "+0.323 stable mechanism slope"; it can only be read as "+0.32 full-range with caveats, +0.07 without n=60, push n before claiming."

The no-inprocessing handling is also honest: it gets promoted to "suggestive" on the full range, then explicitly noted that the leave-n=60-out CI **[−0.048, +0.316]** crosses zero, with the conclusion "CI now crosses zero." No hedging.

The no-eliminate handling is the strictest honesty test, because reporting a null is unrewarded. v5 reports it cleanly as null.

## 3. Cross-checks against the rest of v5

E1 and E2 receive their own retractions in §3.5 and the abstract "upper witness" language is withdrawn — this matters for §10 because the v4 narrative tied the empirical α_Φ ≈ 4.43 to the (retracted) directional inequality. v5 explicitly says α_Φ "remains a measured exponent on a fixed heuristic; only its **interpretation** changes (no formal ordering to CSpace_cum)." This is the consistent move: the bootstrap downgrade in §10 and the theoretical retractions in §3, §9 are reported as parts of the same epistemic cleanup, not isolated patches. A dishonest v5 would have kept §10 hot while retracting §3 and §9; v5 cools all three.

The push-n campaign (n=70..100, ≥10 seeds, paired-by-seed, default + no-restart + no-inprocessing) is the correct obligated next step and is named as such rather than buried in "future work."

## Residual concerns (non-blocking)

- **Pre-registration of the bootstrap design.** A line stating the cluster-by-seed scheme was fixed before seeing the contrast results would foreclose post-hoc-selection objections.
- **No-inprocessing language drift risk.** "Suggestive" can creep toward "confirmed" in citation. The §3.5 retraction block uses "downgraded to suggestive" which is fine; ensure the body text matches.
- **Effective-DoF caveat placement.** The "~4 DoF" note is in §10 but should also surface in any abstract-level mention of the mechanism CIs, so the headline cannot be quoted without it.
- **Bootstrap script provenance.** Output at `/tmp/e3_bootstrap.txt` and script at `/tmp/e3_bootstrap.py` on the SEC server, plus `/tmp/e3_bootstrap_local.py` locally — these should be committed to the paper repo with a hash, not left in `/tmp`, before submission. `/tmp` is ephemeral on the SEC server and the artifact will be unrecoverable after reboot.

## Bottom line

v5 §10 passes the honest-negative test. The paired bootstrap was actually run with the right paired structure, the CI table is reported in full including the null and the leave-one-out, the tied-cell diagnostic is self-incriminating in the correct direction, the headline claim is rewritten in language that cannot be casually misread, and the downgrade is consistent with the parallel §3 and §9 retractions. The push-n campaign obligation is named explicitly. **ACCEPT** with the residual concerns above, none of which are blockers.

---

