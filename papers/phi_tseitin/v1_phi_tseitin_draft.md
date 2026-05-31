# Cumulative Clause-Space on Tseitin Formulas under Davis–Putnam Refutation: An Empirical Localisation Inside a Known Open Interval

**Ludovico Kubler**
*Draft, 2026-05-30*

---

## Abstract

We study the cumulative clause-database size $\Phi$ accumulated by Davis–Putnam (DP) variable elimination on random $3$-regular Tseitin formulas. Across $200$ seed-locked runs in the range $n \in \{6,8,10,12,14\}$ and a separate $1287$-run baseline up to $n=30$, $\Phi$ exhibits a power-law in $n$ whose fitted log–log slope lies in the interval $[2.4, 3.0]$ within the computable window, with no evidence of asymptotic stabilisation. The slope is *not* invariant under elimination order (range $[2.25, 3.95]$ across five heuristics, disjoint bootstrap 95% CIs), nor across proof systems (DRAT slope $5.89$ vs DP slope $3.43$ at $n=30$). The exponent we measure lies strictly between the proved $\Omega(n^2)$ cumulative-clause-space lower bound of Alwen–de Rezende–Nordström–Vinyals (ITCS 2017) and the $2^{O(n)}$ Ben-Sasson–Wigderson (JACM 2001) upper bound — a region the lower-bound authors explicitly flag as open for Tseitin. We make no asymptotic claim. The contribution is an honest, heuristic- and prover-conditional empirical localisation.

---

## 1. Definitions

We anchor all definitions on the formal statement in `Conjecture003.lean` (project `pvnp`, module `CumulativeEntropy`).

**Definition 1 (proof-state entropy).** Let $\pi = (M_0, M_1, \dots, M_T)$ be a sequence of clause databases ("memory configurations") produced by a proof procedure, where $M_t \subseteq \mathcal{C}$ is the active clause set at step $t$. The *proof-state entropy* at step $t$ is
$$
H(M_t) \;:=\; |M_t|
$$
in the unit-weight ($\Phi_{\mathrm{count}}$) variant, and
$$
H_w(M_t) \;:=\; \sum_{C \in M_t} w(C),\quad w(C) = |C|
$$
in the literal-weighted ($\Phi_{\mathrm{weight}}$) variant.

**Definition 2 (cumulative entropy).** Following Alwen–de Rezende–Nordström–Vinyals (ITCS 2017, p. 38:3, footnote 1), define
$$
\Phi(\pi) \;:=\; \sum_{t=0}^{T} H(M_t).
$$
This coincides with the *cumulative clause-space* measure $\mathrm{CSpace}(\pi)$ of that paper. The Lean definition `cumulativeEntropy` in `Conjecture003.lean` is the literal transcription of this sum over a `List (Finset Clause)` trace.

**Definition 3 (the harness).** A *harness* is a triple $(\Pi, \mathcal{F}, h)$ where $\Pi$ is a proof procedure (here: Davis–Putnam variable elimination, or kissat producing a DRAT certificate), $\mathcal{F}$ is a formula family (here: Tseitin formulas $T(G, \chi)$ on a graph $G$ with an odd charge vector $\chi$), and $h$ is the auxiliary policy needed to make $\Pi$ deterministic (here: the elimination order for DP, or the kissat configuration for DRAT). We write $\Phi^{\Pi,h}(F)$ for the cumulative entropy of the trace $\Pi$ produces on $F$ under policy $h$.

The *empirical exponent* $\alpha(\mathcal{F}, \Pi, h)$ is the log–log slope of
$$
n \;\longmapsto\; \mathbb{E}_{F \sim \mathcal{F}_n}\bigl[ \Phi^{\Pi,h}(F) \bigr]
$$
over a finite $n$-window, fitted by ordinary least squares on $(\log n, \log \Phi)$ pairs.

We stress: $\alpha$ is a property of the triple $(\mathcal{F}, \Pi, h)$, not of $\mathcal{F}$ alone. Sections 4–5 give the experimental evidence for this caveat.

---

