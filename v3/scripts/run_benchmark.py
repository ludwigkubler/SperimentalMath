#!/usr/bin/env python3
"""Benchmark local Ollama models on real SEC explorer prompts.

For each (model, task) pair: send the real system+user prompt, measure
latency and token count, save output for offline quality grading.

Usage:
  python3 run_benchmark.py
  python3 run_benchmark.py --models qwen3:8b deepseek-r1:8b glm4:latest
  python3 run_benchmark.py --tasks test_gen propose judge
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROMPTS_FILE = Path("/tmp/benchmark_prompts.json")
RESULTS_FILE = Path("/tmp/benchmark_results.json")
OLLAMA_HOST = "http://localhost:11434"

DEFAULT_MODELS = [
    "qwen3:8b",                # current reasoning baseline
    "qwen2.5-coder:7b",        # current coding baseline
    "deepseek-r1:8b",          # alternative reasoning (already installed)
    "glm4:latest",             # new candidate
    "command-r7b:latest",      # new candidate (Cohere)
    "mistral-nemo:latest",     # new candidate (12B)
    "phi4:latest",             # new candidate (Microsoft 14B, may not fit)
]

DEFAULT_TASKS = ["test_gen", "propose", "judge"]

# Per-task generation parameters. Output capped to limit benchmark time.
TASK_PARAMS = {
    "test_gen":        {"temperature": 0.3, "num_predict": 1200, "num_ctx": 8192},
    "propose":         {"temperature": 0.7, "num_predict": 800,  "num_ctx": 16384},
    "judge":           {"temperature": 0.1, "num_predict": 400,  "num_ctx": 8192},
    "critic":          {"temperature": 0.3, "num_predict": 500,  "num_ctx": 8192},
    "novelty":         {"temperature": 0.3, "num_predict": 400,  "num_ctx": 8192},
    "preregistration": {"temperature": 0.3, "num_predict": 400,  "num_ctx": 8192},
}


def call_ollama(model: str, system_prompt: str, user_prompt: str,
                temperature: float, num_predict: int, num_ctx: int,
                timeout: int = 240) -> dict:
    """Call Ollama /api/generate with /api/chat-style messages.
    Returns dict with latency_s, output, error, tokens."""
    payload = {
        "model": model,
        "prompt": user_prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "num_ctx": num_ctx,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read())
        elapsed = time.monotonic() - t0
        return {
            "latency_s": round(elapsed, 2),
            "output": body.get("response", ""),
            "output_len_chars": len(body.get("response", "")),
            "eval_count": body.get("eval_count"),
            "eval_duration_ns": body.get("eval_duration"),
            "tokens_per_sec": round(
                (body.get("eval_count", 0) * 1e9) /
                max(1, body.get("eval_duration", 1)), 1
            ),
            "error": None,
            "done_reason": body.get("done_reason", "?"),
        }
    except urllib.error.HTTPError as e:
        return {"latency_s": round(time.monotonic() - t0, 2),
                "output": "", "output_len_chars": 0, "eval_count": None,
                "eval_duration_ns": None, "tokens_per_sec": None,
                "error": f"HTTPError {e.code} {e.reason}: {e.read()[:200].decode('utf-8', 'replace')}",
                "done_reason": "error"}
    except Exception as e:
        return {"latency_s": round(time.monotonic() - t0, 2),
                "output": "", "output_len_chars": 0, "eval_count": None,
                "eval_duration_ns": None, "tokens_per_sec": None,
                "error": f"{type(e).__name__}: {e}",
                "done_reason": "error"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    ap.add_argument("--tasks", nargs="+", default=DEFAULT_TASKS)
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()

    if not PROMPTS_FILE.exists():
        print(f"ERROR: {PROMPTS_FILE} not found. Run extract_bench_prompts.py first.")
        return 2
    prompts = json.loads(PROMPTS_FILE.read_text())

    # Validate
    for t in args.tasks:
        if t not in prompts:
            print(f"WARN: task {t!r} not in prompts file; skipping")
    tasks = [t for t in args.tasks if t in prompts]

    results = {}
    total = len(args.models) * len(tasks)
    n = 0
    for task in tasks:
        prompt_data = prompts[task]
        params = TASK_PARAMS.get(task, TASK_PARAMS["judge"])
        results[task] = {}
        for model in args.models:
            n += 1
            print(f"[{n}/{total}] model={model:30s} task={task:18s}  "
                  f"sys={prompt_data['system_prompt_len']:>5} "
                  f"user={prompt_data['user_prompt_len']:>5} ...",
                  end="", flush=True)
            r = call_ollama(
                model=model,
                system_prompt=prompt_data["system_prompt"],
                user_prompt=prompt_data["user_prompt"],
                temperature=params["temperature"],
                num_predict=params["num_predict"],
                num_ctx=params["num_ctx"],
                timeout=args.timeout,
            )
            results[task][model] = r
            if r["error"]:
                print(f" ERROR: {r['error'][:80]}")
            else:
                tps = r["tokens_per_sec"]
                tok = r["eval_count"]
                print(f" {r['latency_s']:>6.1f}s  {tok} tok  {tps} tok/s")

    RESULTS_FILE.write_text(json.dumps(results, indent=2))
    print(f"\nSaved {RESULTS_FILE}")

    # Print summary table
    print("\n=== LATENCY (s) ===")
    print(f"{'task':<18}", end="")
    for m in args.models:
        print(f"{m:>22}", end="")
    print()
    for task in tasks:
        print(f"{task:<18}", end="")
        for m in args.models:
            r = results[task].get(m, {})
            if r.get("error"):
                print(f"{'ERR':>22}", end="")
            else:
                print(f"{r.get('latency_s', '?'):>22}", end="")
        print()

    print("\n=== TOKENS / SEC ===")
    print(f"{'task':<18}", end="")
    for m in args.models:
        print(f"{m:>22}", end="")
    print()
    for task in tasks:
        print(f"{task:<18}", end="")
        for m in args.models:
            r = results[task].get(m, {})
            if r.get("error") or r.get("tokens_per_sec") is None:
                print(f"{'-':>22}", end="")
            else:
                print(f"{r['tokens_per_sec']:>22}", end="")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
