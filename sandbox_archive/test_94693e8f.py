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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_rank(A):
    rank = 0
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    for row in A_copy:
        if any(row):
            rank += 1
    return rank

def decision_tree_size(f, n):
    if n == 1:
        return 1
    var = random.choice(range(n))
    left = [x for x in f if x[var] == 0]
    right = [x for x in f if x[var] == 1]
    return 1 + max(decision_tree_size(left, n - 1), decision_tree_size(right, n - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        f = [tuple(random.randint(0, 1) for _ in range(n)) for _ in range(2**n)]
        R_f = matrix_rank([[f[i][j] for j in range(n)] for i in range(2**n)])
        T_f = decision_tree_size(f, n)
        results.append((R_f, T_f))
    metric_value = sum(T / R for R, T in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(abs(R - T) < 0.1 * max(R, T) for R, T in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Rank vs Decision Tree Size Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")