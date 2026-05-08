# SperimentalMath — Multi-Agent Review Pipeline

**Author**: Ludovico Kubler.
**Effective**: 2026-05-08.
**Purpose**: replace the lenient single-critic stage with a five-agent review system. No conjecture is promoted to `SUPPORTED`, no entry enters `lean_verified/`, and no paper draft leaves the repository unless every gate below is passed.

---

## 1. Design principles

- **The mathematician owns the verdict, not the LLM.** The multi-agent system produces a *recommendation*; the human (L. K.) signs off on every promotion.
- **Each agent is single-purpose.** Generic "smart" agents drift. Each of the five below has one job, one tool set, one output schema.
- **Code is read, not just output.** Every gate that touches a test harness must parse the source, not only its stdout.
- **Royal-Society-grade.** A submission to *Proceedings of the Royal Society A*, *SIAM J. Comput.*, *Theory of Computing*, or *Annals of Math.* is the implicit standard. If a result would not survive the referee process at one of those venues, it does not pass the gate.

---

## 2. Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR                             │
│   (queue management; gate sequencing; rejection bookkeeping)     │
└────────┬───────────┬───────────┬───────────┬───────────┬─────────┘
         │           │           │           │           │
         ▼           ▼           ▼           ▼           ▼
   ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐
   │ AUDITOR │ │MATHEMATI-│ │LITERATU-│ │  LEAN-   │ │  ROYAL-  │
   │         │ │   CIAN   │ │RE SCOUT │ │FORMALIZER│ │ SOCIETY  │
   │ Gate 1  │ │  Gate 2  │ │ Gate 3  │ │  Gate 4  │ │  Gate 5  │
   └─────────┘ └──────────┘ └─────────┘ └──────────┘ └──────────┘
