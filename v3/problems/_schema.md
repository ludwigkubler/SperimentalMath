# Problem Portfolio — TOML Schema

Every `problems/<problem_id>.toml` file in this directory MUST conform to the schema below. The schema is enforced at load time by `v3/portfolio/loader.py` (Pydantic v2 strict mode).

Companion: every TOML file is paired with `problems/<problem_id>.lean` containing the formal statement (Lean 4, no Mathlib).

---

## Top-level fields (required)

```toml
problem_id     = "SCREAMING_SNAKE_CASE_WITH_REF"  # e.g. MONO_CLIQUE_RAZBOROV_85
title          = "Short, citable title"          # ≤80 chars
field          = "circuit_lb"                     # enum: see below
status         = "active"                         # enum: see below
curated_by     = "Ludovico Kubler"
last_reviewed  = 2026-05-19
```

### `field` enum
- `circuit_lb`              — circuit lower bounds (AC^0, monotone, formula depth, …)
- `communication_complexity`
- `proof_complexity`        — resolution width, Frege, cutting planes, …
- `sat_hardness`            — random k-SAT, planted clique, …
- `barrier_theory`          — relativization, naturalization, algebrization
- `fine_grained`            — 3-SUM, OV, APSP, fine-grained reductions
- `algebraic_complexity`    — VP/VNP, permanent vs determinant, GCT
- `derandomization`         — PRGs, BPP vs P, …

### `status` enum
- `active`                  — currently in our portfolio for attacks
- `frozen`                  — not currently attacking but kept for reference
- `resolved`                — open question got settled by external work
- `abandoned`               — we decided this is not a productive direction

---

## Sub-tables

### `[statement]` (required)
```toml
[statement]
markdown   = """
≤500 words, plain markdown. State the problem clearly. Use \\(...\\) for
inline math, \\[...\\] for display math. Pandoc-compatible.
"""
lean_file  = "MONO_CLIQUE_RAZBOROV_85.lean"   # relative to this dir
```

### `[significance_to_pvsnp]` (required)
```toml
[significance_to_pvsnp]
text = """
≤300 words. Why does this question matter for P vs NP specifically?
Be precise: does a positive answer prove P ≠ NP? Does it close a gap that
P vs NP depends on? Does it resolve a barrier?
"""
```

### `[[known_bounds]]` (1+ instances)
```toml
[[known_bounds]]
type            = "lower"                # lower | upper | equality
parameter       = "k"                    # what's being bounded
value_expr      = "n^Omega(k)"           # LaTeX-free expression
range_valid     = "k ≤ (log n)^(1/2)"
reference_key   = "alon_boppana_1987"    # FK to canonical_references
notes           = "..."                  # optional
```

### `[[known_barriers]]` (0+ instances)
```toml
[[known_barriers]]
name            = "natural_proofs"       # relativization|natural_proofs|algebrization|other
caveat          = "Monotone bounds escape NP-natural; this question is below the barrier."
reference_key   = "razborov_rudich_1997" # optional, FK
```

### `[[canonical_references]]` (3+ instances required)
```toml
[[canonical_references]]
key      = "razborov_1985"
title    = "Lower bounds on monotone complexity of the logical permanent"
authors  = ["A. A. Razborov"]
year     = 1985
arxiv_id = "" # one of {arxiv_id, doi, isbn} required (else exempt as folklore)
doi      = "10.1070/SM1985v050n01ABEH002825"
isbn     = "" # for monographs without DOI
venue    = "Mathematics of the USSR-Sbornik"
notes    = ""
```

### `[[open_subquestions]]` (1+ instances required)
The actionable units. These are what Strategies are proposed against.
```toml
[[open_subquestions]]
id                = "sub1"
text              = "Specific, falsifiable question."
suggested_attack  = "1-2 sentence sketch of an experimental approach."
estimated_compute = "feasible on RTX 3070 Ti within hours"  # rough sanity
status            = "open"   # open | in_progress | resolved | dropped
```

---

## Validation rules

1. `problem_id` MUST match the filename: `<problem_id>.toml`
2. `statement.lean_file` MUST exist next to the TOML
3. Every `reference_key` in `known_bounds.reference_key` and `known_barriers.reference_key` MUST exist in `canonical_references`
4. Every `[[canonical_references]]` MUST have at least one of `arxiv_id`, `doi`, `isbn`
5. `last_reviewed` MUST be within the last 90 days of the load time (else load fails — forces periodic refresh)

---

## Curation discipline

- Each Problem is curated from canonical sources (Allender's surveys, Razborov-Rudich, Aaronson's chapters, Williams' algorithmic-method paper, the Complexity Zoo).
- Citations are double-checked: every DOI must resolve; every arXiv ID must exist.
- `[VERIFY]` is a special marker used inline during drafting; it MUST NOT remain in a committed file. If present at load time, the loader fails.

---

*This schema is intentionally restrictive. The point of the Problem Portfolio is to be the engine's institutional memory — its accuracy determines what Strategies the system can validly propose. A loose schema would let LLM hallucination back in.*
