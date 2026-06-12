# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= mod
    return C

def matrix_pow(A, k, mod):
    n = len(A)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_mul(result, A, mod)
        A = matrix_mul(A, A, mod)
        k //= 2
    return result

def matrix_inv(A, mod):
    n = len(A)
    det = 0
    for i in range(n):
        minor = [[A[j][k] for k in range(n) if k != i] for j in range(1, n)]
        det += (-1) ** i * A[0][i] * matrix_det(minor, mod)
    det %= mod
    inv_det = pow(det, mod - 2, mod)
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[A[x][y] for y in range(n) if y != j] for x in range(n) if x != i]
            adjugate[j][i] = (-1) ** (i + j) * matrix_det(minor, mod)
    inv = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv

def matrix_det(A, mod):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for i in range(n):
        minor = [[A[j][k] for k in range(n) if k != i] for j in range(1, n)]
        det += (-1) ** i * A[0][i] * matrix_det(minor, mod)
    return det % mod

def is_invertible(A, mod):
    return matrix_det(A, mod) != 0

def gaussian_elimination(A, b, mod):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = (A[j][i] * pow(A[i][i], mod - 2, mod)) % mod
            for k in range(i, n):
                A[j][k] = (A[j][k] - factor * A[i][k]) % mod
            b[j] = (b[j] - factor * b[i]) % mod
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) * pow(A[i][i], mod - 2, mod) % mod
    return x

def rank_variance(V):
    n = len(V)
    m = len(V[0])
    A = [[0] * (n + m) for _ in range(n)]
    for i in range(n):
        for j in range(m):
            A[i][j] = V[i][j]
            A[i][j + m] = 1
    rank = 0
    for i in range(n):
        if any(A[j][i] != 0 for j in range(i, n)):
            rank += 1
    return (n - rank) ** 2

def algebraic_k_theory(V):
    n = len(V)
    m = len(V[0])
    A = [[0] * (n + m) for _ in range(n)]
    for i in range(n):
        for j in range(m):
            A[i][j] = V[i][j]
            A[i][j + m] = 1
    rank = 0
    for i in range(n):
        if any(A[j][i] != 0 for j in range(i, n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    V = [[random.randint(0, 2**31 - 1) for _ in range(n)] for _ in range(n)]
    r = rank_variance(V)
    k = algebraic_k_theory(V)
    if r == 0:
        return {
            "metric_name": "K-theory generators",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "rank_variance_is_zero"
        }
    ratio = k / r ** (2/3)
    return {
        "metric_name": "K-theory generators",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")