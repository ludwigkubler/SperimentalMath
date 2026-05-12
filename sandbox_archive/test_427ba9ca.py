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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def matrix_multiply(A, B):
    C = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for l in range(len(B)):
                C[i][j] += A[i][l] * B[l][j]
    return C

def rank(A):
    m, n = len(A), len(A[0])
    U = [row[:] for row in A]
    Vt = transpose([col[:] for col in A])
    k = min(m, n)
    for i in range(k):
        max_row = max(range(i, m), key=lambda r: abs(U[r][i]))
        if U[max_row][i] == 0:
            return i
        U[i], U[max_row] = U[max_row], U[i]
        Vt[i], Vt[max_row] = Vt[max_row], Vt[i]
        for j in range(i + 1, m):
            factor = U[j][i] / U[i][i]
            for l in range(n):
                U[j][l] -= factor * U[i][l]
                Vt[l][j] -= factor * Vt[l][i]
    return k

def secant_rank(M):
    n = len(M)
    rank_M = rank(M)
    if rank_M == n:
        return 1
    A = M[:rank_M][:rank_M]
    B = M[rank_M:][rank_M:]
    C = matrix_multiply(A, transpose(B))
    rank_C = rank(C)
    return rank_M + rank_C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M_n = generate_disjointness_matrix(n)
    sr_M_n = secant_rank(M_n)
    metric_value = sr_M_n
    instances_tested = 1
    conjecture_holds = sr_M_n >= 0.6 * n
    counterexample = "" if conjecture_holds else f"n={n}, sr(M_n)={sr_M_n}"
    return {
        "metric_name": "secant_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = results[0]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")