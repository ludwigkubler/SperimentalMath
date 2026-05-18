# AS-IS Architecture — SEC P-vs-NP Research Engine

**Date:** 2026-05-18
**Author:** Claude (Opus 4.7), commissioned by Ludovico Kubler
**Scope:** L3 architecture analysis — describe the system as it is today, identify structural choices, surface the design questions a redesign must answer.
**Companion docs:**
- `AS_IS_inventory.md` (in this folder) — per-module catalogue (122 modules, ~54K LOC)
- `OPERATIONAL_STATUS.md` (repo root) — runtime state and tech debt

---

## 0. Executive summary

The system is a **pipeline-linear research engine with rule-based gates**. A worker cycle (`run_one_cycle`) takes a freshly-proposed conjecture through ~15 phases (LLM-heavy) and emits a verdict (`SUPPORTED` | `FALSIFIED` | `INCONCLUSIVE` | `BARRIER_HIT` | `SCOOPED`). A second-order **framework lifecycle** (`PROPOSED → ELABORATING → EVALUATED → PROMOTED → PUBLISHED → DEAD`) sits on top: each framework spawns ~10 sub-conjectures, each of which goes through the same pipeline.

Every artifact (conjectures, frameworks, retractions, barrier checks, …) is an **append-only JSONL file**. There is no indexed knowledge base. There is no structured representation of "what we already know about computational complexity"; novelty is checked by arXiv/S2/ECCC search to AVOID re-discovery, not to BUILD ON existing results.

The architecture has been **incrementally accreted**: the main `NotebookEntry` dataclass has 30+ fields marked with milestone tags (`T1.1` … `T3.9`, `F1` … `F4`, "Skeptic Gate", "Problem Focus Mode"). Each milestone added fields. None removed any.

**Conclusion from analysis:** the current architecture is a competent **empirical-research framework** that produces structured output and catches its own stub-test pathologies (the audit pipeline works). It is **structurally unable to make progress on P vs NP** because (i) P-vs-NP-style questions cannot be settled by `n ≤ 20` empirical tests, (ii) there is no accumulating mathematical knowledge that conjectures build on, and (iii) the LLM proposer generates "field-A × field-B" cocktails without grounding in specific open problems.

The L3 design questions are at the end of this document.

---

## 1. What the system does today

### 1.1 The main worker: `run_one_cycle` (15 phases)

Source: `pvsnp_explorer.py:1499`. Each cycle takes ~5–15 min wall-clock, makes 5–12 LLM calls, and emits exactly one notebook entry.

| Phase | Module | LLM calls | Side effects |
|------:|:-------|----------:|:-------------|
| 1. **Propose** (or mutate or pre-built) + embedding dedup | `propose_conjecture` | 1 generator + 1 embed | reads notebook; computes cosine against last 500 |
| 2. **F1 barrier filter** | `pvsnp_barriers.run_barrier_filter` | 2× per barrier (consolidator) | early exit `BARRIER_HIT` |
| 3. **Pre-registration** | `write_preregistration` | 1 | hash + append `pvsnp_preregistrations.jsonl` |
| 4. **Novelty** | `check_novelty` | 1 judge + 3 HTTP (arxiv, S2, ECCC) | early exit `SCOOPED` |
| 5. **Test gen + run, with retry** | `generate_and_run_test_with_retry` | up to 4× | sandbox writes, `tester_known_pitfalls.txt` |
| 6. **Critic** | `critic_pass` | 1 (skipped on crash) | none |
| 7. **Judge** | `judge_result` | 1 | sets `verdict`, `reason`, `next_direction` |
| 8. **Safety rails** | inline (8a-f checks) | 0 | may downgrade `SUPPORTED → INCONCLUSIVE` |
| 9. **Skeptic gate** (only if SUPPORTED) | `pvsnp_skeptic.skeptic_gate` | up to 3 (adversarial layer) | may downgrade |
| 10. **Notebook append** | `_append_notebook` | 0 | append `pvsnp_notebook.jsonl` |
| 11. **Paper writer** (only if SUPPORTED+CONFIRM) | `pvsnp_writer.write_paper` | 1 | LaTeX→PDF in `pvsnp_papers/` |
| 12. **Lean stub** (only if SUPPORTED+CONFIRM) | `write_lean_stub` | 1 | `pvsnp_lean_stubs/{eid}.lean` |
| 13. **F3 Lean gate** | `pvsnp_lean_gate` | 1+ tactic search | `lake build`; sets `lean_gate_result` |
| 14. **F3 Lean PROOF attempt** (only if SUPPORTED_HARDENED) | `pvsnp_lean_proof` | 1 | `lean_verified/{eid}/Eaudit.lean` |
| 15. **Lean counterexample** (only if FALSIFIED) | `pvsnp_lean_counterexample` | 1 | `lean_counterexamples/{eid}.lean` |

