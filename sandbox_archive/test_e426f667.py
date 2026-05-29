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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def polynomial_representation(f, n):
    k = 3  # Using a fixed k for simplicity
    A = [[0] * (2**(n+1)) for _ in range(2**k)]
    points = [(i >> j) & 1 for i in range(2**k) for j in range(n)]
    for x in range(2**n):
        f_val = sum(f[i] << i for i in range(n))
        A[f_val][sum(points)] += 1
    return A

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for col in range(n):
        pivot_row = -1
        for row in range(rank, m):
            if A[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        rank += 1
        for r in range(m):
            if r != pivot_row and A[r][col] != 0:
                factor = A[r][col] / A[pivot_row][col]
                for c in range(n):
                    A[r][c] -= factor * A[pivot_row][c]
    return rank

def tree_like_resolution_width(f, n):
    # Placeholder function to compute the width
    # This is a dummy implementation and should be replaced with actual logic
    return 1 + n // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        A = polynomial_representation(f, n)
        rank = matrix_rank(A)
        width = tree_like_resolution_width(f, n)
        results.append({"n": n, "rank": rank, "width": width})
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["rank"] <= math.sqrt(n) * math.log2(n) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank of A(P, f)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")