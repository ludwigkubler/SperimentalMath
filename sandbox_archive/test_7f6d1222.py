# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) * (2 * random.randint(0, 1) - 1)
                   for _ in range(3)]
        clauses.append(clause)
    return clauses

def walsh_hadamard_transform(f, n):
    N = 1 << n
    for s in range(n):
        mask = 1 << (n - s - 1)
        for x in range(N):
            if x & mask:
                f[x] -= f[x ^ mask]
            else:
                f[x] += f[x ^ mask]
        for x in range(N):
            f[x] /= math.sqrt(2)

def additive_energy(f, n):
    E = 0
    N = 1 << n
    for i in range(N):
        for j in range(i + 1, N):
            E += abs(f[i] * f[j])
    return E

def sos_refutation_size(clauses):
    # Simple heuristic: tree depth of DPLL-based search
    max_depth = 0
    stack = [(clauses, [])]
    while stack:
        remaining_clauses, assignment = stack.pop()
        if not remaining_clauses:
            max_depth = max(max_depth, len(assignment))
            continue
        clause = random.choice(remaining_clauses)
        for var in clause:
            new_assignment = assignment + [var]
            new_remaining = [c for c in remaining_clauses if not any(v in c for v in new_assignment)]
            stack.append((new_remaining, new_assignment))
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    m = 5 * n
    clauses = generate_3cnf(n, m)
    f = [0] * (1 << n)
    for clause in clauses:
        for x in range(1 << n):
            if all((x >> abs(v) - 1) & 1 == v // abs(v) for v in clause):
                f[x] += 1
    walsh_hadamard_transform(f, n)
    E = additive_energy(f, n)
    k = sos_refutation_size(clauses)
    if k == 0:
        return {
            "metric_name": "E / (m² / k)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "SOS refutation size is zero"
        }
    metric_value = E * k / m**2
    conjecture_holds = abs(metric_value - 1) < 0.1
    counterexample = "" if conjecture_holds else f"E = {E}, m²/k = {m**2/k}"
    return {
        "metric_name": "E / (m² / k)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"E < m² / (2k)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")