Plus, after the cycle:
- Reviewer pack PDF (`pvsnp_reviewer_pack`)
- Citation rigor (`pvsnp_citations`)
- All MD reports regenerated (`pvsnp_report`)

**Observation:** Phases 11–15 trigger only on positive outcomes that **have not happened in 22 days** (zero SUPPORTED, zero high-confidence FALSIFIED post-2026-04-25). So 60% of the pipeline complexity is dormant code.

### 1.2 The second-order loop: framework lifecycle

Source: `pvsnp_framework.py:509` (`framework_tick`).

State graph:
```
PROPOSED ─┬→ ELABORATING ─→ EVALUATED ─┬→ PROMOTED ─→ PUBLISHED
          │                            │
          │                            └→ DEAD (fitness < 0.10)
          │                            └→ SUSPENDED
          └→ DEAD (no sub-conjectures generated)
```

A framework is a dict with `primitives`, `operations`, `target_invariant`, `axioms_tentative` — all LLM-generated. `ELABORATING` spawns N=10 sub-conjectures, each of which goes through the worker pipeline. `fitness` is a weighted combination of how many survived each gate (barrier-pass, test-OK, critic-CONFIRM, Lean-build-success).

**Currently active:** 6 frameworks (audit count). `frameworks/dead/` is **empty despite 18 BARRIER_HIT** logged — so the `DEAD_THRESHOLD` doesn't fire as expected.

### 1.3 The skeptic gate (the only runtime gate)

Source: `pvsnp_skeptic.py:366` (`skeptic_gate`).

Four sequential layers; short-circuit on first DOWNGRADE:
1. **Tautology AST** — deterministic check for self-referential or hardcoded comparisons (`if X == X:`, etc.)
2. **Boundary replay** — re-run the test with edge-case seeds (n=0, 1, etc.)
3. **Adversarial LLM** — 3 attempts to find a refutation
4. **Kissat oracle** — for SAT-related claims, run actual SAT solver

**Critical:** fires only if `verdict == "SUPPORTED"`. Since SUPPORTED count = 0 for 22 days, the gate fires **never**. The famous `health_report.skeptic_168h.not_invoked = 418` was misread as a bug; it is the correct count of "no SUPPORTED to gate".

### 1.4 Cron map (control flow)

| Schedule | Target | Side effect |
|:---|:---|:---|
| `*/5 min` | `sec_watchdog.py` (NEW) | writes `STATUS.md` + alerts |
| `*/5 min` | `pgrep \|\| spawn pvsnp_explorer` | restart if dead |
| `*/5 min` | `solar_schedule --check` | tunes autonomy |
| `*/5 min` (legacy C-001) | `watchdog.sh`, `security_monitor.py` | C-001 era cruft, still firing |
| `*/30 min` | `pvsnp_monitor` | auto-fix (SERVICE_STALL, …) |
| `*/4 h` | `pvsnp_linkage_graph --refresh` | graph rebuild |
| `*/6 h` | `pvsnp_taxonomy --reweight`, `sec_healthcheck.sh`, `self_improve --tick` | reweight + health + self-mod |
| `*/12 h` | `pvsnp_compute --sweep` | walks OPEN graph nodes |
| `daily 18:00` | C-001 `daily_report.py` | report to `~/Scrivania/pubblicazioni/` |
| `daily 09:00` | C-001 `c003b_counterexample.py` | C-003b focused search |
| `daily 08:00` | C-001 `literature_scan.py` | literature scan |
| `daily 23:00` | C-001 `git_sync.sh` | git commits |
| `daily 03:33` | `pvsnp_reflection` | daily audit |
| `daily 03:00` | `cleanup_videos.py` | monetization (idle) |
| `3× daily 02:11/10:11/18:11` | `pvsnp_arxiv_mirror` | scrape arXiv 50/cat |
| `Sundays 03:00` | `pvsnp_weekly_replay --pick 10` | drift detection |
| `Sundays 04:00` | `pvsnp_compendium` | LaTeX compendium |
| `Sundays 02:33` | `pvsnp_few_shot --regenerate --k 6` | example regen |
| `Mondays 09:13` | `pvsnp_review_alert --window-h 168` | review digest |
| `hourly :17` | `sync_from_sec.sh` | mirror source into kissat |
| `hourly :41` | `pvsnp_sec_diary` | diary writer |
| `hourly :47` | `sync_output.sh` | git push outputs |

