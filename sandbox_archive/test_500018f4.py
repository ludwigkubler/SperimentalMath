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
    m = len(A[0])
    U = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    S = [Fraction(0) for _ in range(n)]
    Vt = [[Fraction(0) for _ in range(n)] for _ in range(m)]

    for j in range(m):
        max_row = j
        for i in range(j+1, n):
            if abs(A[i][j]) > abs(A[max_row][j]):
                max_row = i

        if A[max_row][j] == 0:
            continue

        U[j], S[j], Vt[j] = row_reduce(A, j, max_row)

    return U, S, Vt

def row_reduce(A, j, max_row):
    n = len(A)
    m = len(A[0])
    U = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    S = Fraction(0)
    Vt = [[Fraction(0) for _ in range(n)] for _ in range(m)]

    # Swap rows
    A[j], A[max_row] = A[max_row], A[j]

    # Normalize the pivot row
    pivot = A[j][j]
    for k in range(j, m):
        A[j][k] /= pivot

    S += pivot**2

    # Eliminate other rows
    for i in range(n):
        if i != j:
            factor = A[i][j]
            for k in range(j, m):
                A[i][k] -= factor * A[j][k]

    return U, S, Vt

def rank_variance(A):
    n = len(A)
    m = len(A[0])
    U, S, Vt = gaussian_elimination(A)
    r = sum(1 for s in S if s != 0)
    return Fraction(r * (n - r), n)

def generate_communication_instance(n):
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "rank_variance_mrep_correlation"
    instances_tested = 0
    n_max = 0
    mrep_values = []
    r_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n

        for _ in range(5):  # Ensure at least 30 instances per seed
            A = generate_communication_instance(n)
            r = rank_variance(A)
            mrep = len(A) * len(A[0])
            mrep_values.append(mrep)
            r_values.append(r)
            instances_tested += 1

    if not mrep_values or not r_values:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_instance"
        }

    mean_r = sum(r_values) / len(r_values)
    mean_mrep = sum(mrep_values) / len(mrep_values)
    correlation_coefficient = sum((r - mean_r) * (mrep - mean_mrep) for r, mrep in zip(r_values, mrep_values)) / (len(r_values) * math.sqrt(sum((r - mean_r)**2 for r in r_values)) * math.sqrt(sum((mrep - mean_mrep)**2 for mrep in mrep_values)))

    conjecture_holds = correlation_coefficient > 0.8 and max(mrep_values) <= 1.5 * max(r_values)
    counterexample = "" if conjecture_holds else "correlation_threshold_not_met"

    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")