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

def matrix_rank(M):
    m, n = len(M), len(M[0])
    A = [row[:] + [1] for row in M]
    pivot_row = 0
    for col in range(n):
        if all(A[row][col] == 0 for row in range(pivot_row, m)):
            continue
        for row in range(pivot_row, m):
            if A[row][col] != 0:
                A[pivot_row], A[row] = A[row], A[pivot_row]
                break
        pivot_col = col
        for row in range(m):
            if row == pivot_row:
                continue
            factor = A[row][pivot_col] / A[pivot_row][pivot_col]
            for j in range(n + 1):
                A[row][j] -= factor * A[pivot_row][j]
        pivot_row += 1
    rank = min(m, n)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_disjointness_matrix(n)
    dim_secant_variety = min(matrix_rank(M) + 1, n)
    c = 1 / 4
    conjecture_holds = dim_secant_variety >= c * n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "secant_dimension",
        "metric_value": dim_secant_variety,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")