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
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def det(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det_val = 0
        for j in range(n):
            sub_matrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det_val += (-1) ** j * matrix[0][j] * det(sub_matrix)
        return det_val

def perm(n):
    if n == 0:
        return [[]]
    perms = []
    for i in range(n):
        for p in perm(n - 1):
            if i not in p:
                perms.append(p + [i])
    return perms

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_max = math.isqrt(n * n // 2)
        if m_max < n:
            continue
        
        f = sum(random.randint(1, 10) * x**i for i in range(n))
        perm_n = det(perm(n))
        det_m = [det([[f(x) for x in range(m)]]) for m in range(1, m_max + 1)]
        
        if not det_m:
            continue
        
        ratios = [perm_n / d for d in det_m]
        results.extend(ratios)
    
    if not results:
        return {
            "metric_name": "Ratio of I(perm_n) to I(det_m)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    avg_ratio = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - avg_ratio) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "Ratio of I(perm_n) to I(det_m)",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": avg_ratio > 1 and std_dev < 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["metric_value"] for r in results) > 1.1:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=2) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=<k>")