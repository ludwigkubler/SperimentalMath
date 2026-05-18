# TARGET ARCHITECTURE — SEC v3

**Author:** Claude (Opus 4.7), commissioned by Ludovico Kubler
**Status:** PROPOSAL — pending sign-off
**Date:** 2026-05-19
**Companion:** `AS_IS.md` (the system we are replacing)

---

## 0. The thesis

> **The right unit of value is not the cycle, the conjecture, or the verdict. It is the paper.**

The current engine optimizes for *cycle throughput* (38/day) and *verdict counts*. Neither is what a research mathematician's output is measured on. A working mathematician at the level we want produces a **manuscript with reproducible results, clear motivation grounded in a named open problem, methodology robust to peer review, and an explicit position in the prior-work landscape**. That, exactly, is what v3 produces.

We will produce ~1–4 such manuscripts per year. The system is engineered around that cadence.

---

## 1. What v3 produces (the output contract)

The terminal output of v3 is a **PaperPack**: a directory containing:

```
papers/<problem_slug>/<finding_slug>/
├── manuscript.tex           # publication-grade LaTeX, target ≤16 pages
├── manuscript.pdf
├── manuscript.bib           # ≥20 citations, all verified to exist on arXiv/DOI
├── data/
│   ├── raw/                 # JSONL: every experiment seed-by-seed
│   ├── processed/           # parquet: tidy data per n, per seed
│   └── plots/               # PDF figures, generated reproducibly
├── lean/
│   ├── Statement.lean       # the precise claim, formalized
│   ├── Data.lean            # the data structure used
│   └── (Counterexample.lean | Verified.lean)  # if applicable
├── code/
│   ├── pyproject.toml       # locked deps via uv
│   ├── src/                 # the EXACT code that ran the experiments
│   └── tests/               # ≥80% coverage
├── replay.sh                # one-shot reproduction from clean machine
├── connection.json          # typed link to the P-vs-NP problem portfolio
└── audit.json               # full provenance: every LLM call, every commit, every seed
```

A PaperPack is **submittable as-is** to *Experimental Mathematics*, *Discrete Mathematics*, *ACM Trans. Comp. Theory*, etc. The bar: a third party with `replay.sh` reproduces every number and every figure.

This contract drives every architectural decision below.

---

## 2. Architectural style

### Style: **Functional core / Imperative shell over an explicit state machine**

- **Functional core**: data transformations are pure functions `Strategy → Plan`, `Plan → Experiment`, `Experiment → Finding`, `Finding → PaperDraft`. No I/O, no LLM calls, no side effects.
- **Imperative shell**: thin async wrappers that handle I/O (file, DB, LLM HTTP, sandbox) and call the core.
- **State machine**: every artifact has a finite set of states. Transitions are recorded with timestamps and provenance. No "phases" hidden in a 2000-LOC procedure.

### Not: pipeline, blackboard, multi-agent

- Not pipeline: pipelines are linear, brittle to ordering, hard to resume. v2 is a pipeline. We replace it.
- Not blackboard: too much shared mutable state for our scale. Overkill.
- Not multi-agent: agents are processes with autonomy; we want a controller-driven workflow with explicit decisions. Agents have their place for execution (an `lean_tactic_agent` for instance), not for control.

### Style references (read for shape, not for technology)

- **dbt / Dagster** — typed transformations between stages, lineage as first-class
- **Lean mathlib CI** — proof obligations as data
- **Snakemake / Nextflow** — workflow as DAG with explicit inputs/outputs
- **PostgreSQL replication** — explicit state machine for consistency

---

## 3. The data model

### 3.1 Six entities, normalized

