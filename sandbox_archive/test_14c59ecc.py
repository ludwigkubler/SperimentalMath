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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    rank = sum(1 for row in matrix if any(row))
    return rank

def symplectic_rank(instance):
    n = len(instance)
    A = [[0] * (2*n) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = instance[i][j]
            A[i][n + j] = -instance[j][i]
    return gaussian_elimination(A)

def communication_complexity_rank_variance(instance):
    n = len(instance)
    ccrvar = 0
    for i in range(n):
        for j in range(i+1, n):
            ccrvar += abs(instance[i][j] - instance[j][i])
    return ccrvar / (n * (n-1) / 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    srank = symplectic_rank(instance)
    ccrvar = communication_complexity_rank_variance(instance)
    metric_value = srank / math.sqrt(ccrvar)
    instances_tested = 1
    n_max = n
    conjecture_holds = srank <= ccrvar**0.5
    counterexample = "" if conjecture_holds else "srank > ccrvar^(1/2)"
    return {
        "metric_name": "symplectic_rank_over_ccrvar_sqrt",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if not r["conjecture_holds"]) < 0.5:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"srank > ccrvar^(1/2)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")