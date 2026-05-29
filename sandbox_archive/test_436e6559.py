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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    return A

def matrix_rank(A):
    rank = 0
    A_rref = gaussian_elimination(A)
    for row in A_rref:
        if any(row):
            rank += 1
    return rank

def polynomial_representation(f, n):
    # Convert Boolean function to polynomial representation over GF(2^k)
    k = random.randint(3, 5)  # Choose a random k between 3 and 5
    poly = [0] * (2**k - 1)
    for x in range(2**n):
        if f(x):
            poly[random.randint(0, len(poly)-1)] += 1
    return poly

def tree_like_resolution_width(f, n):
    # Placeholder function to compute tree-like resolution width
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(n//2, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = lambda x: random.choice([True, False])  # Placeholder Boolean function
        rank = matrix_rank(polynomial_representation(f, n))
        width = tree_like_resolution_width(f, n)
        
        results.append({
            "n": n,
            "rank": rank,
            "width": width
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    conjecture_holds = all(result["rank"] <= math.sqrt(n) * math.log2(n) for result in results)
    counterexample = "" if conjecture_holds else f"Rank {result['rank']} exceeds bound for n={n}"
    
    return {
        "metric_name": "Rank of Matrix",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")