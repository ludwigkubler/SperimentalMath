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

def generate_matrix(N):
    return [[random.choice([0, 1]) for _ in range(N)] for _ in range(N)]

def is_independent(lattice, M):
    for i in lattice:
        if any(all(M[i][j] == M[k][j] for j in range(len(M))) for k in lattice if k != i):
            return False
    return True

def find_minimal_lattices(M):
    N = len(M)
    min_I = N
    for r in range(1, N + 1):
        for I in combinations(range(N), r):
            if is_independent(I, M):
                min_I = min(min_I, len(I))
                break
        if min_I < N:
            break
    return min_I

def communication_complexity(n, I):
    if n <= 0 or I <= 0:
        return float('inf')
    return math.log2(n) * math.log(I)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [10, 15, 20, 30, 40]:
        M = generate_matrix(n)
        I = find_minimal_lattices(M)
        cc = communication_complexity(n, I)
        results.append({
            "n": n,
            "I": I,
            "cc": cc
        })
    metric_value = sum(result["cc"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["cc"] <= math.log2(result["n"]) * math.log(min(result["I"], result["n"] - result["I"])) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")