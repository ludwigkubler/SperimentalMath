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

def matrix_det(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in matrix[1:]]
        det += ((-1) ** col) * matrix[0][col] * matrix_det(minor)
    return det

def generate_permutation(n):
    perm = list(range(n))
    random.shuffle(perm)
    return perm

def generate_random_matrix(n, m, seed):
    random.seed(seed)
    matrix = [[random.gauss(0, 1) for _ in range(m)] for _ in range(m)]
    return matrix

def generate_random_linear_form(n, seed):
    random.seed(seed)
    linear_form = [random.gauss(0, 1) for _ in range(n * n)]
    return linear_form

def compute_v_sigma(f_L_l, n, m, sigma, L, ell):
    v_sigma = 0
    for psi in itertools.permutations(range(n), m):
        det_M = matrix_det([[L[a][b] for b in range(m)] for a in range(m)])
        product = 1
        for p in range(n):
            if p not in psi:
                product *= ell[p * n + sigma[p]]
        v_sigma += det_M * product
    return v_sigma

def compute_rho(f_L_l, n, m, L, ell):
    v = [compute_v_sigma(f_L_l, n, m, sigma, L, ell) for sigma in itertools.permutations(range(n))]
    sum_v = sum(v)
    sum_v_squared = sum([x ** 2 for x in v])
    if sum_v_squared == 0:
        return 0
    rho = (sum_v ** 2) / (math.factorial(n) * sum_v_squared)
    return rho

def run_trial(seed):
    n_values = [4, 5, 6]
    m_values = [2, 3, 4, 5]
    max_rho = 0
    counterexample = ""
    for n in n_values:
        for m in m_values:
            if m >= n:
                continue
            L = generate_random_matrix(n, m, seed)
            ell = generate_random_linear_form(n, seed)
            rho = compute_rho(None, n, m, L, ell)
            if rho > max_rho:
                max_rho = rho
            if rho >= 1 - 1 / n:
                counterexample = f"n={n}, m={m}, seed={seed}, rho={rho}"
                break
        if counterexample:
            break
    conjecture_holds = max_rho < 1 - 1 / n if not counterexample else False
    return {
        "metric_name": "max_rho",
        "metric_value": max_rho,
        "instances_tested": len(n_values) * len(m_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        results.append(result)
        print(f"TRIAL: {result}")
    metric_values = [result["metric_value"] for result in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [result["counterexample"] for result in results if result["counterexample"]]
        if counterexamples:
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={results[0]['seed']}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_data")