# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def rank_1_decomposition(T, max_iter=1000, tol=1e-6):
    U = [[random.random() for _ in range(len(T))] for _ in range(len(T[0]))]
    V = [[random.random() for _ in range(len(T[0]))] for _ in range(len(T))]
    for _ in range(max_iter):
        U_new = matrix_multiply(U, T)
        V_new = matrix_multiply(V, transpose(T))
        if max(abs(x) for row in U_new for x in row) < tol and max(abs(x) for row in V_new for x in row) < tol:
            break
        U = [[x / math.sqrt(sum(y**2 for y in row)) for y in row] for row in U_new]
        V = [[x / math.sqrt(sum(y**2 for y in col)) for col in zip(*V_new)] for _ in range(len(V))]
    return U, V

def secant_rank(T):
    U, V = rank_1_decomposition(T)
    rank = 0
    for u_row in U:
        for v_col in zip(*V):
            if sum(x * y for x, y in zip(u_row, v_col)) > tol:
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    T_M = [M] + transpose(M)
    secant_rank_value = secant_rank(T_M)
    conjecture_holds = secant_rank_value >= n / 2
    counterexample = "" if conjecture_holds else "secant rank < n/2"
    return {
        "metric_name": "secant_rank",
        "metric_value": secant_rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"secant rank < n/2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")