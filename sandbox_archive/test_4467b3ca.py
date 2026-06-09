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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_communication_problem(n):
        # Generate a random communication complexity problem with rank variance R
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A, B
    
    def compute_rank_variance(A, B):
        # Compute the rank variance R
        n = len(A)
        rank_A = sum(1 for row in A if any(row))
        rank_B = sum(1 for col in zip(*B) if any(col))
        rank_AB = sum(1 for i in range(n) for j in range(n) if A[i][j] and B[j][i])
        R = (rank_A + rank_B - 2 * rank_AB) / n
        return R
    
    def compute_mgi(A, B):
        # Compute the minimal noncommutative geometric invariant mgi(data_space)
        # This is a placeholder function. Replace with actual computation.
        n = len(A)
        mgi_value = sum(sum(row[i] * col[i] for i in range(n)) for row in A for col in B) / (n ** 2)
        return mgi_value
    
    def covariance(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        return cov
    
    def variance(data):
        mean = sum(data) / len(data)
        var = sum((x - mean) ** 2 for x in data) / len(data)
        return var
    
    n_values = [5, 10, 15, 20, 30, 40]
    mgi_values = []
    rank_variance_values = []
    
    for n in n_values:
        A, B = generate_communication_problem(n)
        R = compute_rank_variance(A, B)
        mgi_value = compute_mgi(A, B)
        
        if R <= 0 or mgi_value <= 0:
            continue
        
        mgi_values.append(mgi_value)
        rank_variance_values.append(R)
    
    if not mgi_values or not rank_variance_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(mgi_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    covariance_value = covariance(mgi_values, rank_variance_values)
    variance_mgi = variance(mgi_values)
    variance_rank_variance = variance(rank_variance_values)
    
    if variance_mgi == 0 or variance_rank_variance == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(mgi_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance_value / math.sqrt(variance_mgi * variance_rank_variance)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mgi_values),
        "n_max": max(n_values) if n_values else 0,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")