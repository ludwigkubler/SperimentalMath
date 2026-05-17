# auto-injected by SEC sandbox
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
import json
from collections import defaultdict

def matrix_mult(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_sub(A, B):
    return [[a - b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

def matrix_add(A, B):
    return [[a + b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

def matrix_scale(A, scalar):
    return [[a * scalar for a in row] for row in A]

def matrix_identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_inverse(A):
    n = len(A)
    I = matrix_identity(n)
    for col in range(n):
        max_row = max(range(col, n), key=lambda r: abs(A[r][col]))
        A[col], A[max_row] = A[max_row], A[col]
        I[col], I[max_row] = I[max_row], I[col]
        pivot = A[col][col]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
        for i in range(n):
            A[col][i] /= pivot
            I[col][i] /= pivot
        for row in range(n):
            if row != col and A[row][col] != 0:
                factor = A[row][col]
                for i in range(n):
                    A[row][i] -= factor * A[col][i]
                    I[row][i] -= factor * I[col][i]
    return I

def matrix_determinant(A):
    n = len(A)
    det = 1
    for col in range(n):
        max_row = max(range(col, n), key=lambda r: abs(A[r][col]))
        A[col], A[max_row] = A[max_row], A[col]
        if col != max_row:
            det *= -1
        pivot = A[col][col]
        if pivot == 0:
            return 0
        det *= pivot
        for row in range(col + 1, n):
            factor = A[row][col] / pivot
            for i in range(col, n):
                A[row][i] -= factor * A[col][i]
    return det

def matrix_eigenvalues(A):
    n = len(A)
    eigenvalues = []
    for _ in range(n):
        x = [random.random() for _ in range(n)]
        for _ in range(100):
            Ax = matrix_mult(A, [x])[0]
            norm = math.sqrt(sum(a**2 for a in Ax))
            if norm == 0:
                break
            x = [a / norm for a in Ax]
        eigenvalues.append(matrix_mult([x], matrix_mult(A, [x]))[0][0])
    return eigenvalues

def count_negative_eigenvalues(A):
    eigenvalues = matrix_eigenvalues(A)
    return sum(1 for ev in eigenvalues if ev < 0)

def generate_random_bp(n, w, seed):
    random.seed(seed)
    N = 2 * n
    Q = list(range(w))
    P = []
    for _ in range(N):
        P.append([random.choice(Q) for _ in range(w)])
    return P, Q

def generate_ip2_bp(n):
    N = 2 * n
    Q = list(itertools.product([0, 1], repeat=n))
    P = []
    for _ in range(N):
        P.append([random.choice(Q) for _ in range(2**n)])
    return P, Q

def compute_moments(P, Q, n, seed):
    random.seed(seed)
    N = 2 * n
    moments = defaultdict(lambda: defaultdict(list))
    for z in itertools.product([0, 1], repeat=N):
        for l in range(N):
            q = P[l][random.randint(0, len(P[l]) - 1)]
            ip2 = (sum(z[i] * z[i + n] for i in range(n)) % 2) - 0.5
            moments[q][l].append(ip2)
    return moments

def build_hankel_matrix(moments, d):
    k = len(moments)
    H = [[0] * (d + 1) for _ in range(d + 1)]
    for i in range(d + 1):
        for j in range(d + 1):
            if i + j < k:
                H[i][j] = sum(m** (i + j) for m in moments[i + j])
    return H

def compute_delta(P, Q, n, seed):
    moments = compute_moments(P, Q, n, seed)
    d = n // 8
    delta = 0
    for q in Q:
        for l in range(2 * n):
            if l in moments[q]:
                H = build_hankel_matrix(moments[q][l], d)
                delta = max(delta, count_negative_eigenvalues(H))
    return delta

def run_trial(seed):
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    w_values = [2, 3, 4, 6, 8, 12]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for w in w_values:
            P, Q = generate_random_bp(n, w, seed)
            delta = compute_delta(P, Q, n, seed)
            s = len(Q)
            bound = 8 * math.ceil(math.log2(s + 1))
            if delta > bound:
                conjecture_holds = False
                counterexample = f"Random BP with n={n}, w={w}, delta={delta}, bound={bound}"
                break

            if n in [3, 4, 5]:
                P_ip2, Q_ip2 = generate_ip2_bp(n)
                delta_ip2 = compute_delta(P_ip2, Q_ip2, n, seed)
                bound_ip2 = math.ceil(math.sqrt(2 * n) / 2)
                if delta_ip2 < bound_ip2:
                    conjecture_holds = False
                    counterexample = f"IP2 BP with n={n}, delta={delta_ip2}, bound={bound_ip2}"
                    break

            instances_tested += 1

    return {
        "metric_name": "delta",
        "metric_value": delta if conjecture_holds else 0,
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

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={counterexample} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")