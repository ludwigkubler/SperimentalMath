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

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        if any(matrix[i][j] != 0 for j in range(n)):
            rank += 1
            for j in range(n):
                matrix[i][j] /= matrix[i][j]
            for k in range(m):
                if k != i and any(matrix[k][j] != 0 for j in range(n)):
                    for j in range(n):
                        matrix[k][j] -= matrix[i][j] * matrix[k][j]
    return rank

def secant_variety_dimension(M):
    m, n = len(M), len(M[0])
    V_M = []
    for i in range(m):
        for j in range(n):
            if M[i][j] == 1:
                V_M.append([M[k][l] * (k != i or l != j) for k in range(m) for l in range(n)])
    V_M = [v for v in V_M if any(x != 0 for x in v)]
    rank_2_flattening = []
    for v1 in V_M:
        for v2 in V_M:
            flattened = [v1[i] + v2[i] for i in range(m * n)]
            rank_2_flattening.append(flattened)
    return matrix_rank(rank_2_flattening)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    disjoint = all(M[i][j] == 0 or i == j for i in range(n) for j in range(n))
    if not disjoint:
        return {
            "metric_name": "secant_variety_dimension",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_disjoint"
        }
    dim = secant_variety_dimension(M)
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": dim,
        "instances_tested": 1,
        "conjecture_holds": dim >= n / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    mean = total_metric_value / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction / len(results)}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_disjoint' first_failing_seed={first_failing_seed}")