## 2. Empirical Setup

**Proof procedure.** Davis–Putnam variable elimination (resolution on a pivot variable until the variable is gone), repeated until $\bot$ or a fixed point is reached. We additionally compare against kissat (CDCL with DRAT proof logging).

**Elimination orders ($h$).** Five deterministic orders: `min_degree`, `min_occurrence` (baseline), `random` (seeded), `max_occurrence`, `reverse_min_occurrence`.

**Graph families ($\mathcal{F}$).** Six families, all with an odd-charge Tseitin encoding:

| family | degree | expansion proxy |
|---|---|---|
| `path` | $\leq 2$ | low |
| `rand_3_regular` | $3$ | medium |
| `rand_4_regular` | $4$ | medium–high |
| `expander_proxy` | $\sim 4$, rejection-sampled for spectral gap | high (finite-$n$ surrogate) |
| `star` | $n-1$ at hub | (artefact: $2^{\deg-1}$ clauses) |
| `grid_2d` | $\leq 4$ | low |

**$n$ range.** Order-comparison experiment: $n \in \{6, 8, 10, 12, 14\}$. Family experiment: $n \in \{6, \dots, 12\}$. Baseline `rand_3_regular` $\Phi_{\mathrm{count}}$ vs $\Phi_{\mathrm{weight}}$: $n \in \{6, \dots, 18\}$. Prover-comparison (DP vs DRAT/kissat): $n \in \{10, \dots, 30\}$.

**Seed scheme.** `master_seed = 20260530`. For each $(\Pi, h, \mathcal{F}, n)$ cell the graph seeds and (where applicable) the random elimination seeds are derived deterministically from `master_seed` via a fixed hash, so every cell is reproducible and the *same* underlying graphs are reused across orders within the order-comparison experiment.

**Instances per cell.** $8$ (order comparison, $200$ runs total), $3$ (family experiment), $20$ (count-vs-weight baseline), $\geq 10$ (prover comparison).

**Bootstrap.** $1000$ resamples over instances, percentile 95% CIs. Slope CIs are computed by refitting OLS on each resample.

**Termination.** $0/200$ blow-ups in the order experiment; all runs completed within the configured clause-DB cap.

---

## 3. Results

### 3.1 Slope as a function of elimination order

Tseitin on `rand_3_regular`, $n \in \{6, 8, 10, 12, 14\}$, $8$ seed-locked instances per cell.

| order | mean $\Phi_{\mathrm{count}}$ at $n{=}14$ | slope $\hat\alpha$ | bootstrap 95% CI |
|---|---:|---:|---|
| `min_degree` | $952$ | $2.25$ | $[2.10, 2.41]$ |
| `min_occurrence` (baseline) | $1{,}515$ | $2.42$ | $[2.27, 2.58]$ |
| `random` | $1{,}835$ | $2.61$ | $[2.43, 2.79]$ |
| `max_occurrence` | $3{,}345$ | $3.18$ | $[2.99, 3.37]$ |
| `reverse_min_occurrence` | $4{,}891$ | $3.95$ | $[3.71, 4.18]$ |

The mean-$\Phi$ spread at $n=14$ is $5.1\times$. All five CIs are pairwise disjoint. This **refutes order-invariance**: $\alpha$ depends materially on $h$.

### 3.2 Slope as a function of graph family

Same $\Pi$, fixed heuristic (`min_occurrence`), $3$ trials per $n$, $n \in \{6, \dots, 12\}$.

| family | mean $\Phi_{\mathrm{count}}$ at $n{=}12$ | slope $\hat\alpha$ |
|---|---:|---:|
| `path` | $133$ | $2.09$ |
| `rand_3_regular` | $762$ | $2.29$ |
| `star` | $2{,}114$ | $5.44$ (encoding artefact: $2^{\deg-1}$ clauses) |
| `rand_4_regular` | $7{,}199$ | $4.06$ |
| `expander_proxy` | $11{,}511$ | $3.96$ |
| `grid_2d` | — | unreliable ($\sqrt{n}$ rounding) |

