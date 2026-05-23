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
from fractions import Fraction
import math

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.add((i, j))
    return edges

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        pivot = None
        for j in range(rank, m):
            if matrix[j][i] != 0:
                pivot = j
                break
        if pivot is None:
            continue
        matrix[pivot], matrix[rank] = matrix[rank], matrix[pivot]
        for j in range(n):
            if j == i:
                continue
            factor = -matrix[rank][j] / matrix[rank][i]
            for k in range(m):
                matrix[k][j] += factor * matrix[k][i]
        rank += 1
    return rank

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    if m == 0 or n == 0:
        return 0
    augmented_matrix = [row + [1 if j == i else 0 for j in range(n)] for i, row in enumerate(matrix)]
    rank = gaussian_elimination(augmented_matrix)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        Tseitin_length = 2 ** (n // 2)  # Simplified estimation of resolution proof length
        
        M = [[0] * n for _ in range(n)]
        for u, v in graph:
            M[u][v] = M[v][u] = 1
        
        rank_M = matrix_rank(M)
        
        results.append({
            "n": n,
            "Tseitin_length": Tseitin_length,
            "rank_M": rank_M
        })
    
    max_rank = max(result["rank_M"] for result in results)
    conjecture_holds = all(max_rank >= 2 ** (result["n"] // 2) for result in results)
    
    return {
        "metric_name": "Rank of Symplectic Matrix / Tseitin Proof Length",
        "metric_value": max_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Graph with n={results[max_rank == 0]['n']} and proof length {results[max_rank == 0]['Tseitin_length']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={results[0]['n']} and proof length {results[0]['Tseitin_length']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")