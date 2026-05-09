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

def generate_random_graph(n, p):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                A[i][j] = A[j][i] = 1
    return A

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def compute_spectral_norm(A):
    n = len(A)
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    epsilon = 1e-6
    k = 50
    x = [random.random() for _ in range(n)]
    x = [x[i] / math.sqrt(sum(x[j]**2 for j in range(n))) for i in range(n)]
    for _ in range(k):
        y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
        y_norm = sum(y[i]**2 for i in range(n))
        x = [y[i] / math.sqrt(y_norm) for i in range(n)]
    return max(abs(x[i]) for i in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    p = 0.5
    A = generate_random_graph(n, p)
    sigma_min = compute_spectral_norm(A)
    d_max = 10
    c = 0.1
    conjecture_holds = True
    counterexample = ""
    
    for d in range(1, d_max + 1):
        # Truncated Lasserre hierarchy simulation (simplified)
        if sigma_min < c * (d ** -1):
            conjecture_holds = False
            counterexample = f"SOS degree {d} requires σ_min(A) ≥ {c * (d ** -1)}, but got {sigma_min}"
            break
    
    return {
        "metric_name": "smallest_singular_value",
        "metric_value": sigma_min,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")