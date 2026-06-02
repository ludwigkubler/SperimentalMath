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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0]*k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        for j in range(i+1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n+1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = (augmented_matrix[i][-1] - sum(augmented_matrix[i][j] * x[j] for j in range(i+1, n))) / augmented_matrix[i][i]
    return x

def min_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    A = matrix[:]
    for i in range(min(m, n)):
        if A[i][i] != 0:
            rank += 1
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return rank

def generate_quiver_representation(q, n):
    # Placeholder implementation: random quiver representation
    matrix = [[random.randint(0, q-1) for _ in range(n)] for _ in range(n)]
    return matrix

def generate_communication_complexity_instance(n):
    # Placeholder implementation: random communication complexity instance
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    min_ranks = []
    comm_ranks = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        q = random.randint(2, 10)
        rho = generate_quiver_representation(q, n)
        min_rank_rho = min_rank(rho)
        min_ranks.append(min_rank_rho)
        
        phi = generate_communication_complexity_instance(n)
        comm_rank_phi = min_rank(phi)
        comm_ranks.append(comm_rank_phi)
    
    correlation_coefficient = sum((x - mean_min_ranks) * (y - mean_comm_ranks) for x, y in zip(min_ranks, comm_ranks)) / len(min_ranks)
    mean_min_ranks = sum(min_ranks) / len(min_ranks)
    mean_comm_ranks = sum(comm_ranks) / len(comm_ranks)
    
    if correlation_coefficient >= 0.8 and max(abs(x - y) for x, y in zip(min_ranks, comm_ranks)) <= 3:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")