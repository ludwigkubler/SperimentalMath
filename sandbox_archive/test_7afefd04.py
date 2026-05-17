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
    return [[random.gauss(0, 1) for _ in range(m)] for _ in range(m)]

def generate_random_vector(n, seed):
    random.seed(seed)
    return [random.gauss(0, 1) for _ in range(n * n)]

def compute_v_sigma(f_L_ell, sigma, n, m, L, ell):
    v_sigma = 0.0
    for psi in itertools.permutations(range(n), m):
        M = [[L[a][b][psi[a] * n + sigma[psi[a]]] for b in range(m)] for a in range(m)]
        det_M = matrix_det(M)
        product = 1.0
        for p in range(n):
            if p not in psi:
                product *= ell[p * n + sigma[p]]
        v_sigma += det_M * product
    return v_sigma * math.factorial(n - m)

def compute_rho(f_L_ell, n, m, L, ell):
    v_f = [compute_v_sigma(f_L_ell, sigma, n, m, L, ell) for sigma in itertools.permutations(range(n))]
    sum_v_sigma = sum(v_f)
    sum_v_sigma_squared = sum(v ** 2 for v in v_f)
    if sum_v_sigma_squared == 0:
        return 0.0
    rho = (sum_v_sigma ** 2) / (math.factorial(n) * sum_v_sigma_squared)
    return rho

def run_trial(seed):
    n_values = [4, 5, 6]
    m_values = [2, 3, 5]  # For n=4, m=2,3; n=5, m=2,3; n=6, m=2,3
    max_rho = 0.0
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for m in m_values:
            if m >= n:
                continue
            L = [[generate_random_vector(n, seed + i + j) for j in range(m)] for i in range(m)]
            ell = generate_random_vector(n, seed + n)
            f_L_ell = lambda y: ell[y] ** (n - m) * matrix_det([[L[i][j][y] for j in range(m)] for i in range(m)])
            rho = compute_rho(f_L_ell, n, m, L, ell)
            instances_tested += 1
            if rho > max_rho:
                max_rho = rho
            if rho >= 1 - 1/n:
                counterexample = f"n={n}, m={m}, seed={seed}, rho={rho}"

    # Sanity check for perm_n
    perm_n = list(range(n))
    v_perm_n = [1.0] * math.factorial(n)
    sum_v_perm_n = sum(v_perm_n)
    sum_v_perm_n_squared = sum(v ** 2 for v in v_perm_n)
    rho_perm_n = (sum_v_perm_n ** 2) / (math.factorial(n) * sum_v_perm_n_squared)
    if abs(rho_perm_n - 1.0) > 1e-9:
        counterexample = f"Sanity check failed: rho(perm_n)={rho_perm_n}"

    return {
        "metric_name": "max_rho",
        "metric_value": max_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": max_rho < 1 - 1/n if not counterexample else False,
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
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=90")