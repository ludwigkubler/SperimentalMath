# Negative observations from autonomous P vs NP exploration — v0.1
**Author:** Ludovico Kubler (with the SEC autonomous research engine as instrument).
**Period covered:** 2026-04-09 → 2026-05-21 (1772 cycles).
**Status:** v0.1 living document. Supersedes `compendium_v01.tex` and `compendium_v02.tex` (both retracted; see `RETRACTIONS_2026-05.md`).

---

## What this document is

A record of what an autonomous LLM-driven research engine *did not produce*, in the field of complexity theory, across 1772 cycles between 2026-04-09 and 2026-05-21. It also records:
- **one** empirical measurement worth preserving (§3),
- **five** recurring failure modes that the engine traversed before each retraction (§4),
- the **pipeline corrections in progress** (§5).

This is not a complexity-theory result. It is a methodology report: the kind of negative observation that, in slow fields, can be more informative than premature positives.

## What this document is not

- **Not a compendium of refutations.** The 16 entries the engine labelled FALSIFIED do not constitute refutations of substantive conjectures. They are pipeline events, of which 9 fail an independent code-level audit. The other 7 refute conjectures that no working mathematician has proposed.
- **Not a claim about P vs NP.** No fragment of P vs NP is settled here, in either direction.
- **Not a stable publication.** Version v0.1 is a snapshot for transparency; substantive revisions are expected as the pipeline is corrected.

---

## §1 — Inventory

The notebook contains, as of 2026-05-21:

| Verdict | April | May | Total | Surviving the 2026-05-08 audit | Citable by author |
|---|---|---|---|---|---|
| SUPPORTED | 4 | 0 | 4 | 0 | 0 |
| FALSIFIED | 15 | 1 | 16 | 9 | 0 |
| BARRIER_HIT | 7 | 327 | 334 | n/a (pre-filter, not result) | n/a |
| SCOOPED | 0 | 34 | 34 | n/a (literature pointer) | n/a |
| INCONCLUSIVE | 231 | 1153 | 1384 | — | — |
| **Total cycles** | **257** | **1515** | **1772** | | |

All 4 SUPPORTED entries from April are retracted in `retractions.json` (stub tests, hard-coded constants, malformed metrics). 5 of the 15 April FALSIFIED entries are retracted on the same grounds. The remaining 9 FALSIFIED, plus the 1 May FALSIFIED, do not survive an independent mathematical re-read (see §4).

## §2 — Why this is being published, not buried

The pipeline that produced these 1772 cycles is documented in `MULTIAGENT_PIPELINE.md` (intended architecture) and `AUDIT_2026-05-08.md` (initial self-audit). The 2026-05-23 independent review (`REVIEW_2026-05-23.md`) and the intervention plan (`INTERVENTION_PLAN_2026-05-23.md`) together establish that:

1. The engine's verdict pipeline can confuse a Python traceback with a refutation.
2. The engine's autoformaliser was prompted to *replace* conjecture primitives with arithmetic surrogates, so the Lean files cited in the prior compendia formalised the wrong objects.
3. The engine's planner produces ~1700 distinct (field A × field B) pairs and never follows a direction long enough for a result to ripen.

These are correctable. The corrections are in flight (§5). Publishing the failures honestly while the corrections land is the only way the next compendium will be credible.

## §3 — One measurement worth preserving

Across the 1772 cycles there is **one** empirical observation that, if reformulated honestly, is a starting point for further work:

**Observation (Tropical discrepancy at finite β).** For tropical polynomials $f$ on $\mathbb{Z}_n$ with min-plus semiring and Maslov-dequantized Tropical Fourier Transform at finite $\beta$, let
$$
\Delta(f, \beta, n) := \big| \mathrm{MFC}(f \star f) - 2 \cdot \mathrm{MFC}(f) \big|
$$
where $\star$ denotes tropical self-convolution and $\mathrm{MFC}$ is the minimum-modulus Fourier coefficient.

The engine's experiment ([entry `e14f176e4ef1`](notebook/2026-04.jsonl)) measured, at $n=8$, $\beta=5$, across 5 seeds × 180 instances per seed:
$$
\mathbb{E}_f[\Delta(f, 5, 8)] \approx 3.78 \;\;\text{with the naïve} \;O(1/n)\;\text{prediction giving} \;0.625.
$$
The factor-6 gap is robust across seeds.

**This is not a refutation** of a known prediction — no published source predicts the $O(1/n)$ bound. It is a measurement: the actual rate appears to be $O(1)$ in $n$ at fixed $\beta = 5$, not $O(1/n)$. The right question is: *what is the actual scaling of $\Delta(f, \beta, n)$ as a function of $(\beta, n)$?* This is the target of the next 50-cycle programme epoch (see §5).

Lean source for the primitives (faithful to the names — `tropicalConvolution`, `maslovTFTMagnitude`, `minFC`): [`lean_verified/e14f176e4ef1/Eaudit.lean`](lean_verified/e14f176e4ef1/Eaudit.lean). The proof is over `Float` (IEEE-754), not ℝ; this is documented in the file's header.

## §4 — Five recurring failure modes

Independent review of the 16 FALSIFIED entries surfaced five patterns that the multiagent pipeline did not catch. Each is now blocked by an explicit safety rail (see §5).

**M1. Two-integer-invariants-are-equal.** Conjectures of the shape "for every $\varphi$, $A(\varphi) = B(\varphi)$" where $A$ and $B$ are integer-valued. Two distinct integer-valued invariants on random small instances are essentially never equal; refuting such a conjecture is a tautology of the planner, not a discovery. *Examples:* `fe46162e441f` ($\chi_{\text{dir}} = B(\varphi)$), `84f371b65a13` ($D(f) = d(\varphi)$), `025337d8bbcc` ($\mathrm{SOS}_{\text{rounds}} = \mathrm{rank}_{\text{sym}}(A)$).

