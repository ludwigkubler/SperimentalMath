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
        M[i][i] = 1
    return M

def tensorize(M, T):
    n = len(M)
    result = [[[0] * 2 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j][0] = M[i][j]
            result[i][j][1] = T[i][j]
    return result

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def rank_1_decomposition(T, max_iter=100, tol=1e-6):
    n = len(T)
    U = [[random.random() for _ in range(n)] for _ in range(n)]
    V = [[random.random() for _ in range(n)] for _ in range(2)]
    for _ in range(max_iter):
        U_new = matrix_multiply(U, T[0])
        V_new = [matrix_multiply(V[i], T[1]) for i in range(2)]
        if max(abs(U_new[i][j] - U[i][j]) for i in range(n) for j in range(n)) < tol and \
           max(abs(V_new[i][j] - V[i][j]) for i in range(2) for j in range(n)) < tol:
            break
        U = U_new
        V = V_new
    return sum(max(abs(U[i][j]) for i in range(n)) * max(abs(V[i][j]) for j in range(n)) for i in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    T_M = tensorize(M, M)
    secant_rank = rank_1_decomposition(T_M)
    return {
        "metric_name": "secant_rank",
        "metric_value": secant_rank,
        "instances_tested": 1,
        "conjecture_holds": secant_rank >= n / 2,
        "counterexample": "" if secant_rank >= n / 2 else f"n={n}, secant_rank={secant_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    secant_ranks = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if support_fraction >= 0.8:
        result_type = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results):
        result_type = "FALSIFIED"
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = f"n={40}, secant_rank<{40/2}"
    else:
        result_type = "INCONCLUSIVE"
        counterexample_desc = "mapping_undefined"

    print(f"RESULT: {result_type} mean={sum(secant_ranks)/len(secant_ranks):.2f} std={math.sqrt(sum((x - sum(secant_ranks)/len(secant_ranks))**2 for x in secant_ranks) / len(secant_ranks)):.2f} support_fraction={support_fraction:.2f}")
    if result_type == "FALSIFIED":
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")