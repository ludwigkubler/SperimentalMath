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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Eliminate non-pivot elements
        factor = Fraction(1, matrix[i][i])
        for j in range(i, n):
            matrix[i][j] *= factor

        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]

    rank = sum(1 for row in matrix if any(row))
    return rank

def laplacian_matrix(graph):
    n = len(graph)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(graph[i][j] for j in range(n) if graph[i][j])
        L[i][i] = -degree
        for j in range(i + 1, n):
            L[i][j] = graph[i][j]
            L[j][i] = graph[j][i]
    return L

def tropical_rank(matrix):
    n = len(matrix)
    T = [[max(0, matrix[i][j]) for j in range(n)] for i in range(n)]
    return gaussian_elimination(T)

def generate_random_graph(n):
    graph = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            graph[i][j] = graph[j][i]
    return graph

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        L_G = laplacian_matrix(graph)
        rho_L_G = tropical_rank(L_G)
        
        T_L_IP_2 = [[max(0, i - j) if i != j else 0 for j in range(n)] for i in range(n)]
        rho_L_IP_2 = gaussian_elimination(T_L_IP_2)
        
        results.append({
            "n": n,
            "rho_L_G": rho_L_G,
            "rho_L_IP_2": rho_L_IP_2
        })
    
    mean_rho_L_G = sum(result["rho_L_G"] for result in results) / len(results)
    std_rho_L_G = (sum((result["rho_L_G"] - mean_rho_L_G) ** 2 for result in results) / len(results)) ** 0.5
    
    conjecture_holds = all(rho_L_G <= n * 10 and rho_L_IP_2 >= n**2 for result in results)
    
    return {
        "metric_name": "rho_L_G",
        "metric_value": mean_rho_L_G,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Graph with n={results[0]['n']}, rho_L_G={results[0]['rho_L_G']}, rho_L_IP_2={results[0]['rho_L_IP_2']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=2) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={results[0]['n']}, rho_L_G={results[0]['rho_L_G']}, rho_L_IP_2={results[0]['rho_L_IP_2']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")