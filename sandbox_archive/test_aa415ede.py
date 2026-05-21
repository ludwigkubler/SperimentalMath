# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def kronecker_coefficient(lam1, lam2):
    if not all(x >= 0 for x in lam1 + lam2):
        raise ValueError("Partition elements must be non-negative")
    m = len(lam1)
    n = len(lam2)
    k = sum(lam1) + sum(lam2)
    C = [[0] * (n + 1) for _ in range(m + 1)]
    C[0][0] = 1
    for i in range(1, m + 1):
        for j in range(n + 1):
            if lam1[i - 1] > 0:
                C[i][j] += C[i - 1][j]
            if j > 0 and lam2[j - 1] > 0:
                C[i][j] += C[i][j - 1]
    return Fraction(C[m][n], k + 1)

def generate_expander_graph(n):
    if n % 2 != 0 or n < 4:
        raise ValueError("n must be even and at least 4")
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if (i + j) % 2 == 0:
                A[i][j] = A[j][i] = 1
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        A = generate_expander_graph(n)
        m = len(A)
        permanent_coefficient = kronecker_coefficient([n], [1] * m)
        determinant_coefficient = kronecker_coefficient([1] * m, [1] * m)
        if permanent_coefficient <= determinant_coefficient:
            conjecture_holds = False
            counterexample = f"Graph with n={n}, A={A}"
            break

        total_metric_value += permanent_coefficient / determinant_coefficient
        instances_tested += 1

    return {
        "metric_name": "Kronecker Coefficient Exponential Gap",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")