```

A candidate enters at the left. It must pass each gate in order. Any failure returns the candidate to the proposer with a structured reason; it does not silently disappear — failures are logged in `audit/rejection_log.jsonl`.

---

## 3. Agents — specifications

### 3.1 AUDITOR (Gate 1)

**Single sentence**: re-runs the empirical test in an isolated sandbox and detects pipeline pathologies before any mathematical content is considered.

**Inputs**:
- `entry_id` and the JSONL row for the candidate
- the test harness Python source

**Tools**: `Bash` (sandboxed Python execution), `Read`, regex pattern matching.

**Required checks**:

| Check | Rule |
|---|---|
| Placeholder leakage | Output must not contain unresolved templates such as `<metric>=<value>`, `<counterexample>`, `???`. |
| Hard-coded constants | Every function in the test must consume a non-trivial subset of its arguments. A function whose return value is independent of `clauses`, `f`, or any sampled object is flagged. Use AST inspection. |
| Skipped enumeration | Output containing `skipping`, `Too many ... configurations`, `falling back to dummy` triggers automatic rejection. |
| Sample size | n_max must be ≥ 50 for asymptotic claims (≥ 8 for finite-domain claims), `--seeds` must include at least 5 distinct values, and the per-seed instance count must be ≥ 200. |
| Determinism | Re-running with the same seeds must yield bit-identical output. Hash both the source and the stdout; commit both. |
| Wall-clock plausibility | A test that completes in < 0.05 s while claiming to evaluate ≥ 200 instances at n ≥ 8 is flagged for stub suspicion. |

**Output schema** (JSON):
```json
{
  "entry_id": "string",
  "audit_passed": false,
  "red_flags": ["placeholder_leakage", "skipped_enumeration", ...],
  "stdout_hash": "sha256:...",
  "source_hash": "sha256:...",
  "reproduction_log": "..."
}
```

**Rejection action**: candidate returned with red_flags list; proposer must regenerate the test, not the conjecture.

---

### 3.2 MATHEMATICIAN (Gate 2)

**Single sentence**: verifies that the formal statement and the empirical test measure the same object.

**Inputs**: passed Auditor report; the natural-language statement; the test harness.

**Tools**: `Read`, symbolic reasoning, optional invocation of a CAS (SymPy, GAP, Macaulay2 via subprocess for small examples).

**Required checks**:

1. **Type-checking the statement.** Every symbol has a stated domain. *"⟨c, x⟩²"* must specify whether the inner product is over ℝ, ℤ, or 𝔽₂ before squaring, and whether the squaring is in the same ring or in a different one.
2. **Statement-test correspondence.** The metric measured by the test must be the metric defined in the statement, with no silent re-interpretation. If the test deviates (as in §2.1 of `AUDIT_2026-05-08.md`), the candidate is rejected.
3. **Trivialisation check.** Identify cases where the conjectured bound is tautological on the sampled regime (e.g., `|width - rank| ≤ 3` is trivial for n ≤ 6 since both quantities are bounded by 6).
4. **Counterexample sanity.** For falsifying entries, the counterexample must be in the *intended* regime (e.g., a SAT-instance counterexample with `m=1` and a satisfiable formula does not falsify a claim about *resolution proofs*).

**Output schema**:
```json
{
  "entry_id": "string",
  "math_passed": true,
  "issues": [],
  "formal_statement_latex": "...",
  "domain_assignments": {"x": "F2^n", "c": "F2^n", ...},
  "trivialisation_regime": null
}
```

---

### 3.3 LITERATURE SCOUT (Gate 3)

**Single sentence**: confirms that the conjecture is genuinely new at *the level of the standard literature*, not at the level of an LLM's training-time recollection.

**Inputs**: formal statement from Gate 2.

**Tools**: `WebFetch`, `WebSearch`, arXiv API, Google Scholar, dblp.

**Required searches**:

- ≥ 50 arXiv hits ranked by cosine similarity to the formal statement (use SciNCL or SPECTER embeddings).
- ≥ 20 Google Scholar hits.
- ≥ 5 standard textbook references in the relevant field, manually curated (e.g., for tropical geometry: Maclagan-Sturmfels, Mikhalkin, Itenberg-Mikhalkin-Shustin; for Frobenius-Schur indicators: Serre, Curtis-Reiner, Isaacs).

A `0 hits` outcome is **always a pipeline error**, never a novelty signal — re-formulate the query.

**Required output**:

```json
{
  "entry_id": "string",
  "novelty_passed": true,
  "arxiv_hits": [{"id": "2201.00728", "title": "...", "similarity": 0.42}, ...],
  "scholar_hits": [...],
  "textbook_refs": [{"author": "Serre", "title": "Linear Representations of Finite Groups", "ch": 2}, ...],
  "near_misses": [...],
  "novelty_argument": "string (≥ 200 words explaining why none of the above subsume the conjecture)"
}
```

`novelty_argument` is the document the eventual paper will quote in its *Related Work* section. If the scout cannot write a defensible 200-word novelty argument, the conjecture is rejected.

---

### 3.4 LEAN-FORMALIZER (Gate 4)

**Single sentence**: produces a Lean 4 file that compiles and either (a) defines the relevant primitives plus a `theorem` for the falsifying counterexample, or (b) at minimum defines the primitives and states the conjecture as a `def` whose well-formedness type-checks.

**Inputs**: formal statement (Gate 2), counterexample data (Auditor reproduction log).

**Tools**: Lean 4 toolchain, `lake`, `Bash`.

**Required deliverables per candidate**:

- a self-contained Lean project under `lean_verified/<entry_id>/` that builds with `lake build`;
- for falsifying entries: an explicit `theorem counterexample_<entry_id> : ¬ <statement> := …` with the counterexample as an executable term;
- for supporting entries (post-empirical): at minimum a `def` of the primitives plus a stated conjecture (`conjecture_<entry_id> : Prop`), so that the conjecture is *machine-readable* even if not yet machine-proved.

Lean files using only `Mathlib` and standard `Std` are acceptable; new tactics or new axioms beyond `Mathlib` must be reviewed by the human.

**Output schema**:

```json
{
  "entry_id": "string",
  "lean_passed": true,
  "lake_build_log_hash": "sha256:...",
  "lean_file_path": "lean_verified/<entry_id>/Statement.lean",
  "uses_axioms_beyond_mathlib": false,
  "build_time_seconds": 12.4
}
```

---

### 3.5 ROYAL-SOCIETY (Gate 5)

**Single sentence**: simulates an adversarial review by a senior fellow of the Royal Society and reports whether the entry would survive at *Proc. R. Soc. A* / *SIAM J. Comput.* / *Theory of Computing*.

**Inputs**: everything from Gates 1–4.

**Tools**: `Read`, adversarial reasoning prompt; access to the related-work file produced by the Scout.

**Output**:

| Grade | Meaning |
|---|---|
| **A** | Submit. No revision required. |
| **B** | Submit after minor revisions (clarity, citation, framing). |
| **C** | Resubmit after major revisions; hold back from external venue. |
| **D** | Reject with reformulation; the underlying intuition may be salvageable. |
| **F** | Reject; do not return. |

A grade ≥ B authorises external submission. Grades C and D return the candidate to the proposer with a typed list of revisions. Grade F is logged in `audit/dead_entries.jsonl`.

The reviewer specifically must answer:

1. *Is this a result, an observation, or a programme?* — and is the language used in the entry honest about which?
2. *What is the contribution?* — in one sentence, in the words a fellow of the Royal Society would use to a colleague.
3. *What are the limitations?* — explicit list. Empty lists are not accepted.
4. *What is the obvious next paper?* — required for grade ≥ B.

---

## 4. Control flow

```
candidate enters queue
      │
      ▼
  AUDITOR (Gate 1)
      │ pass
      ▼
  MATHEMATICIAN (Gate 2)
      │ pass
      ▼
  LITERATURE SCOUT (Gate 3)
      │ pass
      ▼
  LEAN-FORMALIZER (Gate 4)
      │ pass
      ▼
  ROYAL-SOCIETY (Gate 5)
      │ grade A or B
      ▼
  HUMAN SIGN-OFF (L. K.)
      │ approved
      ▼
  promotion to SUPPORTED / lean_verified / paper draft
