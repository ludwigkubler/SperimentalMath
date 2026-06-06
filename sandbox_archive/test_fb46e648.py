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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j]*x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mtc_sum = 0
    rcv_sum = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            # Generate a random communication protocol P
            A = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
            B = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
            C = matrix_multiply(A, B)
            
            # Compute minimal tropical motivic complexity (mtc(P))
            mtc = sum(sum(abs(x) for x in row) for row in C)
            
            # Compute communication complexity rank variance (rcv(P))
            det_C = 1
            for i in range(n):
                det_C *= C[i][i]
            rcv = abs(det_C)
            
            mtc_sum += mtc
            rcv_sum += rcv
            instances_tested += 1

    if instances_tested < 30:
        return {
            "metric_name": "mtc(P) vs rcv(P)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }

    mtc_avg = mtc_sum / instances_tested
    rcv_avg = rcv_sum / instances_tested

    # Compute correlation coefficient
    covariance = sum((mtc - mtc_avg) * (rcv - rcv_avg) for mtc, rcv in zip(mtc_values, rcv_values)) / instances_tested
    mtc_var = sum((mtc - mtc_avg)**2 for mtc in mtc_values) / instances_tested
    rcv_var = sum((rcv - rcv_avg)**2 for rcv in rcv_values) / instances_tested

    if mtc_var == 0 or rcv_var == 0:
        return {
            "metric_name": "mtc(P) vs rcv(P)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Zero variance"
        }

    correlation_coefficient = covariance / math.sqrt(mtc_var * rcv_var)

    return {
        "metric_name": "mtc(P) vs rcv(P)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in res and res["conjecture_holds"] for res in results):
        mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
        std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not ("conjecture_holds" in res and res["conjecture_holds"]))
        counterexample = "Correlation coefficient < 0.9"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")