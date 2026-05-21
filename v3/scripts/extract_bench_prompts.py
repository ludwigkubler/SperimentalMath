#!/usr/bin/env python3
"""Extract real prompts from SEC audit log to use as benchmark inputs."""

import json
from pathlib import Path

logs = [
    Path("/home/ludo/Scrivania/SEC/research/audit/_global-2026-05-19.jsonl"),
    Path("/home/ludo/Scrivania/SEC/research/audit/_global.jsonl"),
]

# Sample one prompt per phase
samples = {}
for log in logs:
    if not log.exists():
        continue
    with log.open() as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            phase = e.get("phase", "?")
            if phase in samples:
                continue  # only one per phase
            if not e.get("system_prompt") or not e.get("user_prompt"):
                continue
            samples[phase] = {
                "phase": phase,
                "provider": e.get("provider", "?"),
                "model": e.get("model", "?"),
                "system_prompt": (e.get("system_prompt") or "")[:6000],
                "user_prompt": (e.get("user_prompt") or "")[:6000],
                "system_prompt_len": len(e.get("system_prompt") or ""),
                "user_prompt_len": len(e.get("user_prompt") or ""),
            }

print(f"Distinct phases sampled: {len(samples)}")
for phase, data in samples.items():
    p = data["provider"]
    m = data["model"]
    spl = data["system_prompt_len"]
    upl = data["user_prompt_len"]
    print(f"  phase={phase!r:20s} provider={p:15s} model={m:30s}")
    print(f"    system_prompt: {spl} chars  user_prompt: {upl} chars")

out = Path("/tmp/benchmark_prompts.json")
out.write_text(json.dumps(samples, indent=2))
print(f"\nSaved to {out}")
print(f"\nWill benchmark these phases: {sorted(samples.keys())}")
