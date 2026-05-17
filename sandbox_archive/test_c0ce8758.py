# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_transpose(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]

def matrix_norm(a):
    return math.sqrt(sum(sum(x**2 for x in row) for row in a))

def svd(a):
    a = [[float(x) for x in row] for row in a]
    m = len(a)
    n = len(a[0])
    u = [[0.0] * m for _ in range(m)]
    vt = [[0.0] * n for _ in range(n)]
    s = [0.0] * min(m, n)

    for i in range(min(m, n)):
        s[i] = matrix_norm([row[i] for row in a])
        if s[i] == 0:
            continue
        for j in range(m):
            u[j][i] = a[j][i] / s[i]
        for j in range(i + 1, n):
            t = sum(u[k][i] * a[k][j] for k in range(m))
            for k in range(m):
                a[k][j] -= t * u[k][i]

    for i in range(min(m, n)):
        for j in range(i + 1, n):
            vt[i][j] = a[i][j] / s[i]
        vt[i][i] = 1.0

    return u, s, vt

def compute_tau(a):
    u, s, vt = svd(a)
    s1 = sum(s)
    s4 = sum(x**4 for x in s)**0.25
    if s4 == 0:
        return 0.0
    return 2 * math.log2(s1) - math.log2(s4)

def generate_disj_matrix(n):
    size = 2**n
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            matrix[x][y] = 1 if not (x & y) else 0
    return matrix

def generate_random_and_function(n, seed):
    random.seed(seed)
    size = 2**n
    ones = set(random.sample(range(size), size // 2))
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            matrix[x][y] = 1 if (x & y) in ones else 0
    return matrix

def generate_tensor_power_matrix(n, seed):
    random.seed(seed)
    size = 2**n
    base_size = 2
    base_matrix = [[random.randint(0, 1) for _ in range(base_size)] for _ in range(base_size)]
    matrix = base_matrix
    for _ in range(n // 2):
        matrix = matrix_mult(matrix, base_matrix)
    return matrix

def compute_ub(a):
    rank = sum(1 for x in a if any(x))
    n = len(a)
    return min(2 * n, math.ceil(math.log2(rank + 1)) + 4 * math.log2(n))

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6, 7, 8])
    family = random.choice(['disj', 'random', 'tensor'])

    if family == 'disj':
        matrix = generate_disj_matrix(n)
        tau = compute_tau(matrix)
        expected_tau = n * math.log2(5 / math.sqrt(7))
        conjecture_holds = abs(tau - expected_tau) <= 1e-6 and 0.7 * n <= tau <= 1.0 * n
        counterexample = "" if conjecture_holds else f"tau(M_DISJ_{n}) = {tau} not in [0.7n, 1.0n]"
    else:
        if family == 'random':
            matrix = generate_random_and_function(n, seed)
        else:
            matrix = generate_tensor_power_matrix(n, seed)
        tau = compute_tau(matrix)
        ub = compute_ub(matrix)
        conjecture_holds = tau <= 8 * ub + 16
        counterexample = "" if conjecture_holds else f"tau(M_g) = {tau} > 8·ub(M_g) + 16"

    return {
        "metric_name": "tau",
        "metric_value": tau,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failure = next((r for r in results if not r["conjecture_holds"]), None)
        if first_failure:
            print(f"RESULT: FALSIFIED counterexample=\"{first_failure['counterexample']}\" first_failing_seed={seeds[results.index(first_failure)]}")
        else:
            print("RESULT: INCONCLUSIVE reason=unknown")