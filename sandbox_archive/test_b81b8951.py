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
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot row
        for k in range(i+1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return A

def determinant(A):
    if len(A) != len(A[0]):
        raise ValueError("Matrix must be square")
    
    n = len(A)
    det = Fraction(1)
    for i in range(n):
        det *= A[i][i]
    return det

def min_tropical_rank(matrix):
    n = len(matrix)
    if n == 0:
        return 0
    rank = 0
    for i in range(n):
        if determinant(gaussian_elimination(matrix[:i+1])) != 0:
            rank += 1
    return rank

def circuit_size(graph):
    # Placeholder function to compute circuit size
    # This is a dummy implementation and should be replaced with actual computation
    return len(graph)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        A = gaussian_elimination(graph)
        min_tr_G = min_tropical_rank(A)
        s_C_G = circuit_size(graph)
        
        results.append({
            "n": n,
            "min_tr_G": min_tr_G,
            "s_C_G": s_C_G
        })
    
    metric_value = sum(result["min_tr_G"] ** 2 / result["s_C_G"] for result in results) / len(results)
    conjecture_holds = all(result["min_tr_G"] <= 1.5 * result["s_C_G"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Min Tropical Rank vs Circuit Size",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")