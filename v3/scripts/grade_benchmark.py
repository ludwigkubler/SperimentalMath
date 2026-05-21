#!/usr/bin/env python3
"""Structural-grading of benchmark outputs.

For each task, applies task-specific structural rules to score each
model's output. This grading is FAST and OBJECTIVE — no LLM judge
required (which would be subjective and slow).

Rules per task:

- test_gen: Python code generation. Scoring:
    +30 has ```python fenced block
    +20 ast.parse() succeeds
    +20 defines run_trial(seed) function
    +10 has `RESULT:` line
    +10 has `TRIAL:` print
    +10 imports only stdlib (no numpy/scipy/sympy/networkx/sklearn/torch)
    -50 contains forbidden imports

- propose: JSON conjecture output. Scoring:
    +30 contains a fenced ```json block (or pure JSON)
    +30 json.loads parses
    +20 has required keys: title, field_A, field_B, statement, rationale, test_strategy
    +10 title length 30-200 chars
    +10 statement contains math/symbol marker (e.g. ∀, ∃, ≥, ≤, ∈)

- judge: JSON verdict. Scoring:
    +40 json.loads parses
    +30 has verdict field with one of SUPPORTED/FALSIFIED/INCONCLUSIVE
    +20 has reason field
    +10 has next_direction field

Also records: latency, tokens/sec, output length.
"""

import argparse
import ast
import json
import re
import sys
from pathlib import Path

RESULTS_FILE = Path("/tmp/benchmark_results.json")
GRADES_FILE = Path("/tmp/benchmark_grades.json")

FORBIDDEN_IMPORTS = {
    "numpy", "scipy", "sympy", "networkx", "sklearn", "torch", "pandas",
    "matplotlib", "igraph", "galois", "cvxpy", "polymake",
}


def extract_python_code(text: str) -> str | None:
    m = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1)
    # Try without fence
    if "def run_trial" in text and "RESULT:" in text:
        return text
    return None


