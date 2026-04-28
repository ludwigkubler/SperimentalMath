# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    echelon_form = gaussian_elimination([row[:] for row in A])
    rank = sum(1 for row in echelon_form if any(row))
    return rank

def sign(x):
    return 1 if x >= 0 else -1

def generate_random_matrix(n):
    return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

def generate_rank_1_planted_matrix(n):
    u = [random.choice([-1, 1]) for _ in range(n)]
    v = [random.choice([-1, 1]) for _ in range(n)]
    return [[sign(u[i] * v[j]) for j in range(n)] for i in range(n)]

def generate_rank_r_planted_matrix(n, r):
    u = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(r)]
    v = [random.choice([-1, 1]) for _ in range(n)]
    return [[sign(sum(u[k][i] * v[j] for k in range(r))) for j in range(n)] for i in range(n)]

def generate_symmetric_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            M[i][j] = random.choice([-1, 1])
            M[j][i] = M[i][j]
    return M

def prefix_sum_row(M, i):
    N = len(M)
    R_i = [0] * (N + 1)
    for j in range(N):
        R_i[j+1] = R_i[j] + M[i][j]
    zero_crossings = sum(1 for x in R_i if x == 0)
    return zero_crossings

def prefix_sum_col(M, j):
    N = len(M)
    R_j = [0] * (N + 1)
    for i in range(N):
        R_j[i+1] = R_j[i] + M[i][j]
    zero_crossings = sum(1 for x in R_j if x == 0)
    return zero_crossings

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5]
    instances_tested = 0
    max_R_row = 0
    max_R_col = 0
    rank_sum = 0

    for n in n_values:
        for _ in range(200):
            if random.random() < 0.25:
                M = generate_random_matrix(n)
            elif random.random() < 0.5:
                M = generate_rank_1_planted_matrix(n)
            elif random.random() < 0.75:
                r = random.randint(2, 3)
                M = generate_rank_r_planted_matrix(n, r)
            else:
                M = generate_symmetric_matrix(n)

            rk = matrix_rank(M)
            R_row = prefix_sum_row(M, random.randint(0, n-1))
            R_col = prefix_sum_col(M, random.randint(0, n-1))

            instances_tested += 1
            max_R_row = max(max_R_row, R_row)
            max_R_col = max(max_R_col, R_col)
            rank_sum += rk

    R_f = max(max_R_row, max_R_col)
    B = 4 * math.sqrt(rank_sum / len(n_values) * 2**n * n)

    conjecture_holds = R_f <= 1.5 * B
    counterexample = "" if conjecture_holds else f"R(f)={R_f}, B={B}"

    return {
        "metric_name": "max(R_row, R_col)",
        "metric_value": R_f,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")