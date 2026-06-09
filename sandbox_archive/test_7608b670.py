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

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input must be a boolean function with 2^n elements")
    
    rank_var = 0
    for i in range(n + 1):
        count = sum(1 for j in range(2**(n-i)) if all(f[j] == f[j ^ (1 << k)] for k in range(i)))
        rank_var += count
    
    return rank_var / (2**n)

def minimal_representation_degree_as_hypergeometric_series(f):
    n = int(math.log2(len(f)))
    # Simplified representation degree calculation
    return len(f) ** 0.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        
        R_f = communication_complexity_rank_variance(f)
        D_f = minimal_representation_degree_as_hypergeometric_series(f)
        
        results.append((R_f, D_f))
    
    if not results:
        return {
            "metric_name": "D(f) vs R(f)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    R_f_values = [R for R, _ in results]
    D_f_values = [D for _, D in results]
    
    n_max = max(n for n, _ in results)
    
    # Polynomial fitting
    coefficients = polynomial_fit(R_f_values, D_f_values)
    if not coefficients:
        return {
            "metric_name": "D(f) vs R(f)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "polynomial_fit_failed"
        }
    
    # Check the polynomial coefficient
    if coefficients[-1] > (max(R_f_values)) ** 1.5:
        return {
            "metric_name": "D(f) vs R(f)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "polynomial_coefficient_too_large"
        }
    
    return {
        "metric_name": "D(f) vs R(f)",
        "metric_value": coefficients[-1],
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

def polynomial_fit(x, y):
    if not x or not y:
        return None
    
    n = len(x)
    A = [[x[i]**j for j in range(n)] for i in range(n)]
    B = y[:]
    
    # Gaussian elimination
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        B[i], B[max_row] = B[max_row], B[i]
        
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        B[i] /= factor
        
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]
            B[k] -= factor * B[i]
    
    # Back substitution
    coefficients = [0] * n
    for i in range(n - 1, -1, -1):
        coefficients[i] = B[i]
        for j in range(i + 1, n):
            coefficients[i] -= A[i][j] * coefficients[j]
    
    return coefficients

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_str = f"SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        result_str = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result_str}")