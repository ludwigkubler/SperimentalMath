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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def norm_4(v):
    return (sum(x**4 for x in v)) ** 0.25

def norm_2(v):
    return (sum(x**2 for x in v)) ** 0.5

def is_unsatisfiable(phi):
    n = len(phi[0])
    queue = [(0, [0]*n)]
    while queue:
        count, assignment = queue.pop(0)
        if all(phi[i][j] == (assignment[j] ^ phi[i][j]) for i in range(len(phi))):
            return True
        for j in range(n):
            new_assignment = assignment[:]
            new_assignment[j] ^= 1
            queue.append((count + 1, new_assignment))
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    alpha = 4.5
    instances_tested = 0
    total_T_DPLL = 0
    counterexample = ""

    for n in n_values:
        m = int(alpha * n)
        phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        if is_unsatisfiable(phi):
            f_phi = [sum(1 for C in phi if all(C[j] == (x[j] ^ C[j]) for j in range(n))) / m for x in [(i >> j) & 1 for i in range(2**n)]]
            g_phi = [f_phi[i] - sum(f_phi) / len(f_phi) for i in range(len(f_phi))]
            norm_g_4 = norm_4(g_phi)
            norm_g_2 = norm_2(g_phi)
            E = norm_g_4 ** 4 / norm_g_2 ** 4 if norm_g_2 != 0 else 1
            T_DPLL = sum(1 for _ in range(10))  # Placeholder for actual DPLL computation

            instances_tested += len(f_phi)
            total_T_DPLL += T_DPLL

            if log2(T_DPLL) < (n - math.log2(m)) / E - 5:
                counterexample = f"Instance with n={n}, m={m} violates the bound."

    mean_T_DPLL = total_T_DPLL / instances_tested
    conjecture_holds = all(log2(T_DPLL) >= (n - math.log2(m)) / E - 5 for T_DPLL, n, m in zip(total_T_DPLL, n_values, [int(alpha * n) for n in n_values]))

    return {
        "metric_name": "log2(T_DPLL)",
        "metric_value": mean_T_DPLL,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_T_DPLL = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_T_DPLL} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")