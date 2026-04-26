# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def max_plus(a, b):
    return a if a > b else b

def min_plus(a, b):
    return a if a < b else b

def tropical_polynomial(N, slopes, offset):
    f = [0] * N
    for i in range(1, N):
        f[i] = f[i-1] + slopes[i-1]
    return [f[i] + random.uniform(-5, 5) for i in range(N)] + [offset]

def max_plus_convolution(f, g):
    N = len(f)
    result = [0] * (2*N - 1)
    for i in range(N):
        for j in range(N):
            result[i+j] = max_plus(result[i+j], f[i] + g[j])
    return result[:N]

def min_max_plus_convolution(f, g):
    N = len(f)
    result = [0] * (2*N - 1)
    for i in range(N):
        for j in range(N):
            result[i-j+N-1] = max_plus(result[i-j+N-1], f[i] + g[j])
    return result[:N]

def tropical_fourier_transform(f, N):
    F = [0] * N
    for k in range(N):
        F[k] = max_plus_convolution([f[x] - k*x for x in range(N)], [1]*N)[k]
    return F

def minimal_fourier_coefficient(F):
    return min_plus(*F)

def discrepancy_measure(f):
    return max(f) - min(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    N_values = [16, 32, 64]
    results = []
    
    for N in N_values:
        slopes = sorted(random.uniform(-5, 5) for _ in range(N-1))
        f = tropical_polynomial(N, slopes, random.uniform(-5, 5))
        
        F = tropical_fourier_transform(f, N)
        G = tropical_fourier_transform(F, N)
        
        max_error = max(abs(G[x] - f[x]) for x in range(N))
        min_fc_f = minimal_fourier_coefficient(F)
        min_fc_g = minimal_fourier_coefficient(G)
        discrepancy_f = discrepancy_measure(f)
        
        results.append({
            "N": N,
            "max_error": max_error,
            "min_fc_f": min_fc_f,
            "min_fc_g": min_fc_g,
            "discrepancy_f": discrepancy_f
        })
    
    all_checks_passed = True
    for result in results:
        if result["max_error"] >= 1e-9 or abs(result["min_fc_f"] - result["min_fc_g"]) >= 1e-9 or result["discrepancy_f"] > abs(result["min_fc_f"]) + abs(result["min_fc_g"]):
            all_checks_passed = False
            break
    
    conjecture_holds = all_checks_passed
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_error",
        "metric_value": sum(result["max_error"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_error = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_error} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")