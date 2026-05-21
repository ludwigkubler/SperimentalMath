# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        return A

    def sigma_max(A):
        U, _, Vt = gaussian_elimination([[A[i][j] ** 2 for j in range(len(A[0]))] for i in range(len(A))])
        max_val = 0
        for row in U:
            max_val = max(max_val, sum(row))
        return math.sqrt(max_val)

    def design_slices(n):
        l = math.ceil(math.log2(n))
        k = math.ceil(math.log2(math.log2(n)))
        m = n // (2 * k + 1)
        slices = []
        for _ in range(m):
            new_slice = random.sample(range(1, n+1), l)
            if all(len(set(new_slice) & set(slice)) <= k for slice in slices):
                slices.append(new_slice)
        return slices

    def indicator_function(x, y):
        return 1 - 2 * (x == y)

    def build_sigma_matrix(f, slices):
        m = len(slices)
        sigma_matrix = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i, m):
                x = [slices[i][j] for j in range(l)]
                y = [slices[j][j] for j in range(l)]
                sigma_matrix[i][j] = 1 - 2 * f(x, y)
                sigma_matrix[j][i] = sigma_matrix[i][j]
        return sigma_matrix

    def DISJ(x, y):
        return indicator_function(sum(x), sum(y))

    def EQ(x, y):
        return indicator_function(x, y)

    def INNER_PRODUCT(x, y):
        return indicator_function(sum(xi * yi for xi, yi in zip(x, y)), 0)

    def GREATER_THAN(x, y):
        return indicator_function(sum(x), sum(y)) > 0

    def uniform_random(x, y):
        return random.choice([-1, 1])

    functions = [DISJ, EQ, INNER_PRODUCT, GREATER_THAN, uniform_random]
    results = []
    
    for n in {12, 16, 20, 24, 28, 32, 36, 40}:
        slices = design_slices(n)
        for f in functions:
            sigma_matrix = build_sigma_matrix(f, slices)
            rho_value = sigma_max(sigma_matrix) / len(slices)
            results.append({
                "n": n,
                "f": f.__name__,
                "rho_value": rho_value
            })
    
    return {
        "metric_name": "ρ(f, D_n)",
        "metric_value": sum(result["rho_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["rho_value"] <= 4 for result in results if result["f"] == "DISJ"),
        "counterexample": "" if all(result["rho_value"] <= 4 for result in results if result["f"] == "DISJ") else "ρ(DISJ) > 4"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ρ(DISJ) > 4\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")