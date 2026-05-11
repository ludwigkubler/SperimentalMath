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
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_power(M, p):
    if p == 0:
        return [[int(i == j) for j in range(len(M))] for i in range(len(M))]
    elif p == 1:
        return M
    else:
        half = matrix_power(M, p // 2)
        result = matrix_multiply(half, half)
        if p % 2 == 1:
            result = matrix_multiply(result, M)
        return result

def kronecker_coefficient(n, k):
    if n < k or k == 0:
        return 0
    if n == k:
        return 1
    result = 0
    for i in range(k + 1):
        result += (-1) ** (k - i) * math.comb(n, i) * math.comb(n - i, k - i)
    return abs(result)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    results = []
    
    for n in range(5, n_max + 1):
        k = math.ceil(math.log2(n))
        min_coeff_perm = float('inf')
        min_coeff_det = float('inf')
        
        for m in range(1, int(n ** 1.5)):
            coeff_perm = kronecker_coefficient(n, k)
            coeff_det = kronecker_coefficient(m, k)
            if coeff_perm < min_coeff_perm:
                min_coeff_perm = coeff_perm
            if coeff_det < min_coeff_det:
                min_coeff_det = coeff_det
        
        results.append({
            "n": n,
            "k": k,
            "min_coeff_perm": min_coeff_perm,
            "min_coeff_det": min_coeff_det,
            "ratio": min_coeff_perm / (min_coeff_det + 1e-9)
        })
    
    all_ratios = [r["ratio"] for r in results]
    avg_ratio = sum(all_ratios) / len(all_ratios)
    std_ratio = math.sqrt(sum((x - avg_ratio) ** 2 for x in all_ratios) / len(all_ratios))
    
    conjecture_holds = all(r["ratio"] > 100 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Kronecker Coefficient Ratio",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    avg_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - avg_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")