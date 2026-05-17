# auto-injected by SEC sandbox
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
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
    a = [[float(x) for x in row] for row in a]
    m = len(a)
    n = len(a[0]) if m > 0 else 0
    u = [[0.0 for _ in range(m)] for _ in range(m)]
    vt = [[0.0 for _ in range(n)] for _ in range(n)]
    s = [0.0] * min(m, n)

    # Simple SVD implementation for small matrices
    at = matrix_transpose(a)
    ata = matrix_mult(at, a)
    u = [[0.0 for _ in range(m)] for _ in range(m)]
    for i in range(m):
        u[i][i] = 1.0

    # Power iteration for dominant singular value
    b = [row[:] for row in a]
    for i in range(min(m, n)):
        if i >= len(b) or i >= len(b[0]):
            break
        s[i] = matrix_norm([row[i] for row in b])
        if s[i] == 0:
            continue
        for j in range(len(b)):
            if j >= len(b[0]):
                break
            b[j][i] /= s[i]
        if i + 1 < min(m, n):
            q = [row[i+1] for row in b]
            for j in range(i+1):
                q[j] = 0.0
            q_norm = matrix_norm(q)
            if q_norm > 0:
                for j in range(len(q)):
                    q[j] /= q_norm
                for j in range(len(b)):
                    if j >= len(b[0]):
                        break
                    b[j][i+1] -= q[j] * q_norm

    # Construct vt
    for i in range(min(m, n)):
        if i >= len(vt) or i >= len(vt[0]):
            break
        vt[i][i] = 1.0

    return u, s, vt

def compute_tau(matrix):
    u, s, vt = svd(matrix)
    s1 = sum(s)
    s4 = sum(x**4 for x in s) ** (1/4)
    if s4 == 0:
        return 0.0
    tau = math.log2(s1**2 / s4)
    return tau

def generate_disj_matrix(n):
    size = 2 ** n
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = 1 if z == 0 else 0
    return matrix

def generate_and_matrix(n, seed):
    random.seed(seed)
    size = 2 ** n
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = 1 if z == (1 << n) - 1 else 0
    return matrix

def generate_random_and_matrix(n, seed):
    random.seed(seed)
    size = 2 ** n
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = random.choice([0, 1])
    return matrix

def generate_tensor_and_matrix(n, seed):
    random.seed(seed)
    size = 2 ** n
    matrix = [[0] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            z = x & y
            matrix[x][y] = (z % 3) + 1
    return matrix

def compute_cc_upper_bound(matrix):
    n = int(math.log2(len(matrix)))
    rank = sum(1 for s in svd(matrix)[1] if s > 1e-10)
    return min(2 * n, math.ceil(math.log2(rank + 1)) + 4 * math.log2(len(matrix)))

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6, 7, 8])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test DISJ matrix
    matrix = generate_disj_matrix(n)
    tau = compute_tau(matrix)
    expected_tau = n * math.log2(5 / math.sqrt(7))
    if abs(tau - expected_tau) > 1e-6 or tau / n < 0.7 or tau / n > 1.0:
        conjecture_holds = False
        counterexample = f"DISJ matrix tau={tau} not in [0.7n,1.0n] for n={n}"

    # Test AND matrices
    for family in [generate_and_matrix, generate_random_and_matrix, generate_tensor_and_matrix]:
        matrix = family(n, seed)
        tau = compute_tau(matrix)
        ub = compute_cc_upper_bound(matrix)
        if tau > 8 * ub + 16:
            conjecture_holds = False
            counterexample = f"{family.__name__} tau={tau} > 8*ub+16 for n={n}"
            break

    instances_tested += 1

    return {
        "metric_name": "tau",
        "metric_value": tau,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    metric_values = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        results.append(result)
        metric_values.append(result["metric_value"])

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")