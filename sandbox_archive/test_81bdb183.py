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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def trace(matrix):
    n = len(matrix)
    tr = 0
    for i in range(n):
        tr += matrix[i][i]
    return tr

def schatten_p_norm(M, p):
    n = len(M)
    A = matrix_multiplication(M, M)
    det_A = 1.0
    for i in range(n):
        det_A *= A[i][i]
    if det_A <= 0:
        return float('inf')
    return (det_A ** (1 / p)) * n ** (-1 / p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    p_values = [1.5, 1.75, 1.9]
    C_estimates = []
    for p in p_values:
        norm = schatten_p_norm(M, p)
        C_estimates.append(norm * n ** (1 / p))
    
    # Fit regression model
    from scipy.stats import linregress
    x = [1 / n ** (1 / p) for p in p_values]
    y = C_estimates
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    
    if abs(slope - 1.2) > 0.2:
        return {
            "metric_name": "Schatten p-norm",
            "metric_value": None,
            "instances_tested": len(p_values),
            "conjecture_holds": False,
            "counterexample": f"Slope {slope} does not match expected 1.2"
        }
    
    return {
        "metric_name": "Schatten p-norm",
        "metric_value": slope,
        "instances_tested": len(p_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    
    if supported_count >= 0.8 * len(seeds):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={supported_count/len(seeds)}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Slope does not match expected 1.2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")