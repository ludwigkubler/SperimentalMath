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

def matrix_rank(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for i in range(min(n, m)):
        if any(A[i][j] != 0 for j in range(m)):
            rank += 1
            for k in range(i + 1, n):
                factor = Fraction(A[k][i], A[i][i])
                for j in range(i, m):
                    A[k][j] -= factor * A[i][j]
    return rank

def count_negative_eigenvalues(H):
    n = len(H)
    count = 0
    for i in range(n):
        if H[i][i] < 0:
            count += 1
    return count

def generate_random_bp(n, w, seed):
    random.seed(seed)
    Q = list(range(w))
    N = 2 * n
    P = {}
    for q in Q:
        for l in range(2 * N):
            P[(q, l)] = [0] * (N + 1)
    for z in itertools.product([0, 1], repeat=N):
        q = random.choice(Q)
        for l in range(2 * N):
            k = sum((z[i] - 0.5) ** 2 for i in range(N))
            P[(q, l)][k] += 1
    return P, Q, N

def generate_ip2_bp(n):
    N = 2 * n
    Q = list(itertools.product([0, 1], repeat=n))
    P = {}
    for q in Q:
        for l in range(2 * N):
            P[(q, l)] = [0] * (N + 1)
    for z in itertools.product([0, 1], repeat=N):
        q = tuple(z[:n])
        for l in range(2 * N):
            k = sum((z[i] - 0.5) ** 2 for i in range(N))
            P[(q, l)][k] += 1
    return P, Q, N

def compute_delta(P, Q, N):
    d = N // 8
    delta = 0
    for q in Q:
        for l in range(2 * N):
            m = P[(q, l)]
            H = [[m[i + j] for j in range(d + 1)] for i in range(d + 1)]
            rank = matrix_rank(H)
            if rank < d + 1:
                delta += 1
    return delta

def run_trial(seed):
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    w_values = [2, 3, 4, 6, 8, 12]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for w in w_values:
            P, Q, N = generate_random_bp(n, w, seed)
            delta = compute_delta(P, Q, N)
            s = len(Q)
            bound = 8 * math.ceil(math.log2(s + 1))
            if delta > bound:
                conjecture_holds = False
                counterexample = f"Random BP with n={n}, w={w}, delta={delta} exceeds bound {bound}"
                break
            metric_values.append(delta)
            instances_tested += 1

        if not conjecture_holds:
            break

    if conjecture_holds:
        for n in [3, 4, 5]:
            P, Q, N = generate_ip2_bp(n)
            delta = compute_delta(P, Q, N)
            bound = math.ceil(math.sqrt(N) / 2)
            if delta < bound:
                conjecture_holds = False
                counterexample = f"IP2 BP with n={n}, delta={delta} falls below bound {bound}"
                break
            metric_values.append(delta)
            instances_tested += 1

    if not metric_values:
        return {
            "metric_name": "delta",
            "metric_value": 0,
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
    seeds = sys.argv[1:]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    results = []
    for seed in seeds:
        result = run_trial(int(seed))
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
        print("RESULT: INCONCLUSIVE reason=unknown")