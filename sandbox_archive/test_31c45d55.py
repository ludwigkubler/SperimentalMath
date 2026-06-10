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

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    
    # Forward elimination
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        
        pivot = A_b[i][i]
        for j in range(n + 1):
            A_b[i][j] /= pivot
        
        for k in range(i+1, n):
            factor = A_b[k][i]
            for j in range(n + 1):
                A_b[k][j] -= factor * A_b[i][j]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A_b[i][-1]
        for j in range(i+1, n):
            x[i] -= A_b[i][j] * x[j]
    
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n)
        phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        
        # Compute geometric Langlands duality invariant D(phi)
        # This is a placeholder function. Replace with actual computation.
        def compute_d_phi(phi):
            return random.random() * n
        
        d_phi = compute_d_phi(phi)
        
        # Compute circuit depth d(phi)
        # This is a placeholder function. Replace with actual computation.
        def compute_circuit_depth(phi):
            return random.randint(1, 3*n)
        
        d_circuit = compute_circuit_depth(phi)
        
        results.append({
            "d_phi": d_phi,
            "d_circuit": d_circuit
        })
    
    mean_d_phi = sum(result["d_phi"] for result in results) / len(results)
    mean_d_circuit = sum(result["d_circuit"] for result in results) / len(results)
    
    correlation = sum((result["d_phi"] - mean_d_phi) * (result["d_circuit"] - mean_d_circuit) for result in results) / len(results)
    
    conjecture_holds = correlation > 0.95
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    correlations = [result["metric_value"] for result in results]
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(correlations)/len(correlations)} std={math.sqrt(sum((x - sum(correlations)/len(correlations))**2 for x in correlations)/len(correlations))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_bound_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")