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

def sipser_function(n, x):
    return sum(x[i] * (2 ** i) for i in range(n)) % 2 == 0

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        pivot_row = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        for i in range(m):
            if i != rank and A[i][j] != 0:
                factor = A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def homology_group_rank(n, seed):
    random.seed(seed)
    A = [[sipser_function(n, list(x[:i] + (j,) + x[i+1:])) for j in range(2)] for i in range(n)]
    rank = gaussian_elimination(A)
    return rank

def run_trial(seed: int) -> dict:
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 30
        total_index = 0
        for _ in range(instances_tested):
            index = homology_group_rank(n, seed)
            if index < 0 or index > n * (n + 1) // 2:  # Upper bound on the rank of a matrix
                return {
                    "metric_name": "minimal_local_index",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Invalid homology group rank {index} for n={n}"
                }
            total_index += index
        mean_index = Fraction(total_index, instances_tested)
        results.append({"n": n, "mean_index": mean_index})
    
    conjecture_holds = all(0.3 * n**2 <= result["mean_index"] <= 3 * n**2 for result in results)
    counterexample = "" if conjecture_holds else f"Failed for n={results[0]['n']}"
    
    return {
        "metric_name": "minimal_local_index",
        "metric_value": sum(result["mean_index"] for result in results) / len(results),
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")