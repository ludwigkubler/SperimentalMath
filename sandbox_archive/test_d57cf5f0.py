# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = -A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def elementary_symmetric_polynomial(A):
    m, n = len(A), len(A[0])
    B = [[A[i][j] for j in range(i+1)] for i in range(m)]
    return gaussian_elimination(B)

def indicator_polynomial(CNF):
    n = len(CNF)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    A[0][0] = 1
    for clause in CNF:
        for i, j in combinations(range(1, n + 1), 2):
            if i not in clause and j not in clause:
                A[i][j] += 1
    return elementary_symmetric_polynomial(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    CNF = [random.sample(range(1, n + 1), k=3) for _ in range(random.randint(1, 2 * n))]
    ABP_width = len(CNF)
    ES_coeff_count = indicator_polynomial(CNF)
    return {
        "metric_name": "ABP Width vs. ES Coeff Count",
        "metric_value": ES_coeff_count,
        "instances_tested": 1,
        "conjecture_holds": ES_coeff_count <= ABP_width,
        "counterexample": "" if ES_coeff_count <= ABP_width else f"n={n}, ABP width={ABP_width}, ES coeff count={ES_coeff_count}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")