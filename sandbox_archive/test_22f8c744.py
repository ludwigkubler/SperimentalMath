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

def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_to_vector(m):
    return [m[i][j] for i in range(len(m)) for j in range(len(m[0]))]

def vector_to_matrix(v, w):
    return [[v[i * w + j] for j in range(w)] for i in range(w)]

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for i in range(n) if any(matrix[i][j] != 0 for j in range(n)))
    return rank

def compute_rho(P, w):
    identity = [[1 if i == j else 0 for j in range(w)] for i in range(w)]
    basis = [matrix_to_vector(identity)]
    for T in P:
        new_basis = []
        for b in basis:
            T_b = matrix_mult(vector_to_matrix(b, w), T)
            new_basis.append(matrix_to_vector(T_b))
        for b in basis:
            for T_b in new_basis:
                new_matrix = matrix_add(vector_to_matrix(b, w), vector_to_matrix(T_b, w))
                new_basis.append(matrix_to_vector(new_matrix))
        basis = [b for b in new_basis if b not in basis]
    rank = gaussian_elimination([basis[i] for i in range(len(basis))])
    return math.log2(rank + 1)

def generate_random_bp(n, w, seed):
    random.seed(seed)
    L = 4 * n
    P = []
    for _ in range(L):
        T = [[0] * w for _ in range(w)]
        for i in range(w):
            j = random.randint(0, w - 1)
            T[i][j] = 1
        P.append(T)
    return P

def generate_adversarial_bp(n):
    w = 2 ** (n + 1)
    P = []
    for _ in range(2 * n):
        T = [[0] * w for _ in range(w)]
        for i in range(w):
            T[i][i] = 1
        P.append(T)
    for _ in range(2 * n):
        T = [[0] * w for _ in range(w)]
        for i in range(w):
            T[i][(i + 1) % w] = 1
        P.append(T)
    return P

def generate_friendly_bp(n):
    w = 2
    P = []
    for _ in range(2 * n):
        T = [[0] * w for _ in range(w)]
        for i in range(w):
            T[i][i] = 1
        P.append(T)
    for _ in range(2 * n):
        T = [[0] * w for _ in range(w)]
        for i in range(w):
            T[i][(i + 1) % w] = 1
        P.append(T)
    return P

def run_trial(seed):
    random.seed(seed)
    n_values = [3, 4, 5, 6, 7, 8]
    w_values = [4, 8]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for w in w_values:
            for _ in range(30):
                P = generate_random_bp(n, w, seed)
                rho = compute_rho(P, w)
                metric_values.append(rho)
                instances_tested += 1
                if rho > 2 * math.log2(w + 1):
                    conjecture_holds = False
                    counterexample = f"Random BP with n={n}, w={w}, seed={seed} has rho={rho} > 2*log2(w+1)"

    for n in [2, 3, 4]:
        P = generate_adversarial_bp(n)
        rho = compute_rho(P, 2 ** (n + 1))
        metric_values.append(rho)
        instances_tested += 1
        if rho < n - 2:
            conjecture_holds = False
            counterexample = f"Adversarial BP with n={n} has rho={rho} < n-2"

    for n in range(2, 9):
        P = generate_friendly_bp(n)
        rho = compute_rho(P, 2)
        metric_values.append(rho)
        instances_tested += 1
        if rho > 2:
            conjecture_holds = False
            counterexample = f"Friendly BP with n={n} has rho={rho} > 2"

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    return {
        "metric_name": "rho",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")