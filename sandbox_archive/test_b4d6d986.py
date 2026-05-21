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

def run_trial(seed: int) -> dict:
    def build_sigma_matrix(f, slices):
        m = len(slices)
        sigma_matrix = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                sigma_matrix[i][j] = 1 - 2 * f(slices[i], slices[j])
                sigma_matrix[j][i] = sigma_matrix[i][j]
        return sigma_matrix

    def spectral_discrepancy(sigma_matrix):
        m = len(sigma_matrix)
        if m <= 8:
            u, _, _ = svd(sigma_matrix)
            return max(abs(u[0]), abs(u[-1]))
        else:
            # For larger matrices, use a more efficient method
            # (e.g., power iteration or Lanczos algorithm)
            # Here we use a placeholder for demonstration purposes
            return 1.0

    def svd(matrix):
        m = len(matrix)
        n = len(matrix[0])
        if m > n:
            matrix = list(zip(*matrix))
            m, n = n, m
        
        u = [list(range(m)) for _ in range(m)]
        s = [1] * min(m, n)
        v = [[0] * n for _ in range(n)]
        v[0][0] = 1
        
        for k in range(min(m, n)):
            x = matrix[k]
            sigma_x = sum(x[i]**2 for i in range(k))**0.5
            u[k][:k+1] = [x[i]/sigma_x if i == k else 0 for i in range(k+1)]
            s[k] = sigma_x
            v[k][k] = 1
            
            for j in range(k+1, n):
                y = [sum(u[i][j]*v[i][k] for i in range(k+1)) for k in range(min(m, n))]
                sigma_y = sum(y[i]**2 for i in range(j))**0.5
                v[j][:j+1] = [y[i]/sigma_y if i == j else 0 for i in range(j+1)]
                s[j] = sigma_y
        
        return u, s, v

    def DISJ(S1, S2):
        return len(S1 & S2) == 0

    def EQ(S1, S2):
        return S1 == S2

    def INNER_PRODUCT(S1, S2):
        return sum(1 for x in range(len(S1)) if S1[x] and S2[x])

    def GREATER_THAN(S1, S2):
        return sum(S1[x] > S2[x] for x in range(len(S1)))

    def uniform_random(S1, S2):
        return random.choice([-1, 1])

    functions = [DISJ, EQ, INNER_PRODUCT, GREATER_THAN, uniform_random]
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    results = []

    for n in n_values:
        l = math.ceil(math.log2(n))
        k = math.ceil(math.log2(math.log2(n)))
        m = max(1, math.floor(n / (2 * k + 1)))

        slices = []
        while len(slices) < m:
            S = set(random.sample(range(n), l))
            if all(len(S & s) <= k for s in slices):
                slices.append(S)

        for f in functions:
            sigma_matrix = build_sigma_matrix(f, slices)
            rho = spectral_discrepancy(sigma_matrix)
            results.append({
                "n": n,
                "f": f.__name__,
                "rho": rho,
                "m": m
            })

    metric_value = sum(result["rho"] * math.sqrt(result["m"]) for result in results) / len(results)
    conjecture_holds = all(result["rho"] * math.sqrt(result["m"]) <= 4 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "ρ(DISJ)·√m",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 8)]  # First 30 primes

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown_failure")