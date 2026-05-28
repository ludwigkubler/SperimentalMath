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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(m):
        if all(A[i][j] == 0 for j in range(n)):
            continue
        pivot_row = i
        while A[pivot_row][i] == 0:
            pivot_row += 1
            if pivot_row == m:
                return rank
        for j in range(i, n):
            A[pivot_row][j], A[i][j] = A[i][j], A[pivot_row][j]
        for k in range(m):
            if k != i:
                factor = A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
        rank += 1
    return rank

def generate_read_twice_bp(n):
    width = random.randint(2, 5)
    bp = []
    for _ in range(width):
        layer = [random.choice([0, 1]) for _ in range(n)]
        bp.append(layer)
    return bp

def construct_crossed_product_algebra(bp):
    n = len(bp[0])
    F2 = [[0, 1], [1, 0]]
    M = []
    for i in range(2*n):
        row = [0] * (2*n)
        for j in range(n):
            if bp[i % width][j] == 1:
                row[2*j + (i // width)] = F2[(i // width) % 2]
        M.append(row)
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_read_twice_bp(n)
        M = construct_crossed_product_algebra(bp)
        rank_M = matrix_rank(M)
        
        if rank_M < n:
            return {
                "metric_name": "rank",
                "metric_value": rank_M,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank_M} is less than {n}"
            }
        
        results.append((n, rank_M))
    
    mean_rank = sum(rank for _, rank in results) / len(results)
    std_rank = math.sqrt(sum((rank - mean_rank)**2 for _, rank in results) / len(results))
    support_fraction = all(rank >= n for _, rank in results)
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank less than n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")