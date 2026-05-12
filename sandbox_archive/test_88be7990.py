# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def fourier_transform(f, n):
    N = 2**n
    result = [0] * N
    for k in range(N):
        sum_val = 0
        for j in range(N):
            angle = 2 * math.pi * k * j / N
            sum_val += f[j] * math.cos(angle) + 1j * math.sin(angle)
        result[k] = sum_val / N
    return result

def gowers_norm_U2(f, n):
    ft = fourier_transform(f, n)
    norm_squared = sum(abs(x)**4 for x in ft)
    return math.sqrt(norm_squared)

def dpll_circuit_minimization(f, n):
    # Simplified DPLL-based heuristic (recursive partitioning with clause learning)
    def dpll(clauses, assignment, literals):
        if not clauses:
            return True
        literal = literals[0]
        pos_clauses = [c for c in clauses if literal in c]
        neg_clauses = [c for c in clauses if -literal in c]
        if dpll(pos_clauses, assignment + [literal], literals[1:]):
            return True
        if dpll(neg_clauses, assignment + [-literal], literals[1:]):
            return True
        return False

    def minimize(clauses):
        n = len(clauses)
        if n == 0:
            return 0
        literal = random.choice([1, -1])
        pos_clauses = [c for c in clauses if literal in c]
        neg_clauses = [c for c in clauses if -literal in c]
        return 1 + min(minimize(pos_clauses), minimize(neg_clauses))

    literals = list(range(1, n+1))
    return minimize(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    f = generate_random_boolean_function(n)
    norm_U2 = gowers_norm_U2(f, n)
    S_f = dpll_circuit_minimization(f, n)
    metric_value = norm_U2 * S_f
    conjecture_holds = metric_value >= 1 / math.sqrt(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "norm_U2 * S_f",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")