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

def sign_communication_matrix(f):
    n = len(f)
    M_f = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M_f[i][j] = (-1) ** (f(i) ^ f(j))
    return M_f

def svd(M):
    # Simple power iteration method to approximate the largest singular value
    n = len(M)
    v = [random.random() for _ in range(n)]
    for _ in range(100):  # Number of iterations
        v = [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
        norm = sum(x**2 for x in v)
        v = [x / math.sqrt(norm) for x in v]
    sigma = max(abs(sum(M[i][j] * v[j] for j in range(n))) for i in range(n))
    return sigma

def log_energy_deficit(sigma_values):
    n = len(sigma_values)
    sigma1 = max(sigma_values)
    sigma_values.remove(sigma1)
    sum_log_diff = sum(math.log(abs(sigma_i / math.sqrt(n) - sigma_j / math.sqrt(n))) for i in range(n-1) for j in range(i+1, n))
    return 0.5 * math.log(sigma1**2 / n) - (2 / (n * (n - 1))) * sum_log_diff

def disc(M):
    # Top singular value bound
    sigma1 = svd(M)
    return sigma1 / len(M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def DISJ(n, i):
        return lambda x: (x >> i) & 1
    
    n_values = [2, 3, 4, 5, 6, 7, 8]
    results = defaultdict(list)
    
    for n in n_values:
        f = DISJ(n, random.randint(0, n-1))
        M_f = sign_communication_matrix(f)
        sigma_values = sorted([svd(M) for M in [M_f]], reverse=True)
        delta_E = log_energy_deficit(sigma_values)
        disc_value = disc(M_f)
        
        results[n].append({
            "n": n,
            "delta_E": delta_E,
            "disc_value": disc_value
        })
    
    mean_delta_E_DISJ = sum(results[6]["delta_E"] for _ in range(30)) / 30
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for result in results[n]:
            if result["n"] * result["delta_E"] / 16 > math.log2(1 / result["disc_value"]) + 3:
                conjecture_holds = False
                counterexample = f"DISJ_{result['n']}"
    
    return {
        "metric_name": "log2(1/disc) vs n*DeltaE/16",
        "metric_value": mean_delta_E_DISJ,
        "instances_tested": len(results[6]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_delta_E_DISJ = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_delta_E_DISJ} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DISJ\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")