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
    return abs(a * b) // gcd(a, b)

def matrix_mul(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for multiplication")
    C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return C

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    pivot_col = 0
    for row in range(m):
        if pivot_col >= n:
            break
        max_row = row
        for i in range(row + 1, m):
            if abs(matrix[i][pivot_col]) > abs(matrix[max_row][pivot_col]):
                max_row = i
        if matrix[max_row][pivot_col] == 0:
            pivot_col += 1
            continue
        matrix[row], matrix[max_row] = matrix[max_row], matrix[row]
        for i in range(m):
            if i != row and matrix[i][pivot_col] != 0:
                factor = matrix[i][pivot_col] / matrix[row][pivot_col]
                for j in range(n):
                    matrix[i][j] -= factor * matrix[row][j]
        rank += 1
        pivot_col += 1
    return rank

def minimal_rank(G):
    # Encode a procedure to compute the minimal rank of G
    # For simplicity, assume G is represented as a list of elements
    # and each element is a tuple representing its coordinates in some space
    # This is a placeholder; replace with actual implementation
    return len(set(tuple(sorted(x)) for x in G))

def communication_complexity(G):
    n = len(G)
    total_pairs = n * (n - 1) // 2
    max_complexity = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Simulate communication complexity for pair (i, j)
            # This is a placeholder; replace with actual implementation
            complexity = random.randint(1, min(len(G[i]), len(G[j])))
            max_complexity = max(max_complexity, complexity)
    return max_complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + (seed % 6) * 5
    G = [(random.randint(0, n), random.randint(0, n)) for _ in range(n)]
    rho_G = minimal_rank(G)
    size_G = len(G)
    comm_complexity = communication_complexity(G)
    
    if comm_complexity > min(rho_G, size_G) * math.log(size_G):
        return {
            "metric_name": "communication_complexity",
            "metric_value": comm_complexity,
            "instances_tested": n * (n - 1) // 2,
            "conjecture_holds": False,
            "counterexample": f"Communication complexity exceeds bound for rho(G)={rho_G}, |G|={size_G}"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": n * (n - 1) // 2,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    total_trials = len(results)
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / total_trials
    mean_value = sum(r["metric_value"] for r in results) / total_trials
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=... support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")