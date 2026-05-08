# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        for k in range(i+1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    
    # Back-substitute to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def compute_disp(B_mid):
    s = len(B_mid)
    n = 2 ** (len(B_mid[0]) - 1)
    sigma_squared_sum = sum(sigma**2 for _, sigma in sorted((sum(row), math.sqrt(sum(x*x for x in row))) for row in B_mid))
    sigma_fourth_sum = sum(sigma**4 for _, sigma in sorted((sum(row), math.sqrt(sum(x*x for x in row))) for row in B_mid))
    disp = 2 * math.log2((sigma_squared_sum ** 2) / sigma_fourth_sum)
    return disp

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12, 14]
    results = []
    
    for N in n_values:
        s = 2 ** (N // 2)
        B_mid = [[random.randint(0, 1) for _ in range(s)] for _ in range(2**N)]
        
        disp = compute_disp(B_mid)
        results.append({
            "n": N,
            "s": s,
            "disp": disp
        })
    
    metric_value = sum(result["disp"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["disp"] >= N / 2 - 4 * math.log2(N) for result in results if result["n"] >= 8)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "DISP",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_disp = sum(r["metric_value"] for r in results) / len(results)
    std_disp = math.sqrt(sum((r["metric_value"] - mean_disp)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_disp} std={std_disp} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")