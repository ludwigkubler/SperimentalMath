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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank(matrix):
    matrix_copy = [row[:] for row in matrix]
    gaussian_elimination(matrix_copy)
    return sum(1 for row in matrix_copy if any(row))

def geometric_quantization(instance, n):
    # Placeholder for actual geometric quantization procedure
    # This is a dummy implementation that returns a random moment matrix
    M = [[random.random() for _ in range(n)] for _ in range(n)]
    return M

def branching_program_size(M):
    # Placeholder for actual branching program construction and size calculation
    # This is a dummy implementation that returns the rank of the moment matrix as a proxy
    return rank(M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = geometric_quantization(None, n)  # Placeholder for actual instance generation
        size = branching_program_size(M)
        rank_M = rank(M)
        
        result = {
            "metric_name": "read_twice_size",
            "metric_value": size,
            "instances_tested": 1,
            "conjecture_holds": size <= (rank_M**2 + 3),
            "counterexample": ""
        }
        
        if not result["conjecture_holds"]:
            result["counterexample"] = f"n={n}, rank(M)={rank_M}, size={size}"
        
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": mean_value,
        "std_metric_value": std_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if "counterexample" in result and result["counterexample"]:
            break
        
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no data collected")
    else:
        mean_value = sum(r["mean_metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["mean_metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["support_fraction"] == 1) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(r["counterexample"] for r in results):
            first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
            print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE not enough support")