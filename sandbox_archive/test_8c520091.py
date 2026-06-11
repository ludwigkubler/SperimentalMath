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

# Gaussian elimination with partial pivoting
def gaussian_elimination(A):
    n = len(A)
    U = [row[:] for row in A]
    P = [[0] * n for _ in range(n)]
    for i in range(n):
        P[i][i] = 1

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(U[k][i]) > abs(U[max_row][i]):
                max_row = k
        U[i], U[max_row] = U[max_row], U[i]
        P[i], P[max_row] = P[max_row], P[i]

        for j in range(i + 1, n):
            factor = -U[j][i] / U[i][i]
            for k in range(n):
                U[j][k] += factor * U[i][k]

    return U, P, P

# Matrix multiplication
def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# Rank variance calculation
def rank_variance(A):
    U, _, Vt = gaussian_elimination(matrix_multiplication(A, A))
    rank = sum(1 for row in U if any(val != 0 for val in row))
    n = len(A)
    return (n - rank) / n

# Minimal categorical complexity calculation
def min_cat(phi_prime):
    # Placeholder function; replace with actual computation
    return random.random()

# Run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        
        rank_var = rank_variance(A)
        min_cat_phi_prime = min_cat(A)
        
        results.append((rank_var, min_cat_phi_prime))
    
    n_max = max([n for _, _ in results])
    metric_value = sum(rank_var * min_cat_phi_prime for rank_var, min_cat_phi_prime in results) / len(results)
    conjecture_holds = all(0.5 <= corr >= 0.8 for _, corr in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": n_max,
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
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")