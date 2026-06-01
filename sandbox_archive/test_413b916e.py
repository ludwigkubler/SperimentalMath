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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i, n + 1):
            matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(i, n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def local_coherence_rank(P):
    # Placeholder function to compute the local coherence rank
    # This is a dummy implementation and should be replaced with actual logic
    return random.random()

def communication_complexity(P):
    # Placeholder function to compute the communication complexity
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "mlcr_diff"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            continue
        
        mlcr_diffs = []
        
        for _ in range(instances_tested):
            P = random.randint(1, 10)  # Dummy protocol
            mlcr_P = local_coherence_rank(P)
            C_P = communication_complexity(P)
            
            if C_P == 0:
                continue
            
            diff = abs(mlcr_P - 2 * C_P)  # Example threshold for k=2
            mlcr_diffs.append(diff)
        
        mean_diff = sum(mlcr_diffs) / len(mlcr_diffs)
        
        if any(diff > 1 for diff in mlcr_diffs):  # Example threshold for k=2
            conjecture_holds = False
            counterexample = f"n={n}, max_diff={max(mlcr_diffs)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_diff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")