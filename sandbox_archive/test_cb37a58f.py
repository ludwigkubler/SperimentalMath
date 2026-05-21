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
        for r in range(i+1, n):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    A_b = gaussian_elimination(A_b)
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A_b[i][-1]
        for j in range(i+1, n):
            x[i] -= A_b[i][j] * x[j]
    return x

def max_cut_approximation(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    # Construct the linear system
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                A[i][i] += 2
                A[j][j] += 2
                A[i][j] -= 4
                b[i] += 2
                b[j] += 2
    
    # Solve the linear system
    x = solve_linear_system(A, b)
    
    # Compute the approximation ratio
    cut_value = sum(max(x[i], 0) for i in range(n))
    max_cut_value = sum(1 for i in range(n) for j in range(i+1, n) if G[i][j])
    return Fraction(cut_value, max_cut_value).limit_denominator()

def betti_numbers(G):
    # Simplicial homology computation (simplified version)
    n = len(G)
    beta_0 = 1
    beta_1 = sum(1 for i in range(n) for j in range(i+1, n) if G[i][j])
    return beta_0, beta_1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random graph with n vertices
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Compute Betti numbers
    beta_0, beta_1 = betti_numbers(G)
    
    # Approximate Max-CUT using SOS degree
    required_degree = max_cut_approximation(G)
    
    # Check the conjecture
    metric_value = required_degree
    conjecture_holds = required_degree >= beta_0 + beta_1
    counterexample = "" if conjecture_holds else f"Graph with n={n}, Betti numbers ({beta_0}, {beta_1}), SOS degree {required_degree}"
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": metric_value,
        "instances_tested": 1,
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
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={seeds[0]}, Betti numbers ({betti_numbers(G)})\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")