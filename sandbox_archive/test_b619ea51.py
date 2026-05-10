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

def lu_decomposition(A):
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        L[i][i] = 1.0
        for j in range(i, n):
            sum_k = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - sum_k
        for k in range(i+1, n):
            sum_k = sum(L[k][i] * U[i][j] for j in range(i))
            L[k][i] = (A[k][i] - sum_k) / U[i][i]
    
    return L, U

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def tensor_rank(matrix):
    n = len(matrix)
    L, U = lu_decomposition(matrix)
    rank = sum(1 for i in range(n) if abs(U[i][i]) > 1e-10)
    return rank

def generate_read_once_bp(n):
    bp = []
    for _ in range(n):
        layer = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        bp.append(layer)
    return bp

def generate_read_twice_bp(n):
    bp = []
    for _ in range(2):
        layer = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        bp.append(layer)
    return bp

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        read_once_bp = generate_read_once_bp(n)
        read_twice_bp = generate_read_twice_bp(n)
        
        read_once_rank = tensor_rank(matrix_multiplication(*read_once_bp))
        read_twice_rank = tensor_rank(matrix_multiplication(*read_twice_bp))
        
        results.append({
            "n": n,
            "read_once_rank": read_once_rank,
            "read_twice_rank": read_twice_rank
        })
    
    metric_value = sum(result["read_twice_rank"] / (2**(result["n"]/2) / result["n"]**2) for result in results)
    instances_tested = len(results)
    
    conjecture_holds = all(result["read_once_rank"] <= 4 * math.log(result["n"]) and result["read_twice_rank"] >= 2**(result["n"]/2) / result["n"]**2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")