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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def solve_linear_system(A, b):
    n = len(A)
    Ab = [row + [b[i]] for i, row in enumerate(A)]
    gaussian_elimination(Ab)
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (Ab[i][-1] - sum(Ab[i][j] * x[j] for j in range(i+1, n))) / Ab[i][i]
    return x

def log_sum_exp(h):
    max_val = max(h)
    return max_val + math.log(sum(math.exp(x - max_val) for x in h))

def maslov_dequantized_fourier_transform(f, beta):
    n = len(f)
    omega = math.exp(2 * math.pi / n)
    tft_f = [0] * n
    for k in range(n):
        if k == 0:
            sum_exp = log_sum_exp([-beta * f[j] for j in range(n)])
        else:
            sum_exp = log_sum_exp([-beta * (f[j] + omega**(j*k)) / 2 for j in range(n)])
        tft_f[k] = -(1/beta) * math.log(abs(sum_exp))
    return tft_f

def min_convolution(f):
    n = len(f)
    g = [0] * n
    for k in range(n):
        g[k] = min(f[i] + f[j] for i, j in enumerate(range(k+1, n)) if (i+j) % n == k)
    return g

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 8
    beta_values = [5, 10, 20, 50, 100, 200]
    results = []
    
    for beta in beta_values:
        f = [random.uniform(0, 1) for _ in range(n)]
        g = min_convolution(f)
        
        tft_f = maslov_dequantized_fourier_transform(f, beta)
        tft_g = maslov_dequantized_fourier_transform(g, beta)
        
        mfc_f = min(abs(tft_f[k]) for k in range(1, n))
        mfc_g = min(abs(tft_g[k]) for k in range(1, n))
        
        delta = abs(mfc_g - 2 * mfc_f)
        bound = 10 * math.log(n) / beta
        
        results.append({
            "beta": beta,
            "delta": delta,
            "bound": bound
        })
    
    max_delta = max(result["delta"] for result in results)
    pass_rate = sum(1 for result in results if result["delta"] <= result["bound"]) / len(results)
    
    return {
        "metric_name": "Delta",
        "metric_value": max_delta,
        "instances_tested": 6 * n,
        "n_max": n,
        "conjecture_holds": pass_rate == 1.0,
        "counterexample": "" if pass_rate == 1.0 else f"beta={results[max(i for i, result in enumerate(results) if result['delta'] > result['bound'])]['beta']}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(6, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_delta = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_delta)**2 for result in results) / len(results))
    pass_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std={std_dev} support_fraction={pass_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"beta={result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")