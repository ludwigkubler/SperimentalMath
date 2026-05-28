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
    rows, cols = len(A), len(A[0])
    for i in range(rows):
        max_row = i
        for k in range(i + 1, rows):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        if factor == 0:
            continue
        for j in range(cols):
            A[i][j] /= factor
        for k in range(rows):
            if k != i:
                factor = A[k][i]
                for j in range(cols):
                    A[k][j] -= factor * A[i][j]

def matrix_rank(A):
    rows, cols = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    rank = 0
    for i in range(rows):
        if any(A_copy[i]):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    P = [[random.random() for _ in range(n)] for _ in range(n)]
    rho_P = matrix_rank(P)
    size_P = n * n
    return {
        "metric_name": "minimal_rank",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": rho_P < n * math.log(n),
        "counterexample": "" if rho_P < n * math.log(n) else f"rho(P) = {rho_P}, size(P) = {size_P}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)

    mean_rho = sum(result["metric_value"] for result in results) / len(results)
    std_rho = math.sqrt(sum((result["metric_value"] - mean_rho)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho(P) >= n log(n)\" first_failing_seed={first_failing_seed}")