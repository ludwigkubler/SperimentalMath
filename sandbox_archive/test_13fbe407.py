# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

# Helper functions for matrix operations and graph generation
def matmul(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    return [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        # Find pivot
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate below
        for j in range(i + 1, n):
            factor = Fraction(M[j][i], M[i][i])
            M[j] = [M[j][k] - factor * M[i][k] for k in range(n)]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(M[i][-1], M[i][i])
        for j in range(i-1, -1, -1):
            M[j][-1] -= M[j][i] * x[i]
    
    return x

def generate_random_graph(n):
    G = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                G[i][j] = G[j][i] = 1
    return G

def local_induction_degree_bound(G):
    n = len(G)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                A[i][j] = 1
                A[j][i] = 1
    
    # Compute the rank of the adjacency matrix
    rank_A = len(gaussian_elimination(A))
    
    return rank_A

def communication_complexity_rank_variance(G):
    n = len(G)
    R = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                R[i][j] = 1
                R[j][i] = 1
    
    # Compute the rank of the communication matrix
    rank_R = len(gaussian_elimination(R))
    
    return rank_R**2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        LIDB_sum = 0
        RCV_sum = 0
        instances_tested = 0
        
        for _ in range(5):  # Sample 5 instances per size
            G = generate_random_graph(n)
            LIDB = local_induction_degree_bound(G)
            RCV = communication_complexity_rank_variance(G)
            
            if RCV <= n**2:
                LIDB_sum += LIDB
                RCV_sum += RCV
                instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        mean_LIDB = Fraction(LIDB_sum, instances_tested)
        mean_RCV = Fraction(RCV_sum, instances_tested)
        
        results.append({
            "n": n,
            "mean_LIDB": mean_LIDB,
            "mean_RCV": mean_RCV
        })
    
    if not results:
        return {
            "metric_name": "LIDB vs RCV",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    n_max = max(result["n"] for result in results)
    LIDB_values = [result["mean_LIDB"] for result in results]
    RCV_values = [result["mean_RCV"] for result in results]
    
    # Pearson correlation coefficient
    mean_LIDB = sum(LIDB_values) / len(LIDB_values)
    mean_RCV = sum(RCV_values) / len(RCV_values)
    numerator = sum((x - mean_LIDB) * (y - mean_RCV) for x, y in zip(LIDB_values, RCV_values))
    denominator = (sum((x - mean_LIDB)**2 for x in LIDB_values) * sum((y - mean_RCV)**2 for y in RCV_values))**0.5
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    # Absolute differences
    abs_diffs = [abs(x - y) for x, y in zip(LIDB_values, RCV_values)]
    mean_abs_diff = sum(abs_diffs) / len(abs_diffs)
    
    return {
        "metric_name": "LIDB vs RCV",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested * len(n_values),
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")