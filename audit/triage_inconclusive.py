"""Triage of the INCONCLUSIVE entries in pvsnp_notebook.jsonl.

Reads from a local copy fetched via scp; classifies entries by:
  - crash type (Python error class)
  - novelty depth
  - output length / signal density

Emits:
  - top crash causes
  - top-20 non-crashing INCONCLUSIVE candidates worth re-test
  - a JSON summary file for the paper
"""

import json
import re
from collections import Counter
from pathlib import Path

NOTEBOOK = Path("/tmp/sperimental_audit/pvsnp_notebook.jsonl")

crash_patterns = Counter()
non_crash = []
crashed_with_titles = []

with NOTEBOOK.open() as f:
    for line in f:
        try:
            e = json.loads(line)
        except Exception:
            continue
        v = e.get("final_verdict") or e.get("phase", "?")
        if v != "INCONCLUSIVE":
            continue
        stdout = e.get("test_stdout") or ""
        stderr = e.get("test_stderr") or ""
        rc = e.get("test_returncode", -1)
        is_crash = (rc != 0) or ("Traceback" in stdout + stderr)
        if is_crash:
            m = re.search(r"([A-Za-z]+(?:Error|Exception|Warning)): (.{0,200})",
                          stdout + "\n" + stderr)
            if m:
                err_type = m.group(1)
                err_msg = m.group(2).strip()
                crash_patterns[err_type] += 1
                crashed_with_titles.append({
                    "entry_id": e.get("entry_id"),
                    "title": e.get("title") or "",
                    "error_type": err_type,
                    "error_msg": err_msg[:80],
                    "novelty_hits": len(e.get("novelty_hits", [])),
                })
            else:
                crash_patterns["_unknown_nonzero_rc"] += 1
        else:
            non_crash.append({
                "entry_id": e.get("entry_id"),
                "title": e.get("title") or "",
                "field_A": e.get("field_A", ""),
                "field_B": e.get("field_B", ""),
                "statement": (e.get("statement") or "")[:300],
                "novelty_hits": len(e.get("novelty_hits", [])),
                "stdout_len": len(stdout),
                "elapsed": e.get("test_elapsed_s", 0),
                "final_reason": (e.get("final_reason") or "")[:200],
                "ts": e.get("ts"),
            })

print(f"INCONCLUSIVE total: {len(non_crash) + sum(crash_patterns.values())}")
print(f"  crashed: {sum(crash_patterns.values())}")
print(f"  non-crashing: {len(non_crash)}")
print()
print("=== Top crash causes ===")
for k, v in crash_patterns.most_common(20):
    print(f"  {v:>4}  {k}")
print()

# Rank non-crashing by:
#  - novelty_hits (more = better, real arXiv signal)
#  - stdout_len (more = real output)
#  - elapsed (must be > 0.5s, signals real computation)
def score(r):
    novelty = min(r["novelty_hits"], 15) / 15.0
    output = min(r["stdout_len"], 5000) / 5000.0
    runtime = 1.0 if r["elapsed"] > 0.5 else r["elapsed"] / 0.5
    return 0.5 * novelty + 0.3 * output + 0.2 * runtime

non_crash.sort(key=score, reverse=True)

print(f"=== Top 25 non-crashing INCONCLUSIVE (ranked) ===")
for r in non_crash[:25]:
    s = score(r)
    print(f"  score={s:.3f} nov={r['novelty_hits']:>2} elap={r['elapsed']:>5.1f}s "
          f"out={r['stdout_len']:>4}  {r['entry_id']}: {r['title'][:75]}")

# crash-cause breakdown by error type with top affected entry
print()
print("=== Sample crashed entries by top error types ===")
for err_type, _ in crash_patterns.most_common(8):
    print(f"\n--- {err_type} ---")
    sample = [c for c in crashed_with_titles if c["error_type"] == err_type][:3]
    for c in sample:
        print(f"  {c['entry_id']}: {c['title'][:60]}")
        print(f"      msg: {c['error_msg']}")

out = {
    "n_inconclusive_total": len(non_crash) + sum(crash_patterns.values()),
    "n_crashed": sum(crash_patterns.values()),
    "n_non_crash": len(non_crash),
    "top_crash_causes": dict(crash_patterns.most_common(20)),
    "top_25_non_crash_candidates": non_crash[:25],
}
out_path = Path("/tmp/sperimental_audit/inconclusive_triage.json")
out_path.write_text(json.dumps(out, indent=2))
print(f"\nsaved: {out_path}")
