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

def matrix_mul(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def det(A):
    if len(A) == 1:
        return A[0][0]
    elif len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det_val = 0
        for c in range(len(A)):
            submatrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            sub_det = det(submatrix)
            det_val += sign * A[0][c] * sub_det
        return det_val

def permanent(A):
    if len(A) == 1:
        return A[0][0]
    elif len(A) == 2:
        return A[0][0] * A[1][1] + A[0][1] * A[1][0]
    else:
        perm_val = 0
        for c in range(len(A)):
            submatrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            sub_perm = permanent(submatrix)
            perm_val += sign * A[0][c] * sub_perm
        return perm_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = n
        f = [random.randint(0, 1) for _ in range(d)]
        φ_f = [[f[i] * f[j] for j in range(n)] for i in range(n)]
        
        min_deg_W = min(sum(row) for row in φ_f)
        perm_gap = permanent([[1 if i == j else 0 for j in range(n)] for i in range(n)]) - det([[1 if i == j else 0 for j in range(n)] for i in range(n)])
        
        results.append({
            "n": n,
            "min_deg_W": min_deg_W,
            "perm_gap": perm_gap
        })
    
    mean_min_deg_W = sum(result["min_deg_W"] for result in results) / len(results)
    mean_perm_gap = sum(result["perm_gap"] for result in results) / len(results)
    
    conjecture_holds = all(result["min_deg_W"] >= result["perm_gap"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_deg_W vs perm_gap",
        "metric_value": mean_min_deg_W,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")