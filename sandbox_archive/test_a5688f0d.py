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

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, p):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(matrix, p)
    if det == 0:
        raise ValueError("Matrix is singular and does not have an inverse")
    det_inv = mod_inverse(det, p)
    for i in range(n):
        for j in range(n):
            minor = get_minor(matrix, i, j)
            adj[j][i] = (det_inv * (-1) ** (i + j) * determinant(minor, p)) % p
    return adj

def determinant(matrix, p):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for i in range(n):
        minor = get_minor(matrix, 0, i)
        det += ((-1) ** i * matrix[0][i] * determinant(minor, p)) % p
    return det

def get_minor(matrix, row, col):
    n = len(matrix)
    minor = []
    for i in range(n):
        if i == row:
            continue
        new_row = []
        for j in range(n):
            if j == col:
                continue
            new_row.append(matrix[i][j])
        minor.append(new_row)
    return minor

def is_p_adic_unit(a, p):
    return a % p != 0 and gcd(a, p) == 1

def minimal_order_of_p_adic_units(n, p):
    units = [a for a in range(1, p) if is_p_adic_unit(a, p)]
    min_order = float('inf')
    for unit in units:
        order = 1
        current = unit % p
        while current != 1:
            current = (current * unit) % p
            order += 1
        min_order = min(min_order, order)
    return min_order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            matrix = [[random.randint(1, p-1) for _ in range(n)] for _ in range(n)]
            det = determinant(matrix, p)
            if det == 0:
                continue
            min_order = minimal_order_of_p_adic_units(abs(det), p)
            total_metric_value += math.sqrt(n)
            instances_tested += 1

            if min_order > math.sqrt(n):
                conjecture_holds = False
                counterexample = f"n={n}, det(matrix)={det}, min_order={min_order}"
                break

    return {
        "metric_name": "sqrt(n)",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")