```python
# domain/types.py — Pydantic v2 models with strict validation

class Problem(BaseModel):
    """A curated open question that bears on P vs NP. ~10–20 in the portfolio."""
    problem_id: str                   # e.g. "MONO_CLIQUE_2SQRT"
    title: str
    statement_md: str                 # markdown, ≤500 words
    statement_lean: Path              # Lean 4 file with the precise claim
    field: Literal[
        "circuit_lb", "communication_complexity", "proof_complexity",
        "sat_hardness", "barrier_theory", "fine_grained", "algebraic_complexity",
    ]
    significance_to_pvsnp: str        # ≤200 words, why this matters for P vs NP
    known_bounds: list["Bound"]       # current best-known upper/lower bounds
    known_barriers: list[BarrierRef]  # relativization, naturalization, …
    canonical_references: list[Citation]
    open_subquestions: list[OpenSubQuestion]
    status: Literal["active", "frozen", "resolved", "abandoned"]
    curated_by: str                   # human curator name
    last_reviewed: date

class Strategy(BaseModel):
    """An experimental approach to a Problem. LLM-proposed, human-approved."""
    strategy_id: str
    problem_id: str                   # FK
    hypothesis: str                   # precise empirical claim
    methodology_md: str               # how we plan to test
    n_range: tuple[int, int]          # min, max instance size
    n_steps: list[int]                # specific sizes to test
    seeds: list[int]
    expected_observable: Observable   # what we'll measure (typed)
    expected_scaling: ScalingHypothesis  # e.g. n^c log n with c ∈ [1, 2]
    statistical_power_target: float   # e.g. 0.95
    estimated_compute_minutes: int
    prior_work_dependencies: list[Citation]
    proposed_by: Literal["llm", "human"]
    approved_by: str | None           # set only after human gate
    status: Literal["proposed", "approved", "rejected", "running", "completed", "archived"]
    created_at: datetime
    pre_registration_hash: str        # locked once approved

class ExperimentPlan(BaseModel):
    """A concrete plan derived from a Strategy. Fully specified, executable."""
    plan_id: str
    strategy_id: str                  # FK
    sandbox_spec: SandboxSpec         # cpu/mem/time limits, image hash
    code_artifact: Path               # the test source, deterministically generated
    code_hash: str                    # sha256 — locks the artifact
    data_schema: Path                 # Lean 4 file declaring observable type
    expected_runtime_minutes: int
    status: Literal["planned", "running", "completed", "failed"]

class ExperimentRun(BaseModel):
    """A single execution at one (n, seed)."""
    run_id: str
    plan_id: str
    n: int
    seed: int
    started_at: datetime
    finished_at: datetime | None
    return_code: int | None
    observable_value: float | None
    metadata: dict                    # additional measurements
    raw_stdout: Path                  # archived, gz-compressed
    raw_stderr: Path

class Finding(BaseModel):
    """A statistical conclusion drawn from ExperimentRuns of one Strategy."""
    finding_id: str
    strategy_id: str
    n_values: list[int]
    n_seeds_per_n: int
    observable: Observable
    scaling_fit: ScalingFit            # fitted curve + 95% CI on parameters
    statistical_tests: list[StatTest]  # power, normality, outlier detection
    null_rejection_pvalue: float       # for the hypothesis under test
    interpretation: Literal[
        "supports_hypothesis", "rejects_hypothesis",
        "underpowered", "scaling_unclear",
    ]
    lean_statement: Path               # the claim, in Lean 4
    lean_verification: Path | None     # proof or counter-example, if applicable
    confidence_score: float            # 0–1, derived from stat tests + skeptic gate
    created_at: datetime

class Connection(BaseModel):
    """A typed edge from a Finding to a Problem. Verified, not just LLM-claimed."""
    connection_id: str
    finding_id: str                   # FK
    problem_id: str                   # FK
    relation_type: Literal[
        "narrows_bound", "rules_out_technique", "provides_evidence_for_lower",
        "provides_evidence_for_upper", "exposes_barrier", "instantiates_general",
    ]
    formal_argument_md: str           # human-readable, ≤500 words
    formal_argument_lean: Path | None # if formalizable
    strength: Literal["direct", "suggestive", "speculative"]
    verified_by: str                  # who/what signed off
    citations: list[Citation]
    created_at: datetime

class Paper(BaseModel):
    """A manuscript synthesizing Findings + Connections for one Problem."""
    paper_id: str
    problem_id: str
    title: str
    abstract: str
    findings: list[str]               # FKs
    connections: list[str]            # FKs
    contributors: list[str]           # always includes "Ludovico Kubler"
    target_venue: str
    status: Literal[
        "drafting", "internal_review", "human_approved",
        "submitted", "under_review", "accepted", "published", "withdrawn",
    ]
    submission_record: SubmissionRecord | None
    revision_number: int
    paperpack_path: Path              # the on-disk directory described in §1
    drafted_at: datetime
```

