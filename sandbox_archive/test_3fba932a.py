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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= 2
    return C

def matrix_power(A, k):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_mult(result, A)
        A = matrix_mult(A, A)
        k //= 2
    return result

def generate_random_bp(n):
    P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    Q = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    R = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    S = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return P, Q, R, S

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        P, Q, R, S = generate_random_bp(n)
        
        # Compute noncommutative Fourier transform
        F = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                F[i][j] = matrix_power(P, i)[j][0] * matrix_power(Q, j)[i][0]
        
        # Measure maximum absolute coefficient
        max_coeff = max(abs(coeff) for row in F for coeff in row)
        
        results.append({
            "n": n,
            "max_coeff": max_coeff
        })
    
    metric_value = sum(result["max_coeff"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(max_coeff >= n for result in results for max_coeff in [result["max_coeff"]])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Noncommutative Fourier Coefficient Gap",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")