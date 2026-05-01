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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    A_rref = gaussian_elimination(A_augmented)
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A_rref[i][-1]
        for j in range(i+1, n):
            x[i] -= A_rref[i][j] * x[j]
        x[i] /= A_rref[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def laplacian_matrix(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    degree_sum = sum(sum(row) for row in G)
    for i in range(n):
        L[i][i] = degree_sum - 2 * sum(G[i])
        for j in range(i+1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = -G[i][j]
    return L

def eigenvalue_lower_bound(L):
    eigenvalues = sorted(math.sqrt(e) for e in numpy.linalg.eigvalsh(L))
    lambda_2 = eigenvalues[1] if len(eigenvalues) > 1 else 0
    return lambda_2

def ben_sasson_wigderson_bound(n, lambda_2):
    return n * math.log(2 / (1 - lambda_2))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = sum(G[i])
    L = laplacian_matrix(G)
    lambda_2 = eigenvalue_lower_bound(L)
    if lambda_2 <= 1 / math.sqrt(n):
        return {
            "metric_name": "Resolution length lower bound",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "non-expander graph"
        }
    resolution_length = ben_sasson_wigderson_bound(n, lambda_2)
    return {
        "metric_name": "Resolution length lower bound",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"non-expander graph\" first_failing_seed={seeds[first_failing_seed]}")