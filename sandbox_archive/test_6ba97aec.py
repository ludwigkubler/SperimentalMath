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

def matrix_mult(A, B):
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

def matrix_inverse(A):
    n = len(A)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        if A[col][col] == 0:
            for row in range(col + 1, n):
                if A[row][col] != 0:
                    A[col], A[row] = A[row], A[col]
                    I[col], I[row] = I[row], I[col]
                    break
        pivot = A[col][col]
        for j in range(n):
            A[col][j] = Fraction(A[col][j], pivot)
            I[col][j] = Fraction(I[col][j], pivot)
        for i in range(n):
            if i != col and A[i][col] != 0:
                factor = A[i][col]
                for j in range(n):
                    A[i][j] -= factor * A[col][j]
                    I[i][j] -= factor * I[col][j]
    return I

def det(A):
    n = len(A)
    det_val = Fraction(1)
    for col in range(n):
        if A[col][col] == 0:
            for row in range(col + 1, n):
                if A[row][col] != 0:
                    A[col], A[row] = A[row], A[col]
                    det_val *= -1
                    break
        if A[col][col] == 0:
            return Fraction(0)
        det_val *= A[col][col]
        for row in range(col + 1, n):
            factor = Fraction(A[row][col], A[col][col])
            for c in range(col, n):
                A[row][c] -= factor * A[col][c]
    return det_val

def generate_permutation(n):
    perm = list(range(n))
    random.shuffle(perm)
    return perm

def generate_random_matrix(n, m, seed):
    random.seed(seed)
    return [[random.gauss(0, 1) for _ in range(n)] for _ in range(m)]

def generate_random_vector(n, seed):
    random.seed(seed)
    return [random.gauss(0, 1) for _ in range(n)]

def compute_v_sigma(f_L_ell, sigma, n, m, L, ell):
    v_sigma = 0
    for psi in itertools.permutations(range(n), m):
        M_sigma_psi = [[L[a][b][psi[a] * n + sigma[psi[a]]] for b in range(m)] for a in range(m)]
        det_M = det(M_sigma_psi)
        product_ell = 1
        for p in range(n):
            if p not in psi:
                product_ell *= ell[p * n + sigma[p]]
        v_sigma += det_M * product_ell
    return v_sigma * math.factorial(n - m)

def compute_rho(f_L_ell, n, m, L, ell):
    v = [compute_v_sigma(f_L_ell, sigma, n, m, L, ell) for sigma in itertools.permutations(range(n))]
    sum_v = sum(v)
    sum_v_sq = sum(x * x for x in v)
    if sum_v_sq == 0:
        return 0
    return (sum_v * sum_v) / (math.factorial(n) * sum_v_sq)

def run_trial(seed):
    n_values = [4, 5, 6]
    m_values = [[2], [n//2], [n-1]]
    max_rho = 0
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for m in m_values:
            random.seed(seed)
            L = [[generate_random_vector(n * n, seed + i + j) for j in range(n)] for i in range(m)]
            ell = generate_random_vector(n * n, seed + m)
            f_L_ell = lambda y: sum(ell[i] * y[i] for i in range(n * n)) ** (n - m) * det([[L[a][b][i] for b in range(m)] for a in range(m)])
            rho = compute_rho(f_L_ell, n, m, L, ell)
            instances_tested += 1
            if rho > max_rho:
                max_rho = rho
            if rho >= 1 - 1/n:
                counterexample = f"rho={rho} >= 1-1/{n} for n={n}, m={m}"
                break
        if counterexample:
            break

    conjecture_holds = max_rho < 1 - 1/n_values[-1]
    return {
        "metric_name": "max_rho",
        "metric_value": max_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        if result["counterexample"]:
            counterexamples.append((seed, result["counterexample"]))

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if counterexamples:
        seed, counterexample = counterexamples[0]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")