**Observations:**
- **3 independent watchdogs** fire every 5 min: `sec_watchdog.py` (new, robust), the inline `pgrep || spawn` (auto-restart), and the C-001 `watchdog.sh` (legacy). They don't coordinate but they also don't conflict.
- **C-001 era cron is still firing** even though memory said "STOPPED". The legacy `src research --config research_gpu.yaml --max-cycles 200` loop runs in parallel with `pvsnp_explorer`, writing to its own log. Two research loops coexist with no resource conflict.
- **The most-frequent feedback signal to a human is the Monday `review_alert` digest.** Nothing else is push-driven. Everything else is pull (open the repo, read a file).

### 1.5 Storage and state

**Files (all append-only JSONL or single JSON):**
- `pvsnp_notebook.jsonl` (15 MB) — every cycle's full record
- `pvsnp_preregistrations.jsonl` (742 KB) — Popper-style commits
- `pvsnp_frameworks.jsonl`, `pvsnp_dead_frameworks.jsonl`, `pvsnp_framework_children.jsonl`
- `pvsnp_barriers_rejected.jsonl` (93 KB)
- `pvsnp_lean_counterexample_log.jsonl` (13 KB)
- `claude_max_call_log.jsonl` (430 KB) — every Claude API call audited
- `monitor_alerts.jsonl` (199 KB)
- `tester_known_pitfalls.txt` (now 81 entries, was 13 pre-2026-05-15)
- `retractions.json` (9 entries)
- `compendium_state.json`
- Plus generated artifacts: `pvsnp_papers/`, `pvsnp_lean_stubs/`, `lean_verified/`, `lean_counterexamples/`, `reports/*.md+pdf`

**Databases:**
- `~/data/entity/entity.db` — ENTITY runtime SQLite (knowledge graph proxy, memory, drives, neurochemistry)
- `~/data/sec.db`, `~/data/sec_learning.db` — SEC main databases (purpose less clear)
- `~/data/entity/audit/actions-YYYY-MM-DD.jsonl` — tool-action audit log (added 2026-05-13)

**Important:** **no indexed mathematical knowledge base.** No graph database, no triple store, no Lean library mirror with theorem index. The `linkage_graph` module produces relationships between *cycles* (`entry_id` → `entry_id`), not between *mathematical concepts*.

---

## 2. Data model (the central abstractions)

### 2.1 `NotebookEntry` (pvsnp_explorer.py:70)

The atomic record. **31 fields**, accreted across milestones:

```python
@dataclass
class NotebookEntry:
    # Core identity (T1.0)
    entry_id: str
    ts: float
    phase: str               # "PROPOSED" | "NOVELTY_FAIL" | "TEST_FAIL" | "VERDICT"
    title, field_A, field_B, statement, rationale: str

    # Novelty (T2.5)
    novelty_queries: list[str]
    novelty_hits: list[dict]
    novelty_verdict: str

    # Test (T1.2)
    test_code, test_stdout: str
    test_returncode: int
    test_elapsed_s: float

    # Verdict (T1.0)
    final_verdict, final_reason: str

    # Tier-1/2/3 extensions
    embedding: list[float]            # T1.3 cosine dedup
    preregistration_hash: str         # T3.9 Popper commit
    acceptance_criterion: str         # T3.9
    seed_results: list[dict]          # T1.2 per-seed
    aggregate_stats: dict             # T1.2 mean/std/CI
    critic_verdict, critic_reasoning: str   # T1.1
    parent_entry_id, mutation_type: str     # T2.4
    paper_path: str                   # T2.6
    lean_stub_path: str               # T3.7

    # V2 F1/F2/F3/F4 extensions
    barrier_checks: list[dict]        # F1
    barrier_final: str                # F1
    taxonomy_category, taxonomy_status: str   # F2
    lean_gate_attempts: list[dict]    # F3
    lean_gate_result, lean_build_log: str    # F3
    framework_id, framework_role: str       # F4

    # Skeptic Gate
    skeptic_verdict, skeptic_downgrade_reason: str
    skeptic_layers: dict

    # Problem Focus Mode
    focus_id: str
```

**Observation:** this dataclass is the architecture's **central abstraction**. Almost every module reads/writes notebook entries. Its shape determines what the system can express.

