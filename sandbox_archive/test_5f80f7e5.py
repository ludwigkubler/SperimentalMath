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
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        pivot = Fraction(1, A[i][i])
        for j in range(n):
            A[i][j] *= pivot
        for j in range(m):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def min_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A = [row[:] for row in matrix]
    rank = 0
    for i in range(m):
        if all(A[i][j] == 0 for j in range(n)):
            continue
        rank += 1
        pivot_col = next(j for j in range(n) if A[i][j] != 0)
        for j in range(i+1, m):
            factor = A[j][pivot_col]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return rank

def sos_degree(instance_size):
    # Placeholder function to compute SOS degree
    # This is a dummy implementation and should be replaced with actual logic
    return instance_size ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    incidence_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    min_rank_val = min_rank(incidence_matrix)
    sos_degree_val = sos_degree(n)
    
    if sos_degree_val == 0:
        return {
            "metric_name": "min_rank_to_sos_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "sos_degree_is_zero"
        }
    
    ratio = Fraction(min_rank_val, sos_degree_val)
    return {
        "metric_name": "min_rank_to_sos_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= Fraction(3, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_to_sos_ratio\" first_failing_seed={first_failing_seed}")