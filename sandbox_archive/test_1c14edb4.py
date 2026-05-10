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

def matrix_multiply(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    for j in range(n):
        pivot_row = max(range(j, m), key=lambda i: abs(augmented[i][j]))
        augmented[j], augmented[pivot_row] = augmented[pivot_row], augmented[j]
        for i in range(m):
            if i != j:
                factor = augmented[i][j] / augmented[j][j]
                for k in range(n + 1):
                    augmented[i][k] -= factor * augmented[j][k]
    return [row[-1] for row in augmented]

def noncommutative_rank(M, n):
    rank = 0
    A = M[:n][:n]
    b = [1 if i < n else 0 for i in range(n)]
    while True:
        try:
            x = gaussian_elimination(A, b)
            rank += 1
        except Exception:
            break
        A = [[A[i][j] - x[j] * M[i][n + j] for j in range(n)] for i in range(n)]
        b = [b[i] - x[j] * M[n + j][i] for i, j in enumerate(range(n))]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 30, 40]
    c = 0.1
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per n
            M_n = generate_disjointness_matrix(n)
            tau_M_n = noncommutative_rank(M_n, n)
            if tau_M_n < c * n:
                conjecture_holds = False
                counterexample = f"n={n}, tau(M_n)={tau_M_n} < {c*n}"
            total_metric_value += tau_M_n
            instances_tested += 1

    return {
        "metric_name": "noncommutative_rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 3 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data to determine support or falsify")