### 2.2 `Framework` (pvsnp_framework.py:48)

```python
@dataclass
class Framework:
    framework_id: str
    ts: float
    generation: int = 0
    parent_framework_id: str = ""
    mutation_from_parent: str = ""
    name: str
    taxonomy_category: str
    primitives: list[dict]        # arbitrary LLM-generated dicts
    operations: list[dict]        # arbitrary LLM-generated dicts
    target_invariant: dict        # arbitrary LLM-generated
    axioms_tentative: list[str]   # arbitrary LLM-generated strings
    status: str = "PROPOSED"
    sub_conjecture_entry_ids: list[str]
    fitness_components: dict
    fitness: float
    paper_path, lean_module_path: str
```

**Observation:** `primitives`, `operations`, `target_invariant`, `axioms_tentative` are typed as `dict`/`list[str]` without schema. The pipeline does not enforce them, and no module reads them structurally — they are inputs to the LLM prompt of `elaborate_one`, not data that machinery operates on. **In effect, a Framework is a structured natural-language brief, not a mathematical object.**

### 2.3 `Refutation` (pvsnp_compendium.py:60)

A view-model over a notebook entry that has `final_verdict=FALSIFIED ∧ critic_verdict=CONFIRM ∧ Lean file present`. Used only by the compendium generator. As of the 2026-05-18 retraction-filter fix: 2 active refutations in v02.

### 2.4 `retractions.json`

Manual artifact maintained by humans (Ludo, post-audit-2026-05-08):

```json
{
  "_meta": { "audit_document": "AUDIT_2026-05-08.md", "audit_date": "2026-05-08", "audit_author": "Ludovico Kubler", "schema_version": 1 },
  "retracted": [
    { "entry_id": "...", "original_verdict": "SUPPORTED"|"FALSIFIED", "title": "...", "reason": "...", "action": "RETRACTED" }
  ],
  "demoted": [ ... ]  // SUPPORTED → INCONCLUSIVE pending reformulation
}
```

Consumed by: `pvsnp_report.py` (filters MD reports) and now `pvsnp_compendium.py` (sentinel `sec_compendium_retraction_filter_v1`, 2026-05-18). **Adding to retractions.json is the only way human judgement enters the pipeline post-hoc.**

---

## 3. The architecture in one sentence

> **The system is a 15-phase LLM-orchestrated pipeline that ingests cocktailed `field_A × field_B` conjectures, runs them through empirical tests on `n ≤ 20` instances, and emits structured verdicts into an append-only log. A separate framework lifecycle adds a layer of mutation+evolution on top. A multi-watchdog cron keeps it alive 24/7. There is no knowledge layer.**

Architectural style: **rule-based pipeline with verifier gates**, not blackboard, not knowledge-graph, not multi-agent, not goal-directed search.

---

## 4. Structural critique (10 points)

These are properties of the current architecture that make P-vs-NP progress unreachable, *regardless of how well each component is implemented*.

### 4.1 No knowledge layer
There is no structured representation of "what is known about computational complexity." `pvsnp_arxiv_mirror.py` scrapes 50 abstracts/category 3× daily into JSONL files; novelty filter searches them; but no module consumes them as **mathematical content**. The system has read 0 theorems, 0 proofs, 0 connections. It has only checked whether titles are similar to its own proposals.

### 4.2 The proposer is shallow combinatorial
`PROPOSER_SYSTEM` (explorer.py:362) is well-prompted ("working research mathematician in computational complexity") but its grounding is the **blacklist of prior attempts**, not any mathematical context. The LLM is asked to generate "novel" Field_A × Field_B combinations. This produces titles like "Forman-Ricci Min-Curvature of Term-Overlap Graph Lower-Bounds Monotone k-CLIQUE DNF" — a syntactically-valid math sentence that has no grounding in the actual landscape of monotone-DNF lower-bound techniques. It is **vocabulary collision, not theorem-building**.

### 4.3 Empirical testing cannot settle P-vs-NP-class questions
The pipeline tests on `n ≤ 20`. P-vs-NP barriers (relativization 1975, natural proofs 1994, algebrization 2008) **prove** that no purely empirical or simulation-based technique can settle the question. A `SUPPORTED at n ≤ 20` verdict has zero predictive value for asymptotic behavior. **The 22-day zero-SUPPORTED streak is not a bug; it is the question's signature.**

