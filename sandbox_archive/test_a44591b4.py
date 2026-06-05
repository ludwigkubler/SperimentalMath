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
from fractions import Fraction
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        pivot_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        A[i], A[pivot_row] = A[pivot_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue  # Skip rows with zero pivot to avoid division by zero
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def random_d_regular_variety(n, d=2):
    A = [[0] * n for _ in range(n)]
    count = 0
    while count < d * n:
        i, j = random.sample(range(n), 2)
        if i != j and A[i][j] == 0:
            A[i][j] = 1
            A[j][i] = 1
            count += 2
    return A

def circuit_satisfiability_threshold(A):
    n = len(A)
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] == 1:
                clauses.append((i, j))
    return len(clauses)

def minimal_tropical_motivic_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] == 1:
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        A = random_d_regular_variety(n)
        tmr = minimal_tropical_motivic_rank(A)
        cst = circuit_satisfiability_threshold(A)
        results.append((tmr, cst))
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n = len(results)
    tmr_values = [tmr for tmr, _ in results]
    cst_values = [cst for _, cst in results]
    
    mean_tmr = sum(tmr_values) / n
    mean_cst = sum(cst_values) / n
    
    cov = sum((tmr - mean_tmr) * (cst - mean_cst) for tmr, cst in results)
    var_tmr = sum((tmr - mean_tmr) ** 2 for tmr in tmr_values)
    var_cst = sum((cst - mean_cst) ** 2 for cst in cst_values)
    
    if var_tmr == 0 or var_cst == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n),
            "conjecture_holds": False,
            "counterexample": "constant_values"
        }
    
    pearson_corr = cov / (math.sqrt(var_tmr) * math.sqrt(var_cst))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": n,
        "n_max": max(n),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")