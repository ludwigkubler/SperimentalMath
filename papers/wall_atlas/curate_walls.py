"""Curate the 32 raw barrier rejections into the canonical Wall Atlas:
group by conjecture title, keep only one entry per unique (title, barrier) pair,
and emit a clean JSON+Markdown table for the paper.
"""
import json
from pathlib import Path
from collections import defaultdict

bar_files = ["algebrization", "karp_lipton", "natural_proofs", "relativization"]
all_rec = []
for b in bar_files:
    p = Path(f"/tmp/sperimental_audit/{b}.jsonl")
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        all_rec.append(rec)

print(f"raw records: {len(all_rec)}")

# Group by conjecture title (case-insensitive)
by_title = defaultdict(list)
for r in all_rec:
    title = r["conjecture"]["title"].strip()
    by_title[title].append(r)

print(f"unique titles: {len(by_title)}")

# For each unique title, pick the rejection with the highest combined_confidence
# and the most-frequent barrier among hits for that title
canonical = []
for title, recs in by_title.items():
    # primary barrier = mode of barrier across records
    barrier_counts = defaultdict(int)
    for r in recs:
        barrier_counts[r["barrier"]] += 1
    primary = max(barrier_counts, key=barrier_counts.get)
    primary_recs = [r for r in recs if r["barrier"] == primary]
    # representative = highest combined_confidence
    rep = max(primary_recs, key=lambda x: x.get("combined_confidence", 0))
    canonical.append({
        "title": title,
        "primary_barrier": primary,
        "rejection_count": len(recs),
        "max_confidence": rep.get("combined_confidence"),
        "field_A": rep["conjecture"].get("field_A", ""),
        "field_B": rep["conjecture"].get("field_B", ""),
        "statement": rep["conjecture"].get("statement", ""),
        "rationale": rep["conjecture"].get("rationale", ""),
        "barrier_count_breakdown": dict(barrier_counts),
        "llm1_reasoning_excerpt": (rep.get("llm1_reasoning") or "")[:500],
        "llm2_reasoning_excerpt": (rep.get("llm2_reasoning") or "")[:500],
        "ts": rep.get("ts"),
    })

# sort by primary_barrier then by max_confidence desc
canonical.sort(key=lambda x: (x["primary_barrier"], -x["max_confidence"]))

print(f"\nCanonical entries: {len(canonical)}")
print()
print("=== By barrier ===")
by_bar = defaultdict(list)
for c in canonical:
    by_bar[c["primary_barrier"]].append(c)
for b in sorted(by_bar):
    print(f"\n{b}:")
    for c in by_bar[b]:
        print(f"  conf={c['max_confidence']:.2f} reps={c['rejection_count']:>2}  {c['title'][:80]}")

# write JSON
out_path = Path("/tmp/sperimental_audit/wall_atlas_curated.json")
out_path.write_text(json.dumps({
    "n_raw_records": len(all_rec),
    "n_unique_conjectures": len(canonical),
    "entries": canonical,
}, indent=2))
print(f"\nsaved: {out_path}")
