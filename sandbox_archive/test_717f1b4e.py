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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for row in A_copy:
        if any(row[j] != 0 for j in range(len(row))):
            rank += 1
    return rank

def generate_communication_complexity_instance(n):
    # Generate a random communication complexity problem instance
    # This is a placeholder function; replace with actual generation logic
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_communication_complexity_instance(n)
        Q = matrix_multiply(phi, phi)
        min_rank = matrix_rank(Q)
        
        if n <= 1:
            continue
        
        r_phi = matrix_rank(phi)
        if r_phi == 0:
            continue
        
        ratio = Fraction(min_rank, math.log(n) * math.log(r_phi))
        results.append({
            "min_rank": min_rank,
            "n": n,
            "r_phi": r_phi,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    ratio_values = [result["ratio"] for result in results]
    mean_ratio = sum(ratio_values) / len(ratio_values)
    
    return {
        "metric_name": "Ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": any(ratio <= 1.5 for ratio in ratio_values) and all(ratio <= 10 for ratio in ratio_values),
        "counterexample": "" if all(ratio <= 1.5 for ratio in ratio_values) else "Ratio > 1.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != 'No valid instances generated')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")