def extract_json_block(text: str) -> str | None:
    # Try fenced first
    m = re.search(r"```(?:json)?\s*\n(\{.*?\})\s*\n```", text, re.DOTALL)
    if m:
        return m.group(1)
    # Try the largest brace-balanced span
    candidates = []
    starts = [i for i, c in enumerate(text) if c == "{"]
    for s in starts:
        depth = 0
        for i in range(s, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    candidates.append(text[s:i + 1])
                    break
    if candidates:
        return max(candidates, key=len)
    return None


def grade_test_gen(output: str) -> tuple[int, list[str]]:
    score = 0
    notes = []
    code = extract_python_code(output)
    if not code:
        notes.append("FAIL: no python code block")
        return 0, notes
    score += 30
    notes.append("OK: has python block (+30)")
    try:
        tree = ast.parse(code)
        score += 20
        notes.append("OK: ast.parse (+20)")
        # Check for run_trial
        has_run_trial = any(
            isinstance(n, ast.FunctionDef) and n.name == "run_trial"
            for n in ast.walk(tree)
        )
        if has_run_trial:
            score += 20
            notes.append("OK: defines run_trial (+20)")
        else:
            notes.append("FAIL: no run_trial def")
        # Check imports
        used_imports = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for alias in n.names:
                    used_imports.add(alias.name.split(".")[0])
            elif isinstance(n, ast.ImportFrom) and n.module:
                used_imports.add(n.module.split(".")[0])
        forbidden_used = used_imports & FORBIDDEN_IMPORTS
        if forbidden_used:
            score -= 50
            notes.append(f"FAIL: forbidden imports: {forbidden_used} (-50)")
        else:
            score += 10
            notes.append("OK: stdlib only (+10)")
    except SyntaxError as e:
        notes.append(f"FAIL: ast.parse SyntaxError: {e.lineno}:{e.offset}")
        return max(0, score), notes
    if "RESULT:" in code:
        score += 10
        notes.append("OK: has RESULT: line (+10)")
    if "TRIAL:" in code or "trial" in code.lower():
        score += 10
        notes.append("OK: has TRIAL marker (+10)")
    return max(0, score), notes


def grade_propose(output: str) -> tuple[int, list[str]]:
    score = 0
    notes = []
    block = extract_json_block(output)
    if not block:
        notes.append("FAIL: no JSON block")
        return 0, notes
    score += 30
    notes.append("OK: JSON block found (+30)")
    try:
        d = json.loads(block)
    except json.JSONDecodeError as e:
        notes.append(f"FAIL: json.loads: {e}")
        return score, notes
    score += 30
    notes.append("OK: json.loads parses (+30)")
    required = ["title", "field_A", "field_B", "statement", "rationale", "test_strategy"]
    missing = [k for k in required if k not in d]
    if not missing:
        score += 20
        notes.append("OK: all required keys (+20)")
    else:
        notes.append(f"PARTIAL: missing keys: {missing}")
    title = d.get("title", "")
    if isinstance(title, str) and 30 <= len(title) <= 200:
        score += 10
        notes.append(f"OK: title length {len(title)} (+10)")
    statement = d.get("statement", "")
    if isinstance(statement, str) and re.search(r"[∀∃≥≤∈∉⊆∪∩→⇒]", statement):
        score += 10
        notes.append("OK: statement has math symbol (+10)")
    return max(0, score), notes


def grade_judge(output: str) -> tuple[int, list[str]]:
    score = 0
    notes = []
    block = extract_json_block(output)
    if not block:
        notes.append("FAIL: no JSON block")
        return 0, notes
    try:
        d = json.loads(block)
    except json.JSONDecodeError as e:
        notes.append(f"FAIL: json.loads: {e}")
        return score, notes
    score += 40
    notes.append("OK: json parses (+40)")
    v = d.get("verdict", "")
    if v in {"SUPPORTED", "FALSIFIED", "INCONCLUSIVE"}:
        score += 30
        notes.append(f"OK: verdict={v} (+30)")
    else:
        notes.append(f"FAIL: verdict not standard: {v!r}")
    if d.get("reason"):
        score += 20
        notes.append("OK: has reason (+20)")
    if "next_direction" in d:
        score += 10
        notes.append("OK: has next_direction (+10)")
    return max(0, score), notes


GRADERS = {
    "test_gen": grade_test_gen,
    "propose":  grade_propose,
    "judge":    grade_judge,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, default=RESULTS_FILE)
    ap.add_argument("--out", type=Path, default=GRADES_FILE)
    args = ap.parse_args()

    if not args.results.exists():
        print(f"ERROR: {args.results} not found", file=sys.stderr)
        return 2
    results = json.loads(args.results.read_text())
    grades = {}
    for task, model_outputs in results.items():
        grader = GRADERS.get(task)
        if grader is None:
            continue
        grades[task] = {}
        for model, r in model_outputs.items():
            if r.get("error"):
                grades[task][model] = {
                    "score": -1, "notes": [f"ERROR: {r['error'][:100]}"],
                    "latency_s": r.get("latency_s"),
                    "tokens_per_sec": r.get("tokens_per_sec"),
                    "eval_count": r.get("eval_count"),
                }
                continue
            score, notes = grader(r.get("output", ""))
            grades[task][model] = {
                "score": score,
                "notes": notes,
                "latency_s": r.get("latency_s"),
                "tokens_per_sec": r.get("tokens_per_sec"),
                "eval_count": r.get("eval_count"),
                "output_len_chars": r.get("output_len_chars"),
            }
    args.out.write_text(json.dumps(grades, indent=2))
    print(f"Grades saved to {args.out}\n")

    # Print summary
    models = sorted({m for t in grades.values() for m in t})
    tasks = sorted(grades.keys())
    print("=" * 78)
    print(f"{'task':<14} {'model':<26} {'score':>6}  {'lat (s)':>8}  {'tok/s':>7}")
    print("-" * 78)
    for task in tasks:
        for model in models:
            g = grades[task].get(model)
            if not g:
                continue
            print(f"{task:<14} {model:<26} {g['score']:>6}  "
                  f"{(g['latency_s'] or 0):>8.1f}  "
                  f"{(g['tokens_per_sec'] or 0):>7.1f}")
    print()
    # Per-task winner
    print("\n=== Per-task WINNERS (by score, tie-break by tok/s) ===")
    for task in tasks:
        ranking = sorted(
            grades[task].items(),
            key=lambda kv: (-kv[1]["score"], -(kv[1].get("tokens_per_sec") or 0)),
        )
        for rank, (model, g) in enumerate(ranking, 1):
            marker = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
            print(f"  {task:<14} {marker} {model:<26} score={g['score']:>3} "
                  f"tok/s={(g['tokens_per_sec'] or 0):>5.1f}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
