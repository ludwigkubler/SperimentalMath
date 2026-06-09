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
from itertools import combinations

# Gaussian elimination with partial pivoting
def gaussian_elimination(A, b):
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        # Find the pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(Augmented[k][i]) > abs(Augmented[max_row][i]):
                max_row = k
        
        # Swap rows
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        
        # Eliminate non-pivot elements in the current column
        for k in range(i+1, n):
            factor = Fraction(Augmented[k][i], Augmented[i][i])
            for j in range(i, n + 1):
                Augmented[k][j] -= factor * Augmented[i][j]
    
    # Back-substitution to find the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(Augmented[i][-1], Augmented[i][i])
        for k in range(i-1, -1, -1):
            Augmented[k][-1] -= Augmented[k][i] * x[i]
    
    return x

# Compute the minimal representation degree of a graph using Kostant-Macdonald formula with q=0
def compute_minimal_representation_degree(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    for i, j in combinations(range(n), 2):
        if G[i][j]:
            A[i][i] += 1
            A[j][j] += 1
            A[i][j] -= 1
            A[j][i] -= 1
            b[i] += 1
            b[j] += 1
    
    try:
        return sum(gaussian_elimination(A, b))
    except ZeroDivisionError:
        return None

# Compute the communication complexity rank variance of a graph
def compute_communication_complexity_rank_variance(G):
    n = len(G)
    rank = 0
    
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                rank += 1
    
    return rank * (n - rank)

# Run a single trial with the given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        G = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
        
        d = compute_minimal_representation_degree(G)
        r = compute_communication_complexity_rank_variance(G)
        
        if d is not None:
            results.append((d, r))
    
    if len(results) < 30:
        return {
            "metric_name": "minimal_representation_degree",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    d_values, r_values = zip(*results)
    correlation_coefficient = sum((d - mean_d) * (r - mean_r) for d, r in zip(d_values, r_values)) / len(results)
    mean_d = sum(d_values) / len(results)
    mean_r = sum(r_values) / len(results)
    
    return {
        "metric_name": "minimal_representation_degree",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")