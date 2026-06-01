Here is the replacement text for v4 Section 3 Lemma A (ii):

---

**Lemma A (part ii — formula-level relation, schedule-bookkeeping inequality).**
We replace the v4 draft's "immediate from min-over-traces" wording, which conflated coarse-grained DP elimination steps with primitive resolution-with-memory steps in the sense of ADRNV Definition 11.

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
no longer goes through unconditionally. The second inequality survives (Esteban–Torán + ADRNV Lemma 12, on bounded-degree expander Tseitin). The first does **not** follow from Lemma A as corrected here. C2 should therefore be downgraded: $\mathrm{CSpace}_{\mathrm{cum}}(F_n) = \Omega(n^2)$ stands as a literature-derived lower bound; $\Phi_{\mathrm{count}}^{\mathrm{DP},\mathrm{min\text{-}occ}}(F_n)$ remains a measured exponent on a fixed heuristic with **no formal ordering** to $\mathrm{CSpace}_{\mathrm{cum}}(F_n)$. The empirical $\alpha_{\Phi} \approx 4.43$ being **larger** than $2$ is consistent with $\Phi_{\mathrm{count}}$ sitting above $\mathrm{CSpace}_{\mathrm{cum}}$, but it is not a proof of the ordering.

---

**Honesty disclosure.** I attempted Path A and it does not close the gap. A DP-min-occ trace, when expanded into a primitive admissible res-with-memory trace, gains extra summands (the download and resolution intermediates between elimination checkpoints), so the expansion's cumulative space is $\ge \Phi_{\mathrm{count}}$, not $=$. Equality of the sum, not just of the checkpoint $M_t$'s, is what Path A needed, and it fails. What I delivered above is Path B with an explicit re-scheduling construction supplying the (now downgraded) one-sided bound $\Phi_{\mathrm{count}}(\mathrm{DP},h)(F) \le \mathrm{CSpace}_{\mathrm{cum}}(\pi'_{\mathrm{DP},h})$. The v4 directional claim $\Phi_{\mathrm{count}} \ge \mathrm{CSpace}_{\mathrm{cum}}$ is **retracted** and Corollary C2 must be weakened accordingly. The "upper witness" language in the v4 abstract and §7 — which depends on the retracted direction — should be replaced with "schedule-specific measurement with no formal ordering to $\mathrm{CSpace}_{\mathrm{cum}}$" in any v5 revision.

Relevant paths:
- /home/ludo/Scrivania/SEC_research/staging/papers/v4_phi_tseitin_draft.md (lines 99–104 to replace; downstream: line 134 C2, line 423 Proposition, line 476 limitations item 1, abstract line 11 "upper witness" language)