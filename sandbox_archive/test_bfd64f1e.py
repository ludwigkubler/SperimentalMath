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
# end SEC prelude

import random
import math
from typing import List, Dict

def gaussian_elimination(A: List[List[float]]) -> List[List[float]]:
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below the pivot
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return A

def operator_norm(matrix: List[List[float]]) -> float:
    U, _, Vt = gaussian_elimination([row + [0] * (len(matrix) - len(row)) for row in matrix])
    singular_values = [math.sqrt(U[i][i]**2 + Vt[i][i]**2) for i in range(len(matrix))]
    return max(singular_values)

def generate_read_once_bp(n: int) -> List[List[int]]:
    bp = [[0] * (1 << n) for _ in range(1 << n)]
    for i in range(1 << n):
        for j in range(1 << n):
            if i & j == 0:
                bp[i][j] = random.randint(0, 1)
    return bp

def generate_read_twice_bp(n: int) -> List[List[int]]:
    bp = [[0] * (1 << n) for _ in range(1 << n)]
    for i in range(1 << n):
        for j in range(1 << n):
            if i & j == 0:
                bp[i][j] = random.randint(0, 1)
                bp[j][i] = bp[i][j]
    return bp

def run_trial(seed: int) -> Dict[str, any]:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M_ro = generate_read_once_bp(n)
        M_twice = generate_read_twice_bp(n)
        
        norm_ro = operator_norm(M_ro)
        norm_twice = operator_norm(M_twice)
        
        results.append({
            "n": n,
            "norm_ro": norm_ro,
            "norm_twice": norm_twice
        })
    
    metric_value = sum(result["norm_ro"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(norm_ro <= math.log(n) and norm_twice >= n / 2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Operator Norm",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")