### 3.2 Why this data model

- **Normalized** — each entity has its own table; relationships are FKs. No JSON blobs of mixed-purpose fields like the 31-field `NotebookEntry`.
- **Schema-enforced** — Pydantic v2 catches malformed records at the boundary, with clear error messages.
- **Append-only by design** — entities have `created_at` but never `updated_at`. Status changes are recorded as separate `StatusTransition` events. No mutation.
- **Lean-native where it matters** — `Problem.statement_lean`, `Strategy.expected_observable` (typed in Lean), `Finding.lean_statement`. This forces precision; you cannot have a vague claim if you cannot type it in Lean.
- **Provenance everywhere** — `proposed_by`, `approved_by`, `verified_by`, `curated_by`. Every artifact can be traced to a responsible agent (human or specific LLM call).

### 3.3 Storage

- **Operational store**: PostgreSQL 16 (or SQLite for single-machine). Strict schema, indexes, transactions, ACID.
- **Artifact store**: filesystem under `~/Scrivania/SEC/v3/store/` — content-addressable (`sha256/aa/bb/<hash>`) for code, raw data, Lean files.
- **Search index**: SQLite FTS5 over `Problem.statement_md`, `Strategy.hypothesis`, `Paper.abstract` for the "what have we said about X?" queries.
- **No JSONL append-only chaos.** That was v2's choice and it's bad — unindexed, schema-drifts.

---

## 4. State machine (the orchestration backbone)

Every Strategy progresses through this graph:

```
                       ┌──────────────┐
                       │   PROPOSED   │  ← LLM (StrategyGen) reads Problem,
                       └──────┬───────┘    proposes hypothesis + methodology
                              │
                  human gate D2 (weekly approval)
                              │
            ┌─────────────────▼─────────────────┐
            │             APPROVED              │
            └──────┬─────────────────────┬──────┘
                   │                     │
              reject?              proceed
                   │                     │
                   ▼                     ▼
            ┌──────────────┐      ┌──────────────┐
            │   REJECTED   │      │    PLANNED   │  ← ExperimentPlan generated +
            └──────────────┘      └──────┬───────┘    sandbox-built + pre-reg locked
                                          │
                                          ▼
                                  ┌──────────────┐
                                  │    RUNNING   │  ← ExperimentRuns enqueue
                                  └──────┬───────┘
                                          │
                              all runs done OR aborted
                                          │
                                          ▼
                                  ┌──────────────┐
                                  │   ANALYZED   │  ← Finding emitted by
                                  └──────┬───────┘    StatisticalEngine
                                          │
                                          ▼
                                  ┌──────────────┐
                                  │  CONNECTED   │  ← Connection edges verified
                                  └──────┬───────┘    (auto-proposed, human-confirmed)
                                          │
                                          ▼
                                  ┌──────────────┐
                                  │   DRAFTED    │  ← Paper draft generated
                                  └──────┬───────┘
                                          │
                                  human gate D3
                                          │
                                          ▼
                                  ┌──────────────┐
                                  │  SUBMITTED   │
                                  └──────────────┘
```

**Properties of this state machine:**

- **Each transition is a typed pure function** in the functional core.
- **Each transition is recorded** in `StatusTransition(strategy_id, from, to, ts, agent, evidence_hash)`.
- **Resumable**: at any state, a fresh worker can pick up where things were left.
- **Two human gates** (D2 strategy approval, D3 paper approval) — Ludo's bandwidth is concentrated where it adds most value.
- **No phase implicit in code paths.** If you want to know the state of strategy X, you query the database.

---

## 5. Component breakdown

### Core (~3500 LOC target)

1. **`domain/`** (~600 LOC, pure)
   - `types.py` — Pydantic models above
   - `transitions.py` — pure-function state transitions
   - `validations.py` — schema validators, never raise outside boundaries

2. **`portfolio/`** (~400 LOC)
   - `loader.py` — reads `problems/*.toml` into `Problem` instances
   - `validator.py` — Lean-check that `statement_lean` compiles + matches `statement_md`
   - `index.py` — FTS5 search