Excluding `star` and `grid_2d`, slope clusters by expansion: low-expansion families (`path`, `rand_3_regular`) at $\approx 2.0$–$2.3$, high-expansion (`rand_4_regular`, `expander_proxy`) at $\approx 4.0$. The ratio is $\approx 1.9\times$. The `rand_3_regular` slope $2.29$ agrees with the $1287$-run baseline mean $2.42$ within $\approx 0.6\sigma$.

### 3.3 $\Phi_{\mathrm{count}}$ vs $\Phi_{\mathrm{weight}}$

Same $\Pi$, `rand_3_regular`, $n \in \{6, \dots, 18\}$, $20$ instances per cell.

| metric | point slope | bootstrap 95% CI |
|---|---:|---|
| $\Phi_{\mathrm{count}}$ | $2.557$ | — |
| $\Phi_{\mathrm{weight}}$ | $2.972$ | — |
| gap $\alpha_w - \alpha_c$ | $0.415$ | $[0.367, 0.464]$ |

The gap CI excludes $0$: $\Phi_{\mathrm{weight}}$ grows *strictly* faster than $\Phi_{\mathrm{count}}$ in this window.

### 3.4 Slope across proof systems

Same `rand_3_regular`, $n \in \{10, \dots, 30\}$.

| prover | slope $\hat\alpha$ | bootstrap 95% CI | $\Phi$ ratio (DRAT/DP) |
|---|---:|---|---:|
| DP (`min_occurrence`) | $3.43$ | $[3.19, 3.68]$ | — |
| kissat / DRAT | $5.89$ | $[5.51, 6.29]$ | $6.8$ at $n{=}10$, $84.3$ at $n{=}30$ |

Paired bootstrap on the slope difference $\alpha_{\mathrm{DRAT}} - \alpha_{\mathrm{DP}}$ excludes $0$. **$\Phi$ is prover-conditional.**

### 3.5 Headline number and its honest reading

The DP-baseline slope on `rand_3_regular` under `min_occurrence` is:

- $n \leq 16$ window: $\hat\alpha \approx 2.42$.
- $n \leq 28{-}30$ window: $\hat\alpha \approx 2.93$ with 95% CI $[2.80, 3.07]$.

The previously reported single number "$\Phi \sim n^{2.4}$" is therefore a **finite-$n$ artefact** of a small window. The honest statement is: $\hat\alpha \in [2.4, 3.0]$ in the computable window, with measurable upward drift and no observed stabilisation.

---

## 4. Theoretical Position

The relevant published bounds on Tseitin under resolution are:

**Upper bound.** Ben-Sasson–Wigderson, *Short proofs are narrow — resolution made simple* (JACM 48(2):149–169, 2001, Thm 3.5): width $\Omega(n)$ implies length $2^{\Omega(n)}$ for Tseitin on constant-expander $3$-regular graphs; the only universal upper bound on length, and hence on $\Phi$, is $2^{O(n)}$.

**Lower bound on cumulative clause-space.** Alwen–de Rezende–Nordström–Vinyals, *Cumulative Space in Black-White Pebbling and Resolution* (LIPIcs ITCS 2017, vol. 67, paper 38):
- p.38:3, footnote 1: the cumulative-clause-space measure used here coincides with our $\Phi$.
- Lemma 12 (p.38:13): if $F$ requires maximal clause-space $s$, then cumulative clause-space is $\Omega(s^2)$.
- Combined with Esteban–Torán (*Lower Bounds for Space in Resolution*, CSL 1999, LNCS 1683), which proves clause-space $n - O(1)$ for Tseitin on bounded-degree expanders, this yields a lower bound of $\Omega(n^2)$ on cumulative clause-space for Tseitin on bounded-degree expanders.
- Theorems 14–15 give $\Omega(N^2)$ and $\Omega(N^2 / \log N)$ cumulative-space lower bounds, but only for *XOR-ified pebbling* formulas, **not** for Tseitin.
- Lines 996–998 (p.38:19): the authors explicitly flag as an open problem the extension of cumulative-space lower bounds "beyond pebbling formulas … to, e.g., Tseitin formulas".

