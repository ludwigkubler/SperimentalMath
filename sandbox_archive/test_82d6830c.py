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
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_transpose(m):
    return [list(row) for row in zip(*m)]

def matrix_trace(m):
    return sum(m[i][i] for i in range(len(m)))

def matrix_power(m, k):
    n = len(m)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    for _ in range(k):
        result = matrix_mult(result, m)
    return result

def compute_moments(Q, K):
    m = [0.0] * (K + 1)
    m[1] = matrix_trace(Q) / len(Q)
    for k in range(2, K + 1):
        Q_pow = matrix_power(Q, k)
        m[k] = matrix_trace(Q_pow) / len(Q)
    return m

def lagrange_inversion(m, K):
    chi = [0.0] * (K + 1)
    chi[0] = 1.0
    for k in range(1, K + 1):
        for j in range(1, k + 1):
            chi[k] += Fraction(j, k) * m[j] * chi[k - j]
    return chi

def compute_S_transform(chi, K):
    S = [0.0] * (K + 1)
    for k in range(1, K + 1):
        S[k] = (1 + k) * chi[k] / k
    return S

def compute_free_mult_defect(m, mu, K):
    m2 = m[2]
    mu2 = mu[2]
    delta = abs(mu2 - 2 * m2 - 1) / (1 + m2)
    return delta

def build_disj_matrix(n):
    N = 2 ** n
    M = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            M[i][j] = 1 if (i & j) == j else 0
    return M

def build_rank1_matrix(N):
    v = [random.randint(0, 1) for _ in range(N)]
    M = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            M[i][j] = v[i] * v[j]
    return M

def build_and_matrix(N):
    M = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            M[i][j] = 1 if (i & j) == j else 0
    return M

def build_identity_matrix(N):
    M = [[0] * N for _ in range(N)]
    for i in range(N):
        M[i][i] = 1
    return M

def compute_cc_upper_bound(M):
    N = len(M)
    max_iter = 4 * N
    cover_size = 0
    for _ in range(max_iter):
        i = random.randint(0, N - 1)
        j = random.randint(0, N - 1)
        if M[i][j] == 1:
            cover_size += 1
    return math.log2(cover_size) if cover_size > 0 else 0

def run_trial(seed):
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        N = 2 ** n
        K = math.ceil(math.log2(N)) + 2

        # Build DISJ matrix
        M_disj = build_disj_matrix(n)
        Q_disj = matrix_mult(matrix_transpose(M_disj), M_disj)
        m_disj = compute_moments(Q_disj, K)
        chi_disj = lagrange_inversion(m_disj, K)
        S_disj = compute_S_transform(chi_disj, K)
        mu_disj = [0.0] * (K + 1)
        for k in range(1, K + 1):
            mu_disj[k] = 2 * S_disj[k]
        delta_disj = compute_free_mult_defect(m_disj, mu_disj, K)

        if delta_disj < 0.125:
            conjecture_holds = False
            counterexample = f"DISJ defect too small: n={n}, delta={delta_disj}"

        # Sample uniform Boolean matrix
        M_uniform = [[random.randint(0, 1) for _ in range(N)] for _ in range(N)]
        Q_uniform = matrix_mult(matrix_transpose(M_uniform), M_uniform)
        m_uniform = compute_moments(Q_uniform, K)
        chi_uniform = lagrange_inversion(m_uniform, K)
        S_uniform = compute_S_transform(chi_uniform, K)
        mu_uniform = [0.0] * (K + 1)
        for k in range(1, K + 1):
            mu_uniform[k] = 2 * S_uniform[k]
        delta_uniform = compute_free_mult_defect(m_uniform, mu_uniform, K)
        U_uniform = compute_cc_upper_bound(M_uniform)

        if U_uniform < 0.05 * math.log2(N) * delta_uniform:
            conjecture_holds = False
            counterexample = f"Uniform matrix: U < 0.05 log2(N) delta: n={n}, U={U_uniform}, delta={delta_uniform}"

        # Build rank-1 matrix
        M_rank1 = build_rank1_matrix(N)
        Q_rank1 = matrix_mult(matrix_transpose(M_rank1), M_rank1)
        m_rank1 = compute_moments(Q_rank1, K)
        chi_rank1 = lagrange_inversion(m_rank1, K)
        S_rank1 = compute_S_transform(chi_rank1, K)
        mu_rank1 = [0.0] * (K + 1)
        for k in range(1, K + 1):
            mu_rank1[k] = 2 * S_rank1[k]
        delta_rank1 = compute_free_mult_defect(m_rank1, mu_rank1, K)
        U_rank1 = compute_cc_upper_bound(M_rank1)

        if U_rank1 < 0.05 * math.log2(N) * delta_rank1:
            conjecture_holds = False
            counterexample = f"Rank-1 matrix: U < 0.05 log2(N) delta: n={n}, U={U_rank1}, delta={delta_rank1}"

        # Build AND matrix
        M_and = build_and_matrix(N)
        Q_and = matrix_mult(matrix_transpose(M_and), M_and)
        m_and = compute_moments(Q_and, K)
        chi_and = lagrange_inversion(m_and, K)
        S_and = compute_S_transform(chi_and, K)
        mu_and = [0.0] * (K + 1)
        for k in range(1, K + 1):
            mu_and[k] = 2 * S_and[k]
        delta_and = compute_free_mult_defect(m_and, mu_and, K)
        U_and = compute_cc_upper_bound(M_and)

        if U_and < 0.05 * math.log2(N) * delta_and:
            conjecture_holds = False
            counterexample = f"AND matrix: U < 0.05 log2(N) delta: n={n}, U={U_and}, delta={delta_and}"

        # Build identity matrix
        M_identity = build_identity_matrix(N)
        Q_identity = matrix_mult(matrix_transpose(M_identity), M_identity)
        m_identity = compute_moments(Q_identity, K)
        chi_identity = lagrange_inversion(m_identity, K)
        S_identity = compute_S_transform(chi_identity, K)
        mu_identity = [0.0] * (K + 1)
        for k in range(1, K + 1):
            mu_identity[k] = 2 * S_identity[k]
        delta_identity = compute_free_mult_defect(m_identity, mu_identity, K)
        U_identity = compute_cc_upper_bound(M_identity)

        if U_identity < 0.05 * math.log2(N) * delta_identity:
            conjecture_holds = False
            counterexample = f"Identity matrix: U < 0.05 log2(N) delta: n={n}, U={U_identity}, delta={delta_identity}"

        metric_values.append(delta_uniform)

    return {
        "metric_name": "free_mult_defect",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(n_values) * 4,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")