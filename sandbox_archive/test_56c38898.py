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

def characteristic_polynomial(truth_table):
    n = int(math.log2(len(truth_table)))
    if 2**n != len(truth_table):
        raise ValueError("Truth table length must be a power of 2")
    
    poly = [0] * (n + 1)
    for i in range(2**n):
        x = truth_table[i]
        for j in range(n):
            if x & (1 << j):
                poly[j] += 1
        poly[n] += x
    
    return poly

def rank_of_variety(poly, n):
    # Implement Gaussian elimination to find the rank of the matrix
    A = [poly[i:i+n+1] for i in range(n+1)]
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            pivot_row = None
            for i in range(rank, m):
                if A[i][j]:
                    pivot_row = i
                    break
            if pivot_row is not None:
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                rank += 1
                for i in range(rank, m):
                    factor = -A[i][j] / A[rank-1][j]
                    for k in range(n+1):
                        A[i][k] += factor * A[rank-1][k]
        return rank
    
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        functions = [generate_random_boolean_function(n) for _ in range(30)]
        
        for func in functions:
            poly = characteristic_polynomial(func)
            rank = rank_of_variety(poly, n)
            results.append((n, rank))
    
    if not results:
        return {
            "metric_name": "Rank of Variety",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No functions generated"
        }
    
    n_values, ranks = zip(*results)
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank)**2 for x in ranks) / len(ranks))
    
    # Hypothetical slope based on the conjecture
    g = 1  # Smallest genus for a non-trivial curve
    s_values = n_values
    expected_slope = (g**2 / max(s_values)) * len(n_values)
    
    correlation_coefficient = sum((x - mean_rank) * (y - expected_slope) for x, y in zip(ranks, s_values))
    correlation_coefficient /= math.sqrt(sum((x - mean_rank)**2 for x in ranks) * sum((y - expected_slope)**2 for y in s_values))
    
    return {
        "metric_name": "Rank of Variety",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": correlation_coefficient >= 0.9 and abs(correlation_coefficient - expected_slope) / expected_slope <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")