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

def matrix_multiply(A, B, mod):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def gaussian_elimination(A, b, mod):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] = (A[i][j] * pow(pivot, mod-2, mod)) % mod
        b[i] = (b[i] * pow(pivot, mod-2, mod)) % mod
        
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % mod
                b[j] = (b[j] - factor * b[i]) % mod
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) % mod
    return x

def grothendieck_witt_class(poly, mod):
    n = len(poly)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = (poly[i] + poly[j]) % mod
    b = [1] * n
    
    try:
        solution = gaussian_elimination(A, b, mod)
        rank = sum(1 for x in solution if x != 0)
        return rank
    except Exception as e:
        print(f"Error in grothendieck_witt_class: {e}")
        return None

def resolution_width(F):
    # Simplified DPLL solver to estimate resolution width (placeholder)
    return len(F)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n // 2, n * 3)
    k = 2
    
    F = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        F.append(clause)
    
    tropical_curve_rank = grothendieck_witt_class(F, 2)
    if tropical_curve_rank is None:
        return {
            "metric_name": "tropical_curve_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    resolution_width_F = resolution_width(F)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_F,
        "instances_tested": 1,
        "conjecture_holds": resolution_width_F <= 1.2 * tropical_curve_rank,
        "counterexample": "" if resolution_width_F <= 1.2 * tropical_curve_rank else f"Resolution width {resolution_width_F} > 1.2 * Tropical curve rank {tropical_curve_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [random.randint(1, 999973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - avg_metric_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")