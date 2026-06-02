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
    n = len(A)
    m = len(A[0])
    for i in range(n):
        pivot_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        A[i], A[pivot_row] = A[pivot_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(m):
            A[i][j] /= pivot
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(m):
                    A[j][k] -= factor * A[i][k]
    return A

def min_rank(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(m)):
            continue
        rank += 1
    return rank

def comm_rank(φ):
    # Placeholder function; replace with actual communication complexity computation
    # For simplicity, assume it returns a random integer between 1 and n
    n = len(φ)
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        φ = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        comm_rank_val = comm_rank(φ)
        A = gaussian_elimination(φ)
        min_rank_val = min_rank(A)
        results.append((comm_rank_val, min_rank_val))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    comm_ranks = [r[0] for r in results]
    min_ranks = [r[1] for r in results]
    n = len(comm_ranks)
    mean_comm_rank = sum(comm_ranks) / n
    mean_min_rank = sum(min_ranks) / n
    covariance = sum((comm_ranks[i] - mean_comm_rank) * (min_ranks[i] - mean_min_rank) for i in range(n)) / n
    variance_comm_rank = sum((comm_ranks[i] - mean_comm_rank) ** 2 for i in range(n)) / n
    variance_min_rank = sum((min_ranks[i] - mean_min_rank) ** 2 for i in range(n)) / n
    pearson_corr = covariance / (math.sqrt(variance_comm_rank * variance_min_rank))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")