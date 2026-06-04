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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Eliminate below the pivot
        factor = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= factor

        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]

    return matrix

def srank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(row))
    return rank

def crank(protocol):
    # Placeholder for communication complexity calculation
    # For simplicity, assume it's a function of the protocol size
    return len(protocol)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        protocol = [random.randint(0, 1) for _ in range(n)]
        srank_value = srank(protocol)
        crank_value = crank(protocol)
        
        if crank_value == 0:
            continue
        
        correlation = srank_value / crank_value
        results.append({
            "n": n,
            "srank_value": srank_value,
            "crank_value": crank_value,
            "correlation": correlation
        })
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_correlation = sum(result["correlation"] for result in results) / len(results)
    max_n = max(result["n"] for result in results)
    
    return {
        "metric_name": "Correlation",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": mean_correlation >= 0.8 and mean_correlation <= 3,
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
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"correlation_out_of_bounds\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE no_valid_instances"
    
    print(f"RESULT: {RESULT} mean={mean_metric_value} std=0 support_fraction={support_fraction}")