### 4.4 The framework engine is a structured-prompt wrapper, not a mathematical engine
`Framework.primitives`, `.operations`, `.target_invariant`, `.axioms_tentative` are typed but un-schema'd dicts. Nothing operates on them; they are only fed back to the LLM elaborator. A framework is, structurally, a fancy prompt template. There is no formal language, no type-checking, no inference.

### 4.5 The verdict ontology is wrong for the goal
`SUPPORTED | FALSIFIED | INCONCLUSIVE | BARRIER_HIT | SCOOPED` reflects an empirical-science mindset. For P-vs-NP-style results, the relevant labels are: `formally proven` | `disproven via specific construction` | `reduced to (named open problem)` | `excluded by (named barrier)` | `unknown`. The closest analogue (`BARRIER_HIT`) is a strict prefilter, not a verdict.

### 4.6 No accumulation of mathematical understanding
`tester_known_pitfalls.txt` accumulates **engineering** lessons (don't use `math.log(0)`, etc.). The pitfall file grew 13 → 81 in 2 days post-fix. But the system has **no analogous file for mathematical lessons**: "the random-restriction approach to AC^0[2] hits this specific obstruction", "Razborov's lower bound for monotone clique requires this construction". After 6 weeks of operation, the math-knowledge state of the engine is the same as week 1.

### 4.7 Self-improvement is on code, not on math
`self_improve.py` (863 LOC) is a ReAct loop that modifies the agent's Python source — bug-fix style. It does not extend a theorem database, refine a proof strategy, or update beliefs about which complexity-theoretic approaches are viable. The agent gets better at running, not at thinking.

### 4.8 The data model is layered chaos
`NotebookEntry` has 31 fields tagged across 4 milestones (T1/T2/T3/F1-4 + Skeptic + Focus). Each was added forward-only. The result: most fields are empty in most entries; consumers must defensively check; the schema does not reflect any coherent model of "an experiment", it reflects the engine's deployment history.

### 4.9 Human-in-the-loop is post-hoc only
Ludo's intervention modes are: (i) `retractions.json` (post-publication audit), (ii) reading reports (passive), (iii) restarting / patching code (operational). The proposer, judge, and skeptic operate without him. The Monday `review_alert` digest is the only push toward him, and it is a summary of what was already decided. **No question is posed to him at decision points** ("should I pursue this strategy? this conjecture?").

### 4.10 The MULTIAGENT_PIPELINE is paper-only
The 5-gate design in `MULTIAGENT_PIPELINE.md` (AUDITOR, MATHEMATICIAN, LITERATURE_SCOUT, LEAN_FORMALIZER, ROYAL_SOCIETY) is the explicit plan to add rigor. But it is **not wired into the runtime**. It exists as a markdown document; the only runtime gate is the 4-layer skeptic, which only fires on the (never-occurring) `SUPPORTED` branch.

---

## 5. Design space for L3 redesign

Given the goal is P-vs-NP and given the critique above, an L3 redesign has these orthogonal axes. Each axis has multiple choices; they cross-product, but some combinations are coherent and others are not.

### 5.1 Axis A — The atom of work

What is the unit the engine reasons about?
- **A1 — Conjecture** (current). A natural-language statement with `field_A × field_B` framing.
- **A2 — Theorem in Lean** (formal). A `theorem T : Prop` and a partial proof tree.
- **A3 — Lemma chain**. A directed graph of statements, each depending on earlier ones, with proof obligations as edges.
- **A4 — Strategy / research program**. A plan attacking a specific named open problem, with sub-goals and known obstacles.
- **A5 — Tactic application**. A single Lean tactic on a goal, accumulating into proof attempts.

### 5.2 Axis B — Knowledge representation

Where does "what we know" live?
- **B1 — Append-only JSONL logs** (current). No index. Read-as-LLM-context only.
- **B2 — Indexed graph database** (Neo4j, etc.) of mathematical objects and relationships.
- **B3 — Lean mathlib + custom extension**. Reuse the existing mathlib infrastructure as the KB.
- **B4 — RDF/Datalog triple store** of complexity-theory facts.
- **B5 — Vector store** of paper abstracts + theorem statements (an inflated RAG).

### 5.3 Axis C — Reasoning paradigm

How does the engine produce new content?
- **C1 — LLM proposes, LLM tests, LLM judges** (current).
- **C2 — Goal-directed proof search** (Lean automation: tactics + LLM-guided tree search, à la AlphaProof, ReProver).
- **C3 — Knowledge-graph traversal**: starting from a node (theorem T), explore adjacent edges (lemmas it depends on; lemmas that depend on it) to find unblock points.
- **C4 — Blackboard architecture**: many specialist agents (lower-bound prover, upper-bound finder, barrier checker, literature scout) post hypotheses on a shared board; controller selects what to advance.
- **C5 — Adversarial dyad**: prover + disprover argue over a target; the controller awards points and prunes.

### 5.4 Axis D — Human-in-the-loop topology

When is Ludo (or any human) involved?
- **D1 — Post-hoc audit only** (current). Retractions, paper review, code patches.
- **D2 — Strategy gate**: human approves which research direction to attack (weekly cadence).
- **D3 — Decision-point gate**: human is asked specific questions ("is this conjecture worth testing? is this proof step plausible?") on demand.
- **D4 — Pair-programming-style**: human and agent collaboratively edit Lean files.

### 5.5 Axis E — Measurement of progress

What does "doing well" look like?
- **E1 — Volume of cycles** (current implicit metric — 38 cycles/24h is celebrated).
- **E2 — Verdicts emitted** (current explicit metric — # SUPPORTED).
- **E3 — Theorems formalized in Lean** (a `lean_verified/` count that actually counts non-trivial formalizations).
- **E4 — Lemmas added to a shared KB** (cumulative knowledge growth).
- **E5 — Papers cited** by external work (long horizon, but ultimately the right metric).
- **E6 — Specific open problems advanced** (1 metric per problem: depth of attack, obstacles ruled out).

### 5.6 Some coherent paths through the design space

**Path α — "Lean-native engine"** (closest to AlphaProof / ReProver):
A2 + B3 + C2 + D4 + E3. Atoms are Lean theorems; KB is mathlib; reasoning is tactic-search; human pair-programs; progress is mathlib contributions.

**Path β — "Knowledge-graph engine"**:
A3 + B2 + C3 + D3 + E4. Atoms are lemmas in a graph; KB is the graph; reasoning traverses the graph; human is queried at decision points; progress is graph growth.

**Path γ — "Strategy-driven engine"**:
A4 + B2 + C4 + D2 + E6. Atoms are research strategies; KB indexes complexity-theory facts; multiple agents work the strategy on a blackboard; human approves strategy choice; progress is depth on named problems.

**Path δ — "Current with discipline added"**:
A1 + B1 + C1 + D2 + E2/E3. Keep the current architecture but: (i) ground the proposer in a specific research program selected weekly by Ludo, (ii) require Lean formalization for any SUPPORTED to count.

### 5.7 Notes on path choice

- **α** is the lowest-risk, highest-realism path. It is what the field is converging to. It requires throwing away most of the current proposer/judge/skeptic and replacing with tactic-search. But it can reuse the existing Lean infrastructure (`pvsnp_lean_gate`, `lean_verified/`, mathlib on disk).
- **β** is the most ambitious knowledge-engineering path. It requires building (or licensing) a structured KB of complexity theory. High up-front cost.
- **γ** is the most "research-y" path — closest to how humans do this work. But it has the highest variance in outcome because "strategy" is hard to operationalize.
- **δ** is the cheapest. It does not move the needle on P-vs-NP but recovers most of the sunk cost of the current system.

---

## 6. What the next session should produce

This document maps the AS-IS. The next session — when you are ready — should produce the **TARGET architecture**: which path (α/β/γ/δ or hybrid), which atoms, which KB, which reasoning paradigm. After that, a **migration plan**: what stays, what gets thrown away, what gets refactored, in what order.

To prepare, before our next session it would help if you decide:
1. **Are you willing to throw away substantial code?** (α and β require throwing away the proposer/judge/skeptic; γ keeps more; δ keeps almost everything.)
2. **Is Lean acceptable as the lingua franca?** (α and β almost require it.)
3. **Are you willing to be in the loop at strategy/decision points?** (D2/D3 require this; D1 keeps the current 24/7-autonomous mode.)

If you want, before that session I can also produce: (i) a deeper read of one specific subsystem you suspect (just point), (ii) a survey of comparable systems (AlphaProof, ReProver, Lean Copilot, Trinity, Magnushammer) for reference, (iii) a quantitative cost estimate (LOC to throw, LOC to write, calendar weeks).

---

*This document is committed at `audit/architecture/AS_IS.md` in the SperimentalMath repo. It is intended as a stable reference for the L3 redesign conversation. It will be updated only on significant architectural change; the live operational state remains in `STATUS.md` and `OPERATIONAL_STATUS.md`.*
