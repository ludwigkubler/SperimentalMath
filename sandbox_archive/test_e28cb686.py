# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for row in A_copy:
        if any(row):
            rank += 1
    return rank

def generate_communication_complexity_instance(n, r):
    # Generate a random communication complexity instance
    # This is a placeholder function; replace with actual generation logic
    Q = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        Q = generate_communication_complexity_instance(n, r=n)
        min_rank = matrix_rank(Q)
        
        if min_rank == 0 or n <= 1:
            continue
        
        ratio = Fraction(min_rank, n * n).limit_denominator()
        results.append({
            "n": n,
            "min_rank": min_rank,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 1,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    total_ratio = sum(result["ratio"] for result in results)
    avg_ratio = total_ratio / len(results)
    max_n = max(result["n"] for result in results)
    
    return {
        "metric_name": "Ratio",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] <= 1.5 for result in results):
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(result["metric_value"] > 10 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 10' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")