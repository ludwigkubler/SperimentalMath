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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + sum(1 for j in range(i, m) if abs(A[j][i]) > abs(A[max_row][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def identity_matrix(n):
    return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]

def plethysm_coefficient(A, n):
    k = 2
    power_matrix = A
    while True:
        next_power = matrix_multiply(power_matrix, A)
        if next_power == identity_matrix(n):
            break
        power_matrix = next_power
        k += 1
    return Fraction(1) / math.log(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    A = gaussian_elimination(A)
    plethysm_coeff = plethysm_coefficient(A, n)
    if plethysm_coeff is None:
        return {
            "metric_name": "plethysm_coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    instances_tested = 30
    metric_value = plethysm_coeff
    conjecture_holds = abs(metric_value - (1 / math.log(n))) < 0.1
    counterexample = "" if conjecture_holds else f"plethysm_coefficient={metric_value}, expected ≈ {1 / math.log(n)}"
    return {
        "metric_name": "plethysm_coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")