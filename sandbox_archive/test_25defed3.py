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

def matrix_svd(A):
    n = len(A)
    m = len(A[0]) if n > 0 else 0

    # Compute A^T A
    A_T = matrix_transpose(A)
    A_T_A = matrix_multiply(A_T, A)

    # Compute eigenvalues and eigenvectors of A^T A
    # Using power iteration for simplicity (not exact)
    def power_iteration(M, num_iterations=100):
        b_k = [random.random() for _ in range(n)]
        for _ in range(num_iterations):
            b_k1 = [0.0] * n
            for i in range(n):
                for j in range(n):
                    b_k1[i] += M[i][j] * b_k[j]
            norm = math.sqrt(sum(x**2 for x in b_k1))
            if norm == 0:
                break
            b_k = [x / norm for x in b_k1]
        return b_k

    # Approximate singular values
    sigma = []
    for _ in range(min(n, m)):
        v = power_iteration(A_T_A)
        sigma.append(math.sqrt(sum(v[i] * A_T_A[i][i] * v[i] for i in range(n))))
        # Deflate A_T_A
        for i in range(n):
            for j in range(n):
                A_T_A[i][j] -= sigma[-1] * v[i] * v[j]

    # Sort singular values in descending order
    sigma.sort(reverse=True)

    return sigma

def compute_discrepancy(M):
    sigma = matrix_svd(M)
    N = len(M)
    p_i = [s**2 / (N**2) for s in sigma]

    # Compute F_M(t)
    def F_M(t):
        k = int(t * N)
        if k >= N:
            return 1.0
        return sum(p_i[:k+1])

    # Compute D_2 using Simpson's rule
    def integrand(t):
        return (F_M(t) - t)**2

    a, b = 0.0, 1.0
    n_points = 4 * N
    h = (b - a) / (n_points - 1)
    integral = integrand(a) + integrand(b)
    for i in range(1, n_points - 1):
        t = a + i * h
        if i % 2 == 1:
            integral += 4 * integrand(t)
        else:
            integral += 2 * integrand(t)
    integral *= h / 3
    D_2 = math.sqrt(integral)
    return D_2

def generate_matrix(N, ensemble_type, seed):
    random.seed(seed)
    if ensemble_type == 'iid':
        return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    elif ensemble_type == 'hadamard' and N in {16, 32}:
        # Sylvester-Hadamard matrix (simplified)
        H = [[1] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if bin(i & j).count('1') % 2 == 1:
                    H[i][j] = -1
        return H
    elif ensemble_type == 'padded_identity':
        M = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if i == j:
                    M[i][j] = 1 if i < N//2 else -1
                else:
                    M[i][j] = random.choice([-1, 1])
        return M
    elif ensemble_type == 'rank3':
        M = [[0] * N for _ in range(N)]
        for i in range(3):
            u = [random.choice([-1, 1]) for _ in range(N)]
            v = [random.choice([-1, 1]) for _ in range(N)]
            for k in range(N):
                for l in range(N):
                    M[k][l] += u[k] * v[l]
        # Add 8% random flips
        for i in range(N):
            for j in range(N):
                if random.random() < 0.08:
                    M[i][j] *= -1
        return M
    else:
        return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]

def run_trial(seed):
    random.seed(seed)
    N_values = [16, 24, 32, 40]
    ensemble_types = ['iid', 'hadamard', 'padded_identity', 'rank3']
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for N in N_values:
        for ensemble_type in ensemble_types:
            M = generate_matrix(N, ensemble_type, seed)
            D_2 = compute_discrepancy(M)
            if (1 - 4 * D_2) <= 0.02:
                continue
            sigma = matrix_svd(M)
            k = N // 2 + 1
            if k >= len(sigma):
                continue
            rho = sigma[k]**2 / (N * (1 - 4 * D_2))
            metric_values.append(rho)
            instances_tested += 1
            if rho < 0.05:
                conjecture_holds = False
                counterexample = f"N={N}, ensemble={ensemble_type}, rho={rho:.4f}"

    if not metric_values:
        return {
            "metric_name": "sigma_{N/2+1}^2 / (N*(1-4D_2))",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": True,
            "counterexample": ""
        }

    metric_value = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "sigma_{N/2+1}^2 / (N*(1-4D_2))",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **trial})}")
        if trial["instances_tested"] > 0:
            metric_values.append(trial["metric_value"])
            if not trial["conjecture_holds"]:
                conjecture_holds_all = False
                counterexample = trial["counterexample"]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for x in metric_values if x >= 0.10) / len(metric_values)

    if not conjecture_holds_all:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[0]}")
    elif support_fraction >= 0.8 and mean >= 0.10:
        print(f"RESULT: SUPPORTED mean={mean:.4f} std={std:.4f} support_fraction={support_fraction:.4f}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")