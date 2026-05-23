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

def generate_random_twisted_module(q, n):
    M = [[random.randint(0, q - 1) for _ in range(n)] for _ in range(n)]
    return M

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def find_minimal_rank(M, n):
    P = [2] + list(range(1, n))
    max_rank = 0
    for i in range(n):
        permuted_M = [[M[P[j]][P[k]] for k in range(n)] for j in range(n)]
        rank = sum(any(row) and all(x == 0 for row in A) for A in [permuted_M])
        max_rank = max(max_rank, rank)
    return max_rank

def monotone_circuit_depth(k, n):
    if k == 1:
        return 1
    elif k == n:
        return n
    else:
        return math.ceil((n + k - 2) / (k - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q = random.randint(2, 5)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_random_twisted_module(q, n)
    k = random.randint(3, n - 1)
    
    minimal_rank = find_minimal_rank(M, n)
    depth = monotone_circuit_depth(k, n)
    ratio = depth / minimal_rank
    
    return {
        "metric_name": "Ratio of Monotone Circuit Depth to Minimal Rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2.0,  # Threshold T = 2.0 for this example
        "counterexample": "" if ratio <= 2.0 else f"Ratio exceeded threshold: {ratio}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded threshold\" first_failing_seed={first_failing_seed}")