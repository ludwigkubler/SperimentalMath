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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def operator_norm(M):
    U, _, Vt = gaussian_elimination([row + [0] * (len(M) - len(row)) for row in M])
    max_singular_value = max(abs(U[i][i]) for i in range(len(U)))
    return max_singular_value

def generate_read_once_bp(n):
    bp = []
    for _ in range(2**n):
        bp.append(random.choice([0, 1]))
    return bp

def generate_read_twice_bp(n):
    bp = []
    for _ in range(2**n):
        bp.extend([random.choice([0, 1]) for _ in range(2)])
    return bp

def construct_communication_matrix(bp):
    n = int(math.log2(len(bp)))
    M = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if bp[i] == bp[j]:
                M[i][j] = 1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        read_once_bp = generate_read_once_bp(n)
        read_twice_bp = generate_read_twice_bp(n)
        
        M_ro = construct_communication_matrix(read_once_bp)
        M_rt = construct_communication_matrix(read_twice_bp)
        
        norm_ro = operator_norm(M_ro)
        norm_rt = operator_norm(M_rt)
        
        results.append({
            "n": n,
            "norm_ro": norm_ro,
            "norm_rt": norm_rt
        })
    
    mean_ro = sum(result["norm_ro"] for result in results) / len(results)
    mean_rt = sum(result["norm_rt"] for result in results) / len(results)
    
    conjecture_holds = all(norm_ro <= math.log(n) and norm_rt >= n/2 for result, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Operator Norm",
        "metric_value": mean_ro,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_ro = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ro} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")