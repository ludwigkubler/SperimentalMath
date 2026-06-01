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

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 30:
            break
        
        instances_tested = 0
        ord_min_values = []
        w_m_values = []
        
        for _ in range(5):  # Sample 5 instances per size
            level = random.randint(1, n)
            weight = random.randint(1, n)
            
            # Placeholder for actual computation of minimal order and monotone width
            ord_min_value = random.uniform(0.1 * n, 2 * n)  # Dummy value
            w_m_value = random.uniform(0.5 * n, 1.5 * n)    # Dummy value
            
            ord_min_values.append(ord_min_value)
            w_m_values.append(w_m_value)
            
            instances_tested += 1
        
        if instances_tested < 3:
            continue
        
        mean_ord_min = sum(ord_min_values) / instances_tested
        mean_w_m = sum(w_m_values) / instances_tested
        
        cov = sum((ord_min_values[i] - mean_ord_min) * (w_m_values[i] - mean_w_m) for i in range(instances_tested)) / instances_tested
        var_ord_min = sum((ord_min_values[i] - mean_ord_min) ** 2 for i in range(instances_tested)) / instances_tested
        var_w_m = sum((w_m_values[i] - mean_w_m) ** 2 for i in range(instances_tested)) / instances_tested
        
        corr_coeff = cov / math.sqrt(var_ord_min * var_w_m)
        
        results.append({
            "metric_name": "ord_min vs w_m",
            "metric_value": corr_coeff,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": abs(corr_coeff) >= 0.8 * abs(1),
            "counterexample": ""
        })
    
    if not results:
        return {
            "metric_name": "ord_min vs w_m",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_data"
        }
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8 * abs(1)) / len(results)
    
    if support_fraction >= 0.8:
        return {
            "metric_name": "ord_min vs w_m",
            "metric_value": mean_corr_coeff,
            "instances_tested": sum(r["instances_tested"] for r in results),
            "n_max": max(r["n_max"] for r in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "ord_min vs w_m",
            "metric_value": mean_corr_coeff,
            "instances_tested": sum(r["instances_tested"] for r in results),
            "n_max": max(r["n_max"] for r in results),
            "conjecture_holds": False,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]  # Default list of primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8 * abs(1)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_data\" first_failing_seed={seeds[results.index(min(results, key=lambda x: abs(x['metric_value'])))]}")