**M2. Counterexamples at $n \le 5$ for asymptotic claims.** Resolution width, decision-tree depth, and similar invariants have trivial closed-form bounds at small $n$; counterexamples in this regime are degenerate. *Example:* `a8b5663ca867` (refuted at $n=5, m=1$, a satisfiable formula).

**M3. Test crashes labelled as refutations.** A Python traceback (`KeyError`, `IndexError`, etc.) in the test output was sometimes parsed as a counterexample because the verdict logic pattern-matched stdout rather than checking exit codes. *Example:* `98ce17e2db79` (`KeyError: 'seed'` in the aggregation step).

**M4. Placeholder counterexamples.** When the test could not compute the required object, the implementation defaulted to `counterexample = "mapping_undefined"`, which the verdict logic treated as a discovered counterexample. *Example:* `8f4860266324`.

**M5. System-defined primitives.** Conjectures that named objects (`induced_kolmogorov_flow`, `phase_cells`, the engine's homebrew `TropicalFourierTransform`) whose only definition was in the test code itself. Refutations of these are not external falsifiability events; they are observations about the test code. *Examples:* `56044fada967`, `32a1e966ed26`, `44f82c29ed79`, `cca077d3c64c`.

A sixth pattern, present in `b0a4fb5d3039`, is specific enough to merit its own line:

**M6. Code-builds-the-wrong-object.** The test claims to instantiate the k-CLIQUE minterm DNF $F^*_v$, but `generate_clique_dnf(v, k)` produces the out-star graph at each vertex. The conjecture refers to one object; the test refutes a property of a different object. Caught by independent reading; not caught by the engine.

## §5 — Pipeline corrections (in flight)

A separate document, [`INTERVENTION_PLAN_2026-05-23.md`](../INTERVENTION_PLAN_2026-05-23.md), specifies eight fixes at the file-and-line level. Highlights:

- **Verdict parser** now refuses to label a non-zero exit code, a Python traceback, or a placeholder counterexample as FALSIFIED.
- **Asymptotic gate** rejects counterexamples below $n \ge 16$ unless the conjecture explicitly targets the small-$n$ regime.
- **Critic gate** receives the test source and is required to emit a *statement-vs-test divergence* paragraph; entries where the critic cannot locate a faithful Python implementation of a named primitive are demoted.
- **Lean autoformaliser** is prompted to reference, by name, every primitive in the conjecture statement; the surrogate-arithmetic style that produced the prior compendium's misleading excerpts is forbidden, with a name-grep post-check enforcing it.
- **Compendium generator** reads from `pvsnp_verified/<eid>/Eaudit.lean` (the name-grep-clean gold tier), not from `lean_counterexamples/<eid>.lean` (the auto-surrogates).
- **Planner lock**: the engine is now constrained to *one* research programme for 50 consecutive cycles. The first programme, active from 2026-05-23, is the tropical-discrepancy-at-finite-β programme (§3). Sub-conjectures and metrics are tracked in `programmes_registry.json` and `programme_metrics.json`.
- **SCOOPED** is restricted to direct matches with literature; "topically adjacent" hits are demoted to `ADJACENT_OK`.
- **Skeptic gate** extended to fire also on FALSIFIED+CONFIRM (not only SUPPORTED), so that `b0a4fb5d3039`-style code-builds-wrong-object cases are caught by the adversarial layer.

The fixes are staged outside the public repository at `staging/`; a deploy script applies them in a strict order with a selftest matrix at every phase. The deploy does not auto-restart the running engine; the operator restarts it manually.

## §6 — What we are not claiming

To be plain:
- We are not claiming the engine produces publishable mathematics. We are claiming it is now structurally able to attempt to.
- We are not claiming that 1772 cycles are "waste." A pipeline cannot be corrected without first observing where it breaks. The corrections in §5 are derived directly from the 1772 cycles' failure modes.
- We are not claiming that fixing the pipeline guarantees a result. Mathematics is slow; an LLM-driven pipeline can fail by exhausting all reachable directions within its prompt budget without producing anything. The 50-cycle epoch is a structural commitment to *depth* — the cost is forgoing breadth, and that may also turn out to be the wrong bet.

## §7 — Open questions worth a referee's time

These are not conjectures the engine has supported. They are *honest open questions* derived from the work, suitable for a human collaborator:

1. **Tropical discrepancy.** What is the asymptotic rate of $\Delta(f, \beta, n)$ for $\beta \in [5, 200]$ and $n \in [8, 64]$, on random tropical polynomials with i.i.d. Gaussian coefficients? Does the rate match a closed form derivable from the Litvinov–Maslov dequantization framework?

2. **Forman–Ricci on real $F^*_v$.** With the corrected `generate_clique_dnf` producing the $\binom{v}{k}$ minterms of $k$-CLIQUE on $K_v$, does $\mu(F^*_v) \ge v/4$ hold for $v \in \{10, 16, 20\}$ at $k = \lceil \log_2 v\rceil$? (b0a4fb5d3039's "refutation" was about a different object.)

3. **CG–KW.** Can the `opaque κ` in the framework's Lean file be replaced with a computable $\kappa$ over a small explicit model space, enabling actual tests of A1–A5 on Andreev's function?

## §8 — Author note

This file is signed by L. Kubler. The engine is the instrument; the responsibility for what is recorded here, and for what is not yet recorded, is mine.

— L. K., 2026-05-23.
