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
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        factor = A[i][i]
        for j in range(i+1, n):
            A[j][i] /= factor
    
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def matrix_rank(M):
    A = [row[:] for row in M]
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Ensure no zero rows or columns
    while any(sum(row) == 0 for row in M):
        M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    while any(sum(col) == 0 for col in zip(*M)):
        M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    dim_secant_variety = matrix_rank(M)
    metric_value = dim_secant_variety
    instances_tested = 1
    
    conjecture_holds = dim_secant_variety >= 0.8 * n
    counterexample = "" if conjecture_holds else "dim(σ(M)) < 0.8n"
    
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='dim(σ(M)) < 0.8n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")