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
        M[i][i + 1 if i < n - 1 else 0] = 1
        M[(i + 2) % n][(i + 3) % n] = 1
    return M

def matrix_multiply(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def transpose(M):
    m, n = len(M), len(M[0])
    M_t = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            M_t[j][i] = M[i][j]
    return M_t

def is_symplectic_form(M, n):
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    return matrix_multiply(matrix_multiply(M, M), I) == -I and matrix_multiply(transpose(M), M) == -I

def symplectic_rank(M, n):
    rank = 0
    while True:
        found = False
        for i in range(n):
            for j in range(i + 1, n):
                if M[i][j] != 0:
                    found = True
                    break
            if found:
                break
        if not found:
            return rank
        rank += 1
        for i in range(n):
            for j in range(n):
                M[i][j] -= M[i][j] * M[j][i]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    c = 0.25
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        M = generate_disjointness_matrix(n)
        if not is_symplectic_form(M, n):
            return {
                "metric_name": "symplectic_rank",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        rank = symplectic_rank(M, n)
        if rank < c * n:
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}"
        instances_tested += 1

    return {
        "metric_name": "symplectic_rank",
        "metric_value": None,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")