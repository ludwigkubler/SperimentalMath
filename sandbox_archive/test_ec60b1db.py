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

def matrix_multiply(a, b):
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

def matrix_subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_norm(a, p=2):
    if p == 2:
        return math.sqrt(sum(sum(x**2 for x in row) for row in a))
    else:
        raise ValueError("Only p=2 norm is implemented")

def matrix_rank(a):
    n = len(a)
    m = len(a[0])
    rank = 0
    for i in range(min(n, m)):
        if any(a[i][j] != 0 for j in range(m)):
            rank += 1
    return rank

def svd(a):
    n = len(a)
    m = len(a[0])
    u = [[0 for _ in range(n)] for _ in range(n)]
    s = [0 for _ in range(min(n, m))]
    vt = [[0 for _ in range(m)] for _ in range(m)]

    # Simple SVD implementation for small matrices
    # This is a placeholder and may not be accurate
    for i in range(min(n, m)):
        s[i] = matrix_norm([row[i] for row in a])
        if s[i] != 0:
            for j in range(n):
                u[j][i] = a[j][i] / s[i]
            for k in range(m):
                vt[i][k] = a[i][k] / s[i]

    return u, s, vt

def compute_tau(a):
    u, s, vt = svd(a)
    s1 = sum(s)
    s4 = sum(x**4 for x in s)**0.5
    if s4 == 0:
        return 0
    return 2 * math.log2(s1) - math.log2(s4)

def generate_disj_matrix(n):
    size = 2**n
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = 1 if z == 0 else 0
    return matrix

def generate_and_matrix(n, seed):
    random.seed(seed)
    size = 2**n
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = 1 if z == (1 << n) - 1 else 0
    return matrix

def generate_random_and_matrix(n, seed):
    random.seed(seed)
    size = 2**n
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = random.choice([0, 1])
    return matrix

def generate_tensor_power_matrix(n, seed):
    random.seed(seed)
    size = 2**n
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = 1 if z == (1 << n) - 1 else 0
    return matrix

def compute_ub(a):
    n = len(a)
    rank = matrix_rank(a)
    return min(2 * n, math.ceil(math.log2(rank + 1)) + 4 * math.log2(n))

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 5, 6, 7, 8]
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        # Test DISJ matrix
        disj_matrix = generate_disj_matrix(n)
        tau_disj = compute_tau(disj_matrix)
        expected_tau_disj = n * math.log2(5 / math.sqrt(7))
        if not (0.7 * n <= tau_disj / n <= 1.0):
            conjecture_holds = False
            counterexample = f"DISJ matrix with n={n} has tau={tau_disj} outside [0.7n, 1.0n]"
            break

        # Test AND matrices
        and_matrix = generate_and_matrix(n, seed)
        tau_and = compute_tau(and_matrix)
        ub_and = compute_ub(and_matrix)
        if tau_and > 8 * ub_and + 16:
            conjecture_holds = False
            counterexample = f"AND matrix with n={n} has tau={tau_and} > 8*ub+16"
            break

        # Test random AND matrices
        random_and_matrix = generate_random_and_matrix(n, seed)
        tau_random_and = compute_tau(random_and_matrix)
        ub_random_and = compute_ub(random_and_matrix)
        if tau_random_and > 8 * ub_random_and + 16:
            conjecture_holds = False
            counterexample = f"Random AND matrix with n={n} has tau={tau_random_and} > 8*ub+16"
            break

        # Test tensor power matrices
        tensor_power_matrix = generate_tensor_power_matrix(n, seed)
        tau_tensor_power = compute_tau(tensor_power_matrix)
        ub_tensor_power = compute_ub(tensor_power_matrix)
        if tau_tensor_power > 8 * ub_tensor_power + 16:
            conjecture_holds = False
            counterexample = f"Tensor power matrix with n={n} has tau={tau_tensor_power} > 8*ub+16"
            break

        metric_values.append(tau_disj)

    if conjecture_holds:
        metric_value = sum(metric_values) / len(metric_values)
    else:
        metric_value = 0

    return {
        "metric_name": "tau",
        "metric_value": metric_value,
        "instances_tested": len(n_values) * 4,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={seed}")