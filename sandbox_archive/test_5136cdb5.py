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
    n = len(a)
    m = len(b[0])
    p = len(b)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_transpose(a):
    return [list(row) for row in zip(*a)]

def matrix_norm(a):
    return math.sqrt(sum(sum(x**2 for x in row) for row in a))

def svd(a):
    a = [list(row) for row in a]
    m = len(a)
    n = len(a[0]) if m > 0 else 0
    u = [[0.0] * m for _ in range(m)]
    vt = [[0.0] * n for _ in range(n)]
    s = [0.0] * min(m, n)

    for i in range(min(m, n)):
        s[i] = matrix_norm([row[i] for row in a])
        if s[i] == 0:
            continue
        for j in range(m):
            u[j][i] = a[j][i] / s[i]
        for j in range(i+1, n):
            aij = sum(a[k][i] * a[k][j] for k in range(m))
            for k in range(m):
                a[k][j] -= aij * u[k][i]

    for i in range(min(m, n)):
        for j in range(i+1, min(m, n)):
            if s[i] > s[j]:
                s[i], s[j] = s[j], s[i]
                for k in range(m):
                    u[k][i], u[k][j] = u[k][j], u[k][i]
                for k in range(n):
                    vt[i][k], vt[j][k] = vt[j][k], vt[i][k]

    return u, s, vt

def compute_tau(matrix):
    u, s, vt = svd(matrix)
    s1 = sum(s)
    s4 = sum(x**4 for x in s) ** 0.25
    if s4 == 0:
        return 0.0
    return 2 * math.log2(s1) - math.log2(s4)

def generate_disj_matrix(n):
    size = 2 ** n
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = 1 if z == 0 else 0
    return matrix

def generate_random_and_function(n, seed):
    random.seed(seed)
    size = 2 ** n
    func = [0] * size
    for i in range(size):
        if bin(i).count('1') == n // 2:
            func[i] = 1
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = func[z]
    return matrix

def generate_tensor_power_matrix(n, seed):
    random.seed(seed)
    size = 2 ** n
    func = [0] * size
    for i in range(size):
        if bin(i).count('1') == 1:
            func[i] = 1
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = func[z]
    return matrix

def compute_cc_upper_bound(matrix):
    n = int(math.log2(len(matrix)))
    rank = sum(1 for s in svd(matrix)[1] if s > 1e-10)
    return min(2 * n, math.ceil(math.log2(rank + 1)) + 4 * math.log2(len(matrix)))

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6, 7, 8])
    family = random.choice(['disj', 'random', 'tensor'])

    if family == 'disj':
        matrix = generate_disj_matrix(n)
        tau = compute_tau(matrix)
        exact_tau = n * math.log2(5 / math.sqrt(7))
        conjecture_holds = abs(tau - exact_tau) <= 1e-6 and 0.7 * n <= tau <= 1.0 * n
        counterexample = f"tau(M_DISJ_{n}) = {tau} not in [0.7n, 1.0n]" if not conjecture_holds else ""
    else:
        if family == 'random':
            matrix = generate_random_and_function(n, seed)
        else:
            matrix = generate_tensor_power_matrix(n, seed)
        tau = compute_tau(matrix)
        ub = compute_cc_upper_bound(matrix)
        conjecture_holds = tau <= 8 * ub + 16
        counterexample = f"tau(M_g) = {tau} > 8*ub(M_g) + 16 = {8*ub+16}" if not conjecture_holds else ""

    return {
        "metric_name": "tau",
        "metric_value": tau,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        if not result["conjecture_holds"] and not counterexample:
            counterexample = result["counterexample"]

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[conjecture_holds_counts]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")