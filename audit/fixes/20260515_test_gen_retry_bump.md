# Fix — test-gen retry loop bump (2026-05-15)

**Author:** Ludovico Kubler (with Claude)
**File touched:** `pvsnp_explorer.py` (both copies: `~/Scrivania/SEC/src/research/` and `~/kissat/pvnp_lab/system_v2/src/` — they were byte-identical pre-edit, see audit/code_integrity/SUMMARY.md D4 + #3)
**Sentinel:** `sec_test_gen_retry_bump_v1`
**Backup:** `pvsnp_explorer.py.bak.20260514_223044` in both directories

## Problem (diagnosed 2026-05-15)

`health_report.json:skeptic_168h.not_invoked = 418` was flagged by the 2026-05-13 audit as a possible bug. Investigation shows the skeptic gate is working as designed — it only fires when `verdict == "SUPPORTED"`, and **zero of the 453 entries in `notebook/2026-05.jsonl` reached SUPPORTED**. The real anomaly is upstream: the engine has produced zero positive results in 6+ weeks.

Breakdown of the 442 INCONCLUSIVE entries (2026-05 month-to-date):

| Cause | Count | % | Source |
|:------|------:|--:|:-------|
| Test code crash at runtime (rc != 0, no seeds) | **294** | **67%** | LLM-generated test has bugs |
| Test timeout (rc=124, 240s wall-clock hit) | 76 | 17% | Method too slow |
| rc=0 but judge said INCONCLUSIVE | 68 | 15% | Often "n=1 too small" |
| Safety rail SUPPORTED→INCONCLUSIVE | 17 | 4% | (working as designed) |
| Judge output parse_fail | 16 | 4% | LLM verdict unparseable |

Bottleneck = **67% of cycles produce zero scientific value because LLM-generated Python crashes at first execution**.

Retry budget: `generate_and_run_test_with_retry(max_retries=1)` — only ONE retry. After a single failure-then-retry, the entry is logged as INCONCLUSIVE.

Pitfall learning: `_record_pitfall` was called **only on successful recovery** (line 956 pre-fix). Terminal failures (the dominant outcome) contributed nothing to the pitfall file, which had accumulated only 13 entries since April despite hundreds of crashes.

## Fix

Three minimal changes, all in `pvsnp_explorer.py`:

### Change 1 — bump `max_retries` from 1 to 3

```diff
 async def generate_and_run_test_with_retry(
     provider, conj: dict, criterion: str = "",
-    max_retries: int = 1,
+    max_retries: int = 3,
 ) -> ...
```

And at the call site (Phase 4 in `run_one_cycle`):

```diff
     (code, stdout, rc, telapsed, seed_results, agg,
      gen_history) = await generate_and_run_test_with_retry(
-        provider, conj, criterion=prereg.get("criterion", ""), max_retries=1,
+        provider, conj, criterion=prereg.get("criterion", ""), max_retries=3,
     )
```

Now: 4 total attempts (1 initial + 3 retries). LLM gets to see the error from each crash and try a corrected version.

### Change 2 — record pitfalls on terminal failure, not only on recovery

```python
# All retries exhausted. Still record the pitfall so the next session
# learns the failure mode even though this entry didn't recover.
if last_error_for_llm and rc != 0:
    summary = last_error_for_llm.strip().split("\n")[-1][:200]
    _record_pitfall(summary, pattern_hint=f"terminal failure after {max_retries+1} attempts")
return code, stdout, rc, elapsed, seed_results, agg, history
```

Effect: every distinct crash mode now appears in `~/Scrivania/SEC/research/tester_known_pitfalls.txt` and is injected into the prompt for the next conjecture. The pitfall list will grow from 13 → many faster, and the LLM stops repeating the same crashes.

### Change 3 — strengthen TESTER_SYSTEM prompt with anti-patterns (j) and (k)

Added to the failure-mode block in the system prompt:

```
(j) Sub-asymptotic n. For ANY size-dependent claim, n_min >= 5 and
    n_max >= 20 are required. n=1 is allowed ONLY when the conjecture
    is about trivial-case enumeration (rare). The judge will downgrade
    any "all trials used n=1" result to INCONCLUSIVE without warning.
    Sweep n through at least 4 distinct sizes inside each trial.

(k) Wall-clock self-abort. The sandbox hard-kills at ~240s. If your
    method estimates it will exceed 200s, exit early and print
    'RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=<k>' so the
    run is structured rather than a SIGKILL with no data.
```

Target: the 68 "n=1 too small" failures (Change 3j) and the 76 timeouts that produce no structured output (Change 3k).

## Expected impact

Conservative estimate (single cycle, no other interventions):

- Pre-fix: 294/442 INCONCLUSIVE were crashes. With max_retries=3, even a 30% recovery rate per additional retry recovers ~150 of those. Net: ~150 entries that previously contributed nothing now reach the judge with real data.
- Pre-fix: 68 entries downgraded for n=1. Change 3j should cut this by ~50%.
- Pitfall file growth: from 13 to ~50–100 within a week of operation (cross-session memory).
- Compute cost: more LLM calls per failed cycle (worst case 4× vs 2× for the test-gen stage). Mitigated by the fact that most cycles still succeed on attempt 1 or 2; only the hard ones use the full retry budget.

## How to validate

1. After ~24 hours of operation, recompute the INCONCLUSIVE breakdown on `notebook/2026-05.jsonl` post-2026-05-15. Expect `crash` bucket to drop from 67% → 30-40%.
2. Check `~/Scrivania/SEC/research/tester_known_pitfalls.txt` line count. Expect growth from 13.
3. Watch for the first non-zero `SUPPORTED` or `FALSIFIED` entry in `notebook/`. This is the real metric — the engine should start producing scientific output again.

## Rollback

```bash
TS=20260514_223044
cp ~/Scrivania/SEC/src/research/pvsnp_explorer.py.bak.${TS} ~/Scrivania/SEC/src/research/pvsnp_explorer.py
cp ~/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.py.bak.${TS} ~/kissat/pvnp_lab/system_v2/src/pvsnp_explorer.py
```

No restart needed: `pvsnp_explorer.py` is loaded fresh per cycle by `pvsnp_monitor`.

## Open issue tracked elsewhere

- **Two divergent copies of `pvsnp_explorer.py`** (audit/code_integrity D4): both were patched here, but they should be consolidated into a shared module. Until that refactor, every fix has to be applied twice. Tracked.
- **Skeptic gate**: untouched. It's working as designed. The 405/418 "not_invoked" counter is a metric about gate firing, not a bug. Documented in `audit/code_integrity/`.