3. **`strategy_gen/`** (~700 LOC)
   - `proposer.py` — LLM call (Claude Opus) given a `Problem` produces candidate `Strategy`
   - `human_gate.py` — CLI + web UI to approve/reject (Ludo's interface)
   - `pre_registration.py` — locks `Strategy` hash to file once approved

4. **`experiment/`** (~900 LOC)
   - `planner.py` — `Strategy → ExperimentPlan` (deterministic)
   - `code_synthesizer.py` — generates the experiment code from the plan + LLM call; output is sandboxed
   - `runner.py` — async pool, runs `ExperimentRun` jobs, collects results
   - `sandbox.py` — bubblewrap or firejail-based isolation, deterministic seeds
   - `lean_check.py` — verifies generated experiment code's data schema matches `data_schema` declaration

5. **`stats/`** (~500 LOC)
   - `aggregator.py` — `ExperimentRun → Finding`
   - `scaling_fit.py` — fits power-law, log-linear, polynomial; CI via bootstrap
   - `power.py` — pre-experiment power calculation; flags underpowered designs
   - `skeptic.py` — port + clean of v2's 4-layer skeptic; adds 5th layer: statistical-test-validation

6. **`connection/`** (~500 LOC)
   - `proposer.py` — LLM call: given `Finding` + portfolio, propose `Connection`
   - `verifier.py` — Lean-checked + citation-grounded validation
   - `human_gate.py` — Ludo confirms strength

7. **`paper/`** (~700 LOC)
   - `templater.py` — LaTeX templates per venue
   - `composer.py` — `Paper(findings, connections) → manuscript.tex`
   - `bib_resolver.py` — every cited work verified to exist via DOI/arXiv
   - `figure_gen.py` — matplotlib (reproducible) → PDF figures
   - `paperpack.py` — assembles the directory in §1

### Infrastructure (~1500 LOC target)

8. **`orchestrator/`** (~400 LOC)
   - `dispatcher.py` — drives state-machine transitions
   - `scheduler.py` — APScheduler or cron-like — replaces v2's 20+ separate cron entries
   - `resumer.py` — recovery on restart

9. **`storage/`** (~400 LOC)
   - `db.py` — SQLAlchemy session management
   - `migrations/` — Alembic
   - `content_addressed.py` — sha256-keyed artifact store

10. **`llm/`** (~300 LOC)
    - `router.py` — heavy refactor of v2's 11-provider router; drop dead providers
    - `cache.py` — content-addressed LLM response cache for replays
    - `audit.py` — append every call to `audit.jsonl` with full provenance

11. **`watchdog/`** (~200 LOC, port from v2)
    - Already built and works — port verbatim, just adapt paths.

12. **`api/`** (~200 LOC)
    - `routes.py` — FastAPI; `/portfolio`, `/strategies`, `/findings`, `/papers/<id>`, `/status`
    - For Ludo's human gates + dashboards.

### Tools (~500 LOC target)

13. **`sandbox/`** — bubblewrap recipe + image build
14. **`lean/`** — wrapper around `lake build`, with caching
15. **`solvers/`** — kissat, z3, cadical adapters (typed Python interfaces)

### Total: ~5500 LOC

Vs v2's ~54K LOC across 122 modules. **Throw away ~90%, write ~5K fresh.**

---

## 6. The Problem Portfolio (the knowledge layer v2 lacked)

This is the keystone. Without it the rest is castle on sand.

### 6.1 Format

`problems/<problem_id>.toml` — human-curated, schema-validated.

Example:

```toml
problem_id = "MONO_CLIQUE_RAZBOROV_85"
title = "Razborov's monotone clique lower bound: closing the gap to k = 5"
field = "circuit_lb"
status = "active"
curated_by = "Ludovico Kubler"
last_reviewed = 2026-05-15

[statement]
markdown = """
Razborov (1985) proved that monotone circuit size for k-CLIQUE on n vertices is at least n^(Ω(k)) for k ≤ (log n)^(1/4). The bound has been improved to k ≤ (log n)^(1/2) (Alon–Boppana 1987). The open question: can the upper limit on k be pushed to k = n^δ for some δ > 0?
"""
lean_file = "problems/MONO_CLIQUE_RAZBOROV_85.lean"

[significance_to_pvsnp]
text = """
The CLIQUE problem is NP-complete. A monotone-circuit lower bound of n^Ω(n^δ) for unbounded k would not directly resolve P vs NP (CLIQUE has non-monotone circuits), but it would close a 40-year question in circuit complexity and resolve naturalness obstructions in that regime.
"""

[[known_bounds]]
type = "lower"
parameter = "k"
value_expr = "n^Omega(k)"
range_valid = "k ≤ (log n)^(1/2)"
reference = "alon_boppana_1987"

[[known_barriers]]
name = "natural_proofs"
caveat = "Monotone bounds escape NP-natural; this question is below the barrier."

[[canonical_references]]
key = "razborov_1985"
arxiv_id = null
doi = "10.1070/SM1985v050n01ABEH002825"
title = "Lower bounds on monotone complexity of the logical permanent"

[[canonical_references]]
key = "alon_boppana_1987"
arxiv_id = null
doi = "10.1007/BF02579196"

[[open_subquestions]]
id = "sub1"
text = "Does there exist a constant δ > 0 such that the Alon–Boppana approximation method gives lower bounds for k = n^δ?"
suggested_attack = "compute_clique_indicator_polynomial_degree"
```

### 6.2 Initial portfolio (proposed seed list)

The first Problem catalog has ~12 entries spanning:
- 3 in circuit lower bounds (monotone, AC^0[p], formula depth)
- 2 in communication complexity (set-disjointness variants, multiparty)
- 2 in proof complexity (resolution width, Frege)
- 1 in SAT hardness (random k-SAT thresholds)
- 1 in barrier theory (algebrization frontier)
- 1 in fine-grained (3-SUM, OV)
- 2 in algebraic complexity (permanent vs determinant, GCT)

**Curation procedure**: I draft each problem from canonical sources (Allender's surveys, Razborov-Rudich, Aaronson's chapters, Williams' algorithmic-method paper). Ludo reviews each. Locked.

### 6.3 What grows the portfolio over time

- **New entries** added when a research direction crystallizes
- **`open_subquestions`** updated when sub-results land
- **`known_bounds`** updated when literature scans find new papers
- **`status`** changes (`active → resolved` when a problem is settled by external work)

This is the engine's institutional memory.

---

## 7. Quality engineering — the "non codice di merda" specs

### 7.1 Language and toolchain

- **Python 3.12+ only** (drop 3.11 compat)
- **uv** for dependency + venv management (replaces pip)
- **mypy --strict** on `domain/`, `stats/`, `experiment/planner.py`, `paper/composer.py`
- **ruff** check with rules `E,F,W,B,C4,SIM,UP,N,DTZ,RET,RUF` and pre-commit hook
- **black** for formatting (line length 100)
- **pytest** with `--cov` minimum 80% on functional core, 60% on shell

### 7.2 Type safety

- **Pydantic v2** models for all domain types (validation at boundary)
- **typing.NewType** for IDs (`StrategyId = NewType("StrategyId", str)`) — prevents mixing
- **Literal types** for enums (not `str`)
- **TypedDict / Protocol** for structural types
- **No `dict[str, Any]`** in domain layer. Period.

### 7.3 Functional core / Imperative shell

The core (`domain/`, `stats/`, `paper/composer.py`, etc.):
- **Pure functions only**. No I/O, no LLM, no time, no random.
- **Receive everything as arguments**, return everything as values.
- **Easily unit-tested** with synthetic data.

The shell:
- **Async wrappers** around I/O
- **Dependency-injected** (LLM client, DB session, filesystem are interfaces)
- **Easy to swap** for tests (in-memory DB, fake LLM)

### 7.4 Determinism

- **Every experiment is reproducible** from `(code_hash, sandbox_spec, n, seed)` → output
- **LLM calls are content-cached**: same prompt → cached response (for replay)
- **Sandbox is hermetic**: no network, no host filesystem, fixed time, fixed entropy

### 7.5 Observability

- **Structured logging** (`structlog` with JSON output)
- **OpenTelemetry traces** for cross-component flows
- **Watchdog port from v2** with extensions for the new entities

### 7.6 CI

- **GitHub Actions** running on every commit:
  1. ruff
  2. mypy --strict (on tagged dirs)
  3. pytest with coverage report
  4. Lean build of all `problems/*.lean`
  5. Smoke test: full end-to-end on a tiny mock Problem
  6. Compare cached vs fresh LLM output (drift detection)

### 7.7 Project structure

```
v3/
├── pyproject.toml
├── uv.lock
├── README.md
├── ARCHITECTURE.md            # this design doc, frozen at deployment
├── domain/
│   ├── types.py
│   ├── transitions.py
│   ├── validations.py
│   └── __init__.py
├── portfolio/
├── strategy_gen/
├── experiment/
├── stats/
├── connection/
├── paper/
├── orchestrator/
├── storage/
├── llm/
├── watchdog/
├── api/
├── tools/
├── problems/                  # the curated portfolio (TOML + Lean)
│   ├── MONO_CLIQUE_RAZBOROV_85.toml
│   ├── MONO_CLIQUE_RAZBOROV_85.lean
│   └── …
├── tests/
│   ├── unit/                  # mirrors source tree
│   └── e2e/
└── .github/workflows/ci.yml
```

---

## 8. Migration plan (how we get there from v2)

### Phase 0 — Curation week
- Build initial Portfolio (12 Problems)
- I draft, Ludo reviews each
- Output: `problems/*.toml` + `*.lean` files locked
- **Deliverable**: portfolio fully populated and Lean-buildable
- **Effort**: ~10–15h of Ludo's time + ~20h of mine

### Phase 1 — Foundations (2 weeks)
- Set up `v3/` repository structure, CI, pre-commit
- Write `domain/types.py` with all Pydantic models
- Write `domain/transitions.py` (pure state-machine)
- Write `storage/db.py` with migrations
- Write `watchdog/` (port from v2, adapt paths)
- **Deliverable**: empty pipeline that can ingest a `Strategy` and progress through all states (with mocked execution)
- **Effort**: ~30h of mine, ~5h of Ludo's review

### Phase 2 — Strategy + Experiment (3 weeks)
- `strategy_gen/proposer.py` + human gate UI
- `experiment/planner.py`, `code_synthesizer.py`, `runner.py`, `sandbox.py`
- `stats/aggregator.py`, `scaling_fit.py`, `power.py`
- First end-to-end run on one Problem from the portfolio
- **Deliverable**: one Strategy progresses from PROPOSED → ANALYZED, producing a real Finding
- **Effort**: ~50h mine, ~5h Ludo

### Phase 3 — Connection + Paper (2 weeks)
- `connection/proposer.py`, `verifier.py`
- `paper/composer.py`, `bib_resolver.py`, `figure_gen.py`, `paperpack.py`
- First end-to-end PaperPack generation (even if the paper itself is preliminary)
- **Deliverable**: one PaperPack at `papers/<problem>/<finding>/`
- **Effort**: ~30h mine, ~10h Ludo (paper review)

### Phase 4 — Shutdown v2, run v3 (1 week)
- Migrate `retractions.json`, `lean_verified/`, the legit Tropical Fourier counter-example, the Forman-Ricci finding into v3 entities
- Switch cron from v2 modules to v3 orchestrator
- Keep v2 in `~/Scrivania/SEC/v2/` for ~6 months as reference, then delete
- **Deliverable**: v3 in production, v2 shut down
- **Effort**: ~15h mine, ~3h Ludo

### Phase 5 — First real paper (4–8 weeks)
- Run v3 against one Problem for real
- Iterate Strategy → Plan → Run → Analyze → Connect → Draft
- Ludo reviews paper
- **Deliverable**: first submitted manuscript
- **Effort**: continuous + ~20h Ludo review

### Total

- **Engineering before first paper**: ~9 weeks calendar / ~125h my work / ~25h Ludo
- **First real paper**: month 3
- **Steady state**: ~1 paper / quarter

---

## 9. What we throw away from v2

- ❌ `pvsnp_explorer.py` (2035 LOC) — replaced by state machine
- ❌ `pvsnp_framework.py` (679 LOC) — frameworks become Problems (curated, not LLM-generated)
- ❌ The 11-provider router for LLMs — keep 2 (Claude + 1 local Ollama)
- ❌ The ENTITY runtime entirely — it doesn't contribute to math
- ❌ All monetization modules (~13K LOC) — long disabled
- ❌ `pvsnp_taxonomy`, `pvsnp_linkage_graph`, `pvsnp_compute --sweep` — over-engineered
- ❌ The `Field_A × Field_B` proposer — replaced by Problem-grounded `StrategyGen`
- ❌ The `framework lifecycle` (proposed → elaborated → evaluated → …) — collapses into Strategy lifecycle
- ❌ JSONL append-only stores — replaced by Postgres/SQLite
- ❌ 1370 jsonl files in `audit/` — moved to content-addressable store
- ❌ `~/SEC` diverged tree (Phase 4 of cleanup) — finally killed

## 10. What we keep from v2 (verbatim or port)

- ✅ `sec_watchdog.py` — works well
- ✅ The audit logger pattern (`src/entity/audit_log.py`) — generalize
- ✅ The sandbox shell with AST validator for `python -c` — port
- ✅ Lean infrastructure: mathlib on disk, `lake build` wrapper
- ✅ Arxiv mirror — but now it feeds the Portfolio reviewer, not novelty filter
- ✅ The `retractions.json` discipline — formalize as a state transition
- ✅ The pitfalls file — generalize as a learnings store

## 11. What v3 deliberately does NOT do

- Not 24/7 autonomous. The system has natural pause points (D2, D3 human gates).
- Not "thousands of cycles". One Strategy per week at peak. Quality > volume.
- Not chasing SUPPORTED verdicts. We chase publishable Findings + verified Connections.
- Not chasing "novelty". Novelty is implicit in attacking a curated Problem with an unstudied Strategy.
- Not solving P vs NP. We produce work that contributes to the P-vs-NP **landscape** — citable, defensible, building on a clear named problem.

---

## 12. Risks and mitigations

| Risk | Severity | Mitigation |
|:---|:--|:---|
| Curating the Portfolio is harder than expected | High | Phase 0 has dedicated time; we accept smaller initial portfolio if needed |
| Lean integration is heavyweight for some Problems | Medium | Allow `lean_file = null` for now if the statement is not yet formalizable; flag as tech debt |
| LLM hallucination in Strategy proposals | Medium | Human gate D2 catches it; pre-registration locks the experiment plan |
| Underpowered experiments give noisy Findings | Low | `stats/power.py` computes minimum-detectable-effect before any run |
| Connection claims are not credible | Medium | Connection verification requires either Lean argument or citation chain |
| First paper takes longer than 3 months | Medium | Acceptable; quality > speed |
| Ludo's review-bandwidth becomes the bottleneck | High | Concentrate Ludo's attention at D2/D3; everything else automated; can scale to 1 review-hour per week |

---

## 13. Decision points for Ludo

Before Phase 0, I need answers to:

1. **PostgreSQL or SQLite** for the operational store?
   - SQLite: single-machine, simpler ops, fine for our volume (~10K entities/year)
   - PostgreSQL: prepares for multi-machine, more robust, more ops complexity
   - **Recommendation**: SQLite

2. **Single LLM (Claude Opus only) or dual (Claude + Ollama)?**
   - Single: simpler, all calls are top-quality
   - Dual: Ollama for cheap iterations on code synthesis, Claude for strategy + judging
   - **Recommendation**: Dual; Claude for proposer/judge, Ollama for code synthesis (where you'd benefit from cheap retries)

3. **Web UI for human gates or CLI only?**
   - CLI only: faster to build, requires Ludo at terminal
   - Simple FastAPI dashboard: 1 day extra work, much nicer for review
   - **Recommendation**: FastAPI dashboard

4. **Target venue for first paper?**
   - Different venues have different conventions (LaTeX class, page limits, citation styles)
   - **Recommendation**: *Experimental Mathematics* (Taylor & Francis) — well-fitting venue for this kind of work

5. **Initial portfolio size: 12 or smaller?**
   - 12 is a moderate spread across subfields
   - Smaller (6) is easier to curate well in Phase 0
   - **Recommendation**: Start with 6; grow during Phase 1

---

## 14. The single bet this architecture makes

> **The right unit of value is the paper. Everything else is a means to that end.**

If that bet is wrong — if you want a system that, say, contributes lemmas to mathlib without ever writing a paper, or builds a competitive theorem-proving agent, or maximizes the rate of conjecture refutations — then **this architecture is wrong**, and we should design a different one.

If that bet is right, then this is the system. Phase 0 starts the moment you approve.

---

*Companion document to AS_IS.md. Read together: AS_IS describes what is, this describes what should be, and the migration plan describes how we get from one to the other.*
