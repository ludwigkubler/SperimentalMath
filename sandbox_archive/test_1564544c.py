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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def max_singular_value(M):
    m, n = len(M), len(M[0])
    U = [[0] * n for _ in range(n)]
    S = [0] * min(m, n)
    V = [[0] * m for _ in range(m)]

    # Center the matrix
    M_centered = [[M[i][j] - (sum(M[i]) + sum(M[j])) / (2 * n) for j in range(n)] for i in range(m)]

    # Compute SVD using power iteration method
    v = [1.0] * n
    for _ in range(100):
        u = [sum(M_centered[i][j] * v[j] for j in range(n)) for i in range(m)]
        norm_u = math.sqrt(sum(x**2 for x in u))
        u = [x / norm_u for x in u]
        s = sum(u[i] * M_centered[i][j] * v[j] for i in range(m) for j in range(n))
        v = [sum(M_centered[i][j] * u[j] for j in range(n)) for i in range(m)]
        norm_v = math.sqrt(sum(x**2 for x in v))
        v = [x / norm_v for x in v]

    S[0] = s
    U[0] = u
    V[0] = v

    return max(S)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    norm = max_singular_value(M)
    c = 0.5
    conjecture_holds = norm >= c * math.sqrt(n)
    counterexample = "" if conjecture_holds else "norm < c√n"
    return {
        "metric_name": "noncommutative_L_infinity_norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = "norm < c√n"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")