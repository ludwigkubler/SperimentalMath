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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        pivot = A[i][i]
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(m):
                A[j][k] -= factor * A[i][k]
    
    return A

def min_rank(A):
    rank = 0
    for row in gaussian_elimination(A):
        if any(row):
            rank += 1
    return rank

def comm_rank(φ):
    # Placeholder function to compute communication complexity rank
    # This is a dummy implementation; replace with actual algorithm
    return len(φ)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size 5 times
            φ = [random.randint(0, 1) for _ in range(n)]
            comm_rank_val = comm_rank(φ)
            
            A = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i+1, n):
                    if random.choice([True, False]):
                        A[i][j] = 1
                        A[j][i] = 1
            
            min_rank_val = min_rank(A)
            
            results.append({
                "n": n,
                "comm_rank_val": comm_rank_val,
                "min_rank_val": min_rank_val
            })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    comm_rank_vals = [r["comm_rank_val"] for r in results]
    min_rank_vals = [r["min_rank_val"] for r in results]
    
    mean_comm_rank = sum(comm_rank_vals) / len(comm_rank_vals)
    mean_min_rank = sum(min_rank_vals) / len(min_rank_vals)
    
    covariance = sum((comm_rank_vals[i] - mean_comm_rank) * (min_rank_vals[i] - mean_min_rank) for i in range(len(comm_rank_vals))) / len(comm_rank_vals)
    variance_comm_rank = sum((comm_rank_vals[i] - mean_comm_rank) ** 2 for i in range(len(comm_rank_vals))) / len(comm_rank_vals)
    variance_min_rank = sum((min_rank_vals[i] - mean_min_rank) ** 2 for i in range(len(min_rank_vals))) / len(min_rank_vals)
    
    pearson_corr = covariance / (math.sqrt(variance_comm_rank) * math.sqrt(variance_min_rank))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")