```

A failure at any gate returns the candidate to the proposer with the structured reason, *and* logs the failure in `audit/rejection_log.jsonl`. Repeated failures from the same proposer pattern (e.g., multiple stubs using the same return-`n` shortcut) trigger a meta-alert: the *proposer* itself needs a code change.

---

## 5. Schedule of work — first 12 weeks

| Week | Focus | Deliverable |
|---|---|---|
| 1 | Audit `compendium_v01.tex` (4 Tropical Fourier entries) through all 5 gates | re-reproduction log, 4 Lean files |
| 2 | Royal Society review of the compendium; revisions | compendium_v02 |
| 3–4 | External preprint (arXiv cs.CC) of compendium_v02 | arXiv submission |
| 5 | Retraction sweep of `supported_findings.md` and `falsified_findings.md` per AUDIT_2026-05-08.md | clean public-facing reports |
| 6–7 | Promote framework CG-KW (`fw_85a254b4a0`) to scaffolding paper draft | `papers/cg_kw_programme.tex` |
| 8–9 | Wall Atlas curation (21 → ≤ 12 entries with proper barrier citations) | `papers/wall_atlas_curated.tex` |
| 10 | Triage of 343 INCONCLUSIVE; flag top-20 for re-test under new pipeline | re-test queue |
| 11–12 | First re-tested batch through 5-gate pipeline | first new SUPPORTED candidates (if any) |

---

## 6. Open questions for the human-in-the-loop

These are decisions that the multi-agent system must defer to L. K.:

1. **Compendium venue**: arXiv only (free), or aim for *Theory of Computing* (peer-reviewed, open access)?
2. **Lean base**: stay with `Mathlib4`, or also accept `Mathport` legacy translations?
3. **Frequency of audits**: weekly (automated by Auditor on the entire `notebook` JSONL), or only on entries that reach Gate 4?
4. **Proposer change**: the current LLM proposer keeps emitting stubs; should the proposer prompt include the `AUDIT_2026-05-08.md` document as a prior?

---

*Document maintained by L. K. Future revisions versioned in this file's git history.*
