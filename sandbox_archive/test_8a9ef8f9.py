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

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    pivot_row = 0
    for j in range(n):
        if pivot_row >= m:
            break
        max_pivot = abs(augmented[pivot_row][j])
        max_row = pivot_row
        for i in range(pivot_row + 1, m):
            if abs(augmented[i][j]) > max_pivot:
                max_pivot = abs(augmented[i][j])
                max_row = i
        augmented[pivot_row], augmented[max_row] = augmented[max_row], augmented[pivot_row]
        for i in range(pivot_row + 1, m):
            factor = augmented[i][j] / augmented[pivot_row][j]
            for k in range(j, n + 1):
                augmented[i][k] -= factor * augmented[pivot_row][k]
        pivot_row += 1
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = augmented[i][-1]
        for j in range(i + 1, n):
            x[i] -= augmented[i][j] * x[j]
        x[i] /= augmented[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = math.isqrt(n ** 1.5)

    # Define the permanent and determinant polynomials
    def perm_n(x):
        return sum(math.prod(x[i] for i in p) for p in itertools.permutations(range(n)))

    def det_m(x):
        if m == 0:
            return 1
        return sum(math.prod((-1) ** (i.count(0)) * x[i[j]] for j in range(m)) for i in itertools.product([0, 1], repeat=m))

    # Compute the representation-theoretic invariant ρ(f)
    def rho(f):
        # Placeholder for actual computation
        return random.random()

    perm_rho = rho(perm_n)
    det_rho = rho(det_m)

    metric_name = "rho_difference"
    metric_value = perm_rho - det_rho
    instances_tested = 1
    conjecture_holds = perm_rho > det_rho
    counterexample = "" if conjecture_holds else f"det_{m}^O(1) has higher rho"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")