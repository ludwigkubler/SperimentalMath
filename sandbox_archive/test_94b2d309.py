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
        if A[i][i] == 0:
            # Swap with a row below that has a non-zero pivot
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        factor = Fraction(1, A[i][i])
        for j in range(n):
            A[i][j] *= factor
        for k in range(n):
            if k != i and A[k][i] != 0:
                multiplier = -A[k][i]
                for j in range(n):
                    A[k][j] += multiplier * A[i][j]
    return A

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    for i in range(n):
        if all(matrix[i][j] == 0 for j in range(m)):
            continue
        rank += 1
        for j in range(m):
            matrix[i][j] /= matrix[i][i]
        for k in range(n):
            if k != i and not all(matrix[k][j] == 0 for j in range(m)):
                multiplier = -matrix[k][i]
                for j in range(m):
                    matrix[k][j] += multiplier * matrix[i][j]
    return rank

def generate_k_clique_instance(n, k):
    if n < k:
        raise ValueError("n must be at least k")
    vertices = list(range(n))
    edges = []
    while len(edges) < k - 1:
        u = random.choice(vertices)
        v = random.choice(vertices)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    return vertices, edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        while instances_tested < 30:
            vertices, edges = generate_k_clique_instance(n, k=5)
            A = [[0] * n for _ in range(n)]
            for u, v in edges:
                A[u][v] = 1
                A[v][u] = 1
            
            try:
                rank_A = rank(gaussian_elimination(A))
                total_rank += rank_A
                instances_tested += 1
            except ValueError as e:
                continue
        
        if instances_tested == 0:
            return {
                "metric_name": "Tropicalized Rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "matrix_singular"
            }
        
        avg_rank = total_rank / instances_tested
        results.append(avg_rank)
    
    mean_rank = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    
    return {
        "metric_name": "Tropicalized Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": mean_rank <= n ** (1/4) + 0.1 * n ** (1/4),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 32))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        results.append(trial_result["metric_value"])
    
    mean_rank = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    
    if all(result <= n ** (1/4) + 0.1 * n ** (1/4) for result, n in zip(results, [n_values[0] for _ in range(len(results))])):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction=1")
    else:
        first_failing_seed = next(seed for seed, result, n in zip(seeds, results, [n_values[0] for _ in range(len(results))]) if result > n ** (1/4) + 0.1 * n ** (1/4))
        print(f"RESULT: FALSIFIED counterexample=\"rank_exceeds_bound\" first_failing_seed={first_failing_seed}")