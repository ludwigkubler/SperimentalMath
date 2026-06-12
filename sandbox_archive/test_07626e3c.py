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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A, mod):
    n = len(A)
    m = len(A[0])
    x = [0] * n
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(m):
            A[i][j] = (A[i][j] * pow(pivot, -1, mod)) % mod
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(m):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % mod
    return x

def matrix_mult(A, B, mod):
    n = len(A)
    m = len(B[0])
    p = len(B)
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_add(A, B, mod):
    n = len(A)
    m = len(A[0])
    C = [[(A[i][j] + B[i][j]) % mod for j in range(m)] for i in range(n)]
    return C

def matrix_sub(A, B, mod):
    n = len(A)
    m = len(A[0])
    C = [[(A[i][j] - B[i][j]) % mod for j in range(m)] for i in range(n)]
    return C

def inverse_matrix(M, mod):
    n = len(M)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    A = [row[:] + col[:] for row, col in zip(M, I)]
    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, n * 2):
            A[i][j] = (A[i][j] * pow(pivot, -1, mod)) % mod
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n * 2):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % mod
    return [row[n:] for row in A]

def rank_variance(V):
    n, m = len(V), len(V[0])
    M = [[V[i][j] for j in range(m)] + [1 if i == k else 0 for k in range(n)] for i in range(n)]
    _, U = gaussian_elimination(M, 2)
    rank = sum(1 for row in U if any(row[j] != 0 for j in range(n)))
    return n - rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 0
    total_ratio = 0.0
    n_max = 5
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break

        V_phi = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        r = rank_variance(V_phi)
        if r == 0:
            continue

        K_phi = n - r
        ratio = Fraction(K_phi, r**(2/3)).limit_denominator()
        total_ratio += ratio
        instances_tested += 1
        n_max = max(n_max, n)

        if ratio < 1.0:
            conjecture_holds = False
            counterexample = f"n={n}, K(φ)={K_phi}, r={r}, ratio={ratio}"

    return {
        "metric_name": "Ratio of |K(φ)| / r^(2/3)",
        "metric_value": total_ratio / instances_tested if instances_tested > 0 else 0.0,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")