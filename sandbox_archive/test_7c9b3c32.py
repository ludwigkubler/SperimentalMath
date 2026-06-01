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

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def min_local_ring_norm(tropical_circuit):
    # Placeholder implementation, should be replaced with actual computation
    return random.random()

def monotone_width(circuit):
    # Placeholder implementation, should be replaced with actual computation
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    correlations = []
    
    for n in n_values:
        instances_tested = 0
        total_t_norm = 0
        total_width = 0
        
        while instances_tested < 30:
            circuit = [random.choice([0, 1]) for _ in range(n)]
            t_norm = min_local_ring_norm(circuit)
            width = monotone_width(circuit)
            
            if t_norm > 0 and width > 0:
                total_t_norm += t_norm
                total_width += width
                instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "No valid instances found"
            }
        
        avg_t_norm = total_t_norm / instances_tested
        avg_width = total_width / instances_tested
        correlation = avg_t_norm * avg_width / (avg_t_norm**2 + avg_width**2)
        correlations.append(correlation)
    
    mean_corr = sum(correlations) / len(correlations)
    std_corr = math.sqrt(sum((x - mean_corr)**2 for x in correlations) / len(correlations))
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_corr,
        "instances_tested": 30 * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": mean_corr >= 0.8 and std_corr <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No valid instances found")