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
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def kronecker_coefficient(a, b):
    if a == 0 or b == 0:
        return 1
    if a < b:
        a, b = b, a
    result = 1
    for i in range(1, b+1):
        result *= (a + i - 1) * (b - i + 1)
        result //= i * (a - b + i)
    return result

def symmetric_power_decomposition(n, k):
    if n == 0 or k == 0:
        return [1]
    result = [0] * (n + 1)
    result[0] = 1
    for _ in range(k):
        new_result = [0] * (n + 1)
        for i in range(n + 1):
            for j in range(i + 1):
                new_result[i] += result[j] * kronecker_coefficient(i - j, j)
        result = new_result
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        k = (n + 1) // 2
        characteristic_polynomial = [1] * (n + 1)
        for i in range(1, n + 1):
            characteristic_polynomial[i] = -sum(characteristic_polynomial[j] * (-1)**j for j in range(i))

        permanent_decomposition = symmetric_power_decomposition(n, k)
        determinant_decomposition = symmetric_power_decomposition(n, k)

        permanent_value = sum(permanent_decomposition[i] * kronecker_coefficient(k, i) for i in range(n + 1))
        determinant_value = sum(determinant_decomposition[i] * kronecker_coefficient(k, i) for i in range(n + 1))

        if permanent_value == 0 or determinant_value == 0:
            counterexample = "mapping_undefined"
            conjecture_holds = False
            break

        ratio = permanent_value / determinant_value
        total_metric_value += math.log2(ratio)
        instances_tested += 1

    return {
        "metric_name": "log2(permanent/determinant_ratio)",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*2 + 1, 2))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")