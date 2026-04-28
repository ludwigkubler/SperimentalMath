# auto-injected by SEC sandbox
import math
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import json
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def xor(x, y):
        return x ^ y
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            if A[i][i] == 0:
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
            pivot = A[i][i]
            for j in range(n):
                A[i][j] = A[i][j] // pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def min_weight_inconsistent_subsets(A, b):
        m, n = len(A), len(A[0])
        A_b = [row + b for row in A]
        g_star = 0
        for weight in range(1, m + 1):
            for subset in combinations(range(m), weight):
                if all(all(A_b[i][j] == 0 for j in range(n)) for i in subset):
                    g_star = max(g_star, weight)
        return g_star
    
    def sigma(A):
        A_plus_A = set()
        for a, b in product(A, repeat=2):
            A_plus_A.add(xor(a, b))
        return len(set(A)), len(A_plus_A), len(A_plus_A) / len(A)
    
    n = random.choice([8, 10, 12, 14, 16])
    alpha = random.choice([1.2, 2.0, 3.0])
    m = int(n * alpha)
    
    F = []
    for _ in range(m):
        clause = [random.randint(0, 1) for _ in range(n)]
        b = random.randint(0, 1)
        F.append((clause, b))
    
    A = [F[i][0] for i in range(len(F))]
    set_A_size, A_plus_A_size, sigma_value = sigma(A)
    g_star = min_weight_inconsistent_subsets(A, [F[i][1] for i in range(len(F))])
    
    metric_name = "g*(F) - σ(A)"
    metric_value = g_star - sigma_value
    instances_tested = 1
    conjecture_holds = g_star >= sigma_value + 1
    counterexample = "" if conjecture_holds else f"Instance with n={n}, alpha={alpha}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")