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
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if any(A[i]):
            rank += 1
    return rank

def fundamental_group(G):
    # Compute the adjacency matrix of G
    n = len(G)
    adj_matrix = [[0] * n for _ in range(n)]
    for u, v in G:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    
    # Compute the Laplacian matrix L = D - A
    degree_sum = [sum(row) for row in adj_matrix]
    laplacian = [[degree_sum[i] - adj_matrix[i][j] if i == j else -adj_matrix[i][j] for j in range(n)] for i in range(n)]
    
    # Compute the kernel of L to get the fundamental group
    ker_L = gaussian_elimination(laplacian)
    return rank_of_matrix(ker_L)

def communication_complexity(A):
    n = len(A)
    count = 0
    for i in range(n):
        for j in range(i+1, n):
            if A[i][j] == 1:
                count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random graph with n vertices
    n = random.randint(5, 40)
    G = []
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < 0.3:  # Edge probability
                G.append((i, j))
    
    # Compute the fundamental group dimension and communication complexity
    dim = fundamental_group(G)
    cc = communication_complexity(G)
    
    # Check if the communication complexity scales exponentially with the dimension of the fundamental group
    conjecture_holds = abs(cc - 2**dim) < 1e-6 * 2**dim
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"CC(Aut_G) = {cc}, dim(π₁(G)) = {dim}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_cc)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")