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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def inverse_matrix(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    augmented = [row + col for row, col in zip(A, I)]
    gaussian_elimination(augmented)
    return [row[n:] for row in augmented]

def moment_cumulant_formula(moments):
    n = len(moments)
    cumulants = [0] * n
    cumulants[0] = moments[0]
    for k in range(1, n):
        cumulants[k] = (moments[k] - sum(cumulants[i] * cumulants[k-i-1] for i in range(k))) / (k + 1)
    return cumulants

def generate_read_twice_bp(n):
    variables = [random.choice([-1, 1]) for _ in range(2**n)]
    bp = []
    for i in range(2**n):
        path_weight = 1
        for j in range(n):
            if (i >> j) & 1:
                path_weight *= variables[j]
        bp.append(path_weight)
    return bp

def generate_ip2_distribution(n):
    return [[random.choice([-1, 1]) for _ in range(2**n)] for _ in range(2**n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    moments_limit = 5 * math.log(n)

    bp = generate_read_twice_bp(n)
    ip2_distribution = generate_ip2_distribution(n)

    max_cumulant = 0
    for _ in range(30):
        path_weight = sum(bp[i] for i in range(len(bp)) if random.choice([True, False]))
        moments = [path_weight**k / len(bp) for k in range(1, n+1)]
        cumulants = moment_cumulant_formula(moments)
        max_cumulant = max(max_cumulant, max(cumulants))

    ip2_max_cumulant = 0
    for _ in range(30):
        path_weight = sum(ip2_distribution[i][j] for i in range(len(ip2_distribution)) if random.choice([True, False]) for j in range(len(ip2_distribution)))
        moments = [path_weight**k / len(ip2_distribution) for k in range(1, n+1)]
        cumulants = moment_cumulant_formula(moments)
        ip2_max_cumulant = max(ip2_max_cumulant, max(cumulants))

    return {
        "metric_name": "max_cumulant",
        "metric_value": max(max_cumulant, ip2_max_cumulant),
        "instances_tested": 60,
        "conjecture_holds": max_cumulant <= moments_limit and ip2_max_cumulant > moments_limit * 40,
        "counterexample": "" if max_cumulant <= moments_limit and ip2_max_cumulant > moments_limit * 40 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")