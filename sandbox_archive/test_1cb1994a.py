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

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scale(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def matrix_norm(A):
    return math.sqrt(sum(sum(a * a for a in row) for row in A))

def matrix_identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_copy(A):
    return [row[:] for row in A]

def matrix_svd(A):
    n = len(A)
    m = len(A[0])
    if n < m:
        A = matrix_transpose(A)
        n, m = m, n
        transpose = True
    else:
        transpose = False

    U = matrix_identity(n)
    V = matrix_identity(m)

    for i in range(min(n, m)):
        for j in range(i + 1, n):
            if A[j][i] != 0:
                break
        else:
            continue

        if j != i:
            A[i], A[j] = A[j], A[i]
            U[i], U[j] = U[j], U[i]

        for k in range(i + 1, n):
            if A[k][i] == 0:
                continue
            factor = Fraction(A[k][i], A[i][i])
            for l in range(i, m):
                A[k][l] -= factor * A[i][l]
            for l in range(n):
                U[k][l] -= factor * U[i][l]

    for i in range(min(n, m)):
        if A[i][i] == 0:
            continue
        factor = 1 / A[i][i]
        for j in range(i, m):
            A[i][j] *= factor
        for j in range(n):
            U[i][j] *= factor

    for i in range(min(n, m)):
        for j in range(i + 1, min(n, m)):
            if A[i][j] == 0:
                continue
            factor = Fraction(A[i][j], A[j][j])
            for k in range(j, m):
                A[i][k] -= factor * A[j][k]
            for k in range(n):
                U[i][k] -= factor * U[j][k]

    sigma = [A[i][i] for i in range(min(n, m))]

    if transpose:
        U, V = V, U

    return U, sigma, V

def generate_random_matrix(n, seed):
    random.seed(seed)
    return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

def generate_sylvester_hadamard(n, seed):
    random.seed(seed)
    if n not in {16, 32}:
        return generate_random_matrix(n, seed)
    H = [[1] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (i & j) != 0:
                H[i][j] = -1
    return H

def generate_padded_identity(n, seed):
    random.seed(seed)
    k = n // 2
    M = [[0] * n for _ in range(n)]
    for i in range(k):
        M[i][i] = 1
        M[i + k][i + k] = -1
    for i in range(n):
        for j in range(n):
            if random.random() < 0.1:
                M[i][j] *= -1
    return M

def generate_rank3_matrix(n, seed):
    random.seed(seed)
    M = [[0] * n for _ in range(n)]
    for i in range(3):
        u = [random.choice([-1, 1]) for _ in range(n)]
        v = [random.choice([-1, 1]) for _ in range(n)]
        for j in range(n):
            for k in range(n):
                M[j][k] += u[j] * v[k]
    for i in range(n):
        for j in range(n):
            if random.random() < 0.08:
                M[i][j] *= -1
    return M

def compute_discrepancy(M):
    U, sigma, V = matrix_svd(M)
    n = len(M)
    p = [s * s / (n * n) for s in sigma]
    F_M = [sum(p[:i + 1]) for i in range(n)]
    D_2 = 0.0
    for i in range(1, 4 * n):
        t = i / (4 * n)
        F_t = F_M[min(int(t * n), n - 1)]
        D_2 += (F_t - t) ** 2
    D_2 = math.sqrt(D_2 / (4 * n))
    return D_2

def run_trial(seed):
    random.seed(seed)
    n_values = [16, 24, 32, 40]
    results = []
    for n in n_values:
        matrices = [
            generate_random_matrix(n, seed),
            generate_sylvester_hadamard(n, seed),
            generate_padded_identity(n, seed),
            generate_rank3_matrix(n, seed)
        ]
        for M in matrices:
            D_2 = compute_discrepancy(M)
            if (1 - 4 * D_2) <= 0.02:
                continue
            U, sigma, V = matrix_svd(M)
            k = n // 2
            sigma_k = sigma[k]
            rho = (sigma_k ** 2) / (n * (1 - 4 * D_2))
            results.append(rho)
    if not results:
        return {
            "metric_name": "sigma_{N/2+1}^2 / (N * (1 - 4 * D_2))",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": True,
            "counterexample": ""
        }
    median_rho = sorted(results)[len(results) // 2]
    min_rho = min(results)
    conjecture_holds = median_rho >= 0.10 and min_rho >= 0.05
    counterexample = f"rho={min_rho}" if min_rho < 0.05 else ""
    return {
        "metric_name": "sigma_{N/2+1}^2 / (N * (1 - 4 * D_2))",
        "metric_value": median_rho,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trial["seed"] = seed
        print(f"TRIAL: {trial}")
        trials.append(trial)
    metric_values = [trial["metric_value"] for trial in trials if trial["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_non_vacuous_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [trial["counterexample"] for trial in trials if trial["counterexample"]]
        if counterexamples:
            first_failing_seed = next(trial["seed"] for trial in trials if trial["counterexample"])
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")