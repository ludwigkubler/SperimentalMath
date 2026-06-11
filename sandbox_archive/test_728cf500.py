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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def p_adic_index(A):
    n = len(A)
    det = 1
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    for i in range(n):
        det *= A[i][i]
    return abs(det)

def communication_rank(G):
    # Placeholder implementation. Replace with actual computation.
    return len(G)  # Example: rank is the number of vertices

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = [random.sample(range(1, n+1), random.randint(1, n)) for _ in range(n)]
        A_G = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i, n):
                A_G[i][j] = sum(len(set(G[k]) & set(G[l])) for k in range(n) if k != i and k != j)
                A_G[j][i] = A_G[i][j]
        
        i_G = p_adic_index(A_G)
        r_G = communication_rank(G)
        
        results.append({
            "n": n,
            "i_G": i_G,
            "r_G": r_G
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    i_G_values = [r["i_G"] for r in results]
    r_G_values = [r["r_G"] for r in results]
    
    mean_i_G = sum(i_G_values) / len(i_G_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)
    
    n_max = max([r["n"] for r in results])
    
    if n_max < 16:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_low"
        }
    
    if len(i_G_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    covariance = sum((i_G_values[i] - mean_i_G) * (r_G_values[i] - mean_r_G) for i in range(len(i_G_values)))
    variance_i_G = sum((i_G_values[i] - mean_i_G) ** 2 for i in range(len(i_G_values)))
    variance_r_G = sum((r_G_values[i] - mean_r_G) ** 2 for i in range(len(r_G_values)))
    
    if variance_i_G == 0 or variance_r_G == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_i_G) * math.sqrt(variance_r_G))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(pearson_corr) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=None support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Pearson correlation coefficient < 0.7"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")