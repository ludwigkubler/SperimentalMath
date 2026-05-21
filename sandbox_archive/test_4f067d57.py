# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    def spectral_discrepancy(sigma_matrix):
        m = len(sigma_matrix)
        u, _, _ = svd(sigma_matrix)
        sigma_x = sum(u[i][i] for i in range(m))
        if sigma_x == 0:
            return float('inf')  # Handle division by zero gracefully
        rho = max(abs(x) for x in u[k][:k+1]) / m
        return rho

    def svd(matrix):
        m, n = len(matrix), len(matrix[0])
        U = [[0] * n for _ in range(m)]
        S = [0] * min(m, n)
        V = [[0] * m for _ in range(n)]

        # Compute the covariance matrix
        AAT = [[sum(a[i] * b[j] for a, b in zip(row_a, row_b)) for j in range(n)] for row_a in matrix]
        ATA = [[sum(a[i] * b[j] for a, b in zip(col_a, col_b)) for j in range(m)] for col_a in transpose(matrix)]

        # Perform SVD on AAT
        U_AAT, _, Vt_AAT = svd_helper(AAT)
        U[:m][:n] = U_AAT
        V[:n][:m] = Vt_AAT

        # Extract singular values from the diagonal of sigma matrix
        for i in range(min(m, n)):
            S[i] = math.sqrt(AAT[i][i])

        return U, S, V

    def svd_helper(matrix):
        m, n = len(matrix), len(matrix[0])
        U = [[0] * n for _ in range(m)]
        S = [0] * min(m, n)
        Vt = [[0] * m for _ in range(n)]

        # Compute the covariance matrix
        AAT = [[sum(a[i] * b[j] for a, b in zip(row_a, row_b)) for j in range(n)] for row_a in matrix]
        ATA = [[sum(a[i] * b[j] for a, b in zip(col_a, col_b)) for j in range(m)] for col_a in transpose(matrix)]

        # Perform SVD on AAT
        U_AAT, _, Vt_AAT = svd_helper(AAT)
        U[:m][:n] = U_AAT
        V[:n][:m] = Vt_AAT

        # Extract singular values from the diagonal of sigma matrix
        for i in range(min(m, n)):
            S[i] = math.sqrt(AAT[i][i])

        return U, S, Vt

    def transpose(matrix):
        m, n = len(matrix), len(matrix[0])
        T = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                T[j][i] = matrix[i][j]
        return T

    def generate_design(n, l, k):
        design = []
        while len(design) < n // (2 * k + 1):
            S = random.sample(range(1, n+1), l)
            if all(len(set(S).intersection(set(s))) <= k for s in design):
                design.append(S)
        return design

    def generate_function(n):
        functions = {
            'DISJ': lambda x, y: 1 if len(x.intersection(y)) > 0 else -1,
            'EQ': lambda x, y: 1 if x == y else -1,
            'INNER_PRODUCT mod 2': lambda x, y: (sum(a * b for a, b in zip(x, y))) % 2,
            'GREATER_THAN': lambda x, y: 1 if sum(1 for a, b in zip(x, y) if a > b) > len(x) // 2 else -1,
            'uniform-random': lambda _, __: random.choice([-1, 1])
        }
        return functions[random.choice(list(functions.keys()))]

    def build_sigma_matrix(design, f):
        m = len(design)
        sigma_matrix = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i+1, m):
                sigma_matrix[i][j] = 1 - 2 * f(set(design[i]), set(design[j]))
                sigma_matrix[j][i] = sigma_matrix[i][j]
        return sigma_matrix

    random.seed(seed)
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    results = []

    for n in n_values:
        l = math.ceil(math.log2(n))
        k = math.ceil(math.log2(math.log2(n)))
        m = n // (2 * k + 1)

        design = generate_design(n, l, k)
        f = generate_function(n)
        sigma_matrix = build_sigma_matrix(design, f)
        rho = spectral_discrepancy(sigma_matrix)

        results.append({
            "metric_name": "spectral_discrepancy",
            "metric_value": rho,
            "instances_tested": 1,
            "conjecture_holds": True if (f.__name__ == 'DISJ' and rho <= 4 * math.sqrt(m)) or (f.__name__ == 'EQ' and rho >= 1 - 6 / m) else False,
            "counterexample": ""
        })

    return {
        "seed": seed,
        "metric_name": "spectral_discrepancy",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

        if not trial_result["conjecture_holds"]:
            counterexample = f"{trial_result['metric_name']}({trial_result['seed']})={trial_result['metric_value']}"
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={trial_result['seed']}")
            sys.exit(0)

        results.append(trial_result["metric_value"])

    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = 1.0

    print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")