**Width lower bound.** Urquhart (*Hard examples for resolution*, JACM 34(1):209–219, 1987) and Ben-Sasson–Wigderson (2001) give width $\Omega(n)$ on bounded-degree expander Tseitin. Width and cumulative size scale independently, so our results neither contradict nor strengthen this bound.

**Localisation.** Our measured DP slope (between $2.4$ and $3.0$ in the computable window, conditional on `min_occurrence`) lies strictly above the $\Omega(n^2)$ lower bound and strictly below $2^{O(n)}$. The interval is an *open region* in the literature — and it is open precisely because the lower-bound authors say so. We therefore claim:

- We do **not** contradict any published bound.
- We do **not** prove a new bound.
- We provide the first systematic empirical localisation of $\Phi$ for Tseitin under a named DP heuristic inside this open interval.

---

## 5. Limitations

1. **No asymptotics.** The largest $n$ we can compute is $30$. The $\hat\alpha$ drift from $\approx 2.42$ at $n \leq 16$ to $\approx 2.93$ at $n \leq 30$ is real and may continue. No claim about $n \to \infty$ is justified.
2. **Heuristic-conditional.** Section 3.1 shows $\hat\alpha$ ranges over $[2.25, 3.95]$ as $h$ varies, with disjoint CIs. Any future numeric claim must name $h$.
3. **Prover-conditional.** Section 3.4 shows DP and DRAT/kissat give materially different slopes ($3.43$ vs $5.89$) and a $\Phi$-ratio that grows from $6.8$ to $84.3$ over $n \in [10, 30]$. $\Phi$ is *not* a derivation invariant; DP-$\Phi$ and DRAT-$\Phi$ are distinct quantities and must be reported as such. This is an honest correction to the earlier `c003b` framing.
4. **$\Phi_{\mathrm{weight}} > \Phi_{\mathrm{count}}$ gap is finite-$n$.** Solid in $n \in [6, 18]$ with bootstrap CI $[0.367, 0.464]$, but Urquhart / BSW width bounds do not license an asymptotic claim about the gap.
5. **Expander-proxy is a surrogate.** Rejection-sampled at finite $n$; no certified spectral gap.
6. **Graph family scope.** Only random $3$- and $4$-regular Tseitin in the main results. Structured Tseitin (grid, hypercube, explicit Ramanujan) is untested. The `star` and `grid_2d` rows in Section 3.2 are diagnostics, not results.
7. **No formal verification.** The Lean definition `cumulativeEntropy` in `Conjecture003.lean` matches the empirical $\Phi_{\mathrm{count}}$ definitionally, but no theorem about its asymptotics is currently proved sorry-free.

---

## 6. Open Question

The single concrete claim that would convert this empirical localisation into a contribution to proof complexity is the following:

> **Open question.** Let $G_n$ be a random $3$-regular graph on $n$ vertices and $\chi_n$ an odd charge vector, and let $T(G_n, \chi_n)$ be the corresponding Tseitin CNF. Prove a lower bound of the form
> $$
> \min_{\pi \text{ DP-refutation of } T(G_n, \chi_n)} \; \Phi(\pi) \;=\; \omega(n^2)
> $$
> or, complementarily, an upper bound
> $$
> \min_{\pi} \; \Phi(\pi) \;=\; n^{O(1)}
> $$
> for some explicit DP elimination order. Either direction would resolve, for Tseitin, the open problem flagged on p.38:19 of Alwen–de Rezende–Nordström–Vinyals (ITCS 2017).

Our empirical interval $[2.4, 3.0]$ is, at present, the strongest evidence we have about which of these two outcomes is more likely — and that evidence is heuristic-conditional, prover-conditional, and finite-$n$. We do not stake a guess.

---

*Attribution: Ludovico Kubler. All measurements reproducible from `master_seed = 20260530` with the harness referenced in Section 2; the formal `cumulativeEntropy` definition is the one in `Conjecture003.lean` and is the anchor for all numerical $\Phi$ values reported here.*
