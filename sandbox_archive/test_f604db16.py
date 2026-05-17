# auto-injected by SEC sandbox
import json
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
from collections import defaultdict

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0.0 for _ in range(m)] for _ in range(n)]
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

def matrix_identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def matrix_rank(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for row in range(n):
        if rank >= m:
            break
        i = rank
        while i < n and A[i][rank] == 0:
            i += 1
        if i == n:
            continue
        A[rank], A[i] = A[i], A[rank]
        for i in range(rank + 1, n):
            factor = A[i][rank] / A[rank][rank]
            for j in range(rank, m):
                A[i][j] -= factor * A[rank][j]
        rank += 1
    return rank

def matrix_determinant(A):
    n = len(A)
    det = 1.0
    for i in range(n):
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    det *= -1
                    break
            else:
                return 0.0
        det *= A[i][i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return det

def matrix_eigenvalues(A):
    n = len(A)
    eigenvalues = []
    for i in range(n):
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                eigenvalues.append(0.0)
                continue
        eigenvalues.append(A[i][i])
    return eigenvalues

def build_hankel_matrix(moments, d):
    H = [[0.0 for _ in range(d + 1)] for _ in range(d + 1)]
    for i in range(d + 1):
        for j in range(d + 1):
            if i + j < len(moments):
                H[i][j] = moments[i + j]
    return H

def compute_delta(P, Q, n, seed):
    N = 2 * n
    d = N // 8
    max_k = N // 4
    moments = defaultdict(lambda: defaultdict(list))
    for z in range(2 ** N):
        for l in range(2 * N):
            q = P[z][l]
            x = sum((z >> i) & 1 for i in range(n))
            y = sum((z >> (n + i)) & 1 for i in range(n))
            IP2 = (x * y) % 2
            moments[q][l].append(IP2 - 0.5)
    delta = 0
    for q in Q:
        for l in range(2 * N):
            if l not in moments[q]:
                continue
            m = moments[q][l]
            if len(m) < max_k:
                continue
            H = build_hankel_matrix(m, d)
            eigenvalues = matrix_eigenvalues(H)
            negative_eigenvalues = sum(1 for ev in eigenvalues if ev < 0)
            delta = max(delta, negative_eigenvalues)
    return delta

def generate_random_bp(n, w, seed):
    N = 2 * n
    Q = list(range(w))
    P = [[0 for _ in range(2 * N)] for _ in range(2 ** N)]
    random.seed(seed)
    for z in range(2 ** N):
        for l in range(2 * N):
            P[z][l] = random.choice(Q)
    return P, Q

def generate_ip2_bp(n):
    N = 2 * n
    Q = list(range(2 ** n))
    P = [[0 for _ in range(2 * N)] for _ in range(2 ** N)]
    for z in range(2 ** N):
        x = z & ((1 << n) - 1)
        y = (z >> n) & ((1 << n) - 1)
        for l in range(n):
            P[z][l] = x
        for l in range(n, 2 * n):
            P[z][l] = (x * y) % 2
    return P, Q

def run_trial(seed):
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    widths = [2, 3, 4, 6, 8, 12]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        N = 2 * n
        for w in widths:
            P, Q = generate_random_bp(n, w, seed)
            s = len(Q)
            delta = compute_delta(P, Q, n, seed)
            bound = 8 * math.ceil(math.log2(s + 1))
            if delta > bound:
                conjecture_holds = False
                counterexample = f"Random BP with n={n}, w={w}, delta={delta}, bound={bound}"
                break
            metric_values.append(delta)
            instances_tested += 1

        if not conjecture_holds:
            break

        if n in [3, 4, 5]:
            P, Q = generate_ip2_bp(n)
            s = len(Q)
            delta = compute_delta(P, Q, n, seed)
            bound = math.ceil(math.sqrt(N) / 2)
            if delta < bound:
                conjecture_holds = False
                counterexample = f"IP2 BP with n={n}, delta={delta}, bound={bound}"
                break
            metric_values.append(delta)
            instances_tested += 1

    if not metric_values:
        return {
            "metric_name": "delta",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    metric_value = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "delta",
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

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_metric_values")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")