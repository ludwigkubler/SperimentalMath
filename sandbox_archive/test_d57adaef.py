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
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    return sum(1 for row in A_copy if any(row))

def log2(x):
    return math.log2(x)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = 2**n
        A_F = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
        
        rank_F2 = rank(A_F)
        delta_F = log2(m + 1) - log2(rank_F2)
        
        results.append({
            "n": n,
            "m": m,
            "rank_F2": rank_F2,
            "delta_F": delta_F
        })
    
    total_instances = len(results)
    mean_delta_F = sum(result["delta_F"] for result in results) / total_instances
    std_delta_F = math.sqrt(sum((result["delta_F"] - mean_delta_F)**2 for result in results) / total_instances)
    
    conjecture_holds = all(delta_F >= n for result in results for delta_F in [result["delta_F"]] * (n_values.count(result["n"]) * 10))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "GF(2) Rank Defect",
        "metric_value": mean_delta_F,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if all(result["conjecture_holds"] for result in all_results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")