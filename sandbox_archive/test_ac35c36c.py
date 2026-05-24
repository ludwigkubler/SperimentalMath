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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            # Find a non-zero pivot below and swap rows
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                # No non-zero pivot found, skip this column
                continue
        
        factor = Fraction(1, matrix[i][i])
        for j in range(n):
            matrix[i][j] *= factor
        
        for k in range(i + 1, n):
            factor = matrix[k][i]
            for j in range(n):
                matrix[k][j] -= factor * matrix[i][j]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def tropical_rank(matrix):
    n = len(matrix)
    T = [[max(a, b) for a, b in zip(row, col)] for row, col in zip(*matrix)]
    return gaussian_elimination(T)

def laplacian_matrix(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if G[i][j])
        L[i][i] = -degree
        for j in range(i + 1, n):
            L[i][j] = L[j][i] = G[i][j]
    return L

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for n in {5, 10, 15, 20, 30, 40}:
        for _ in range(5):
            G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            L_G = laplacian_matrix(G)
            rho_L_G = tropical_rank(L_G)
            
            L_IP_2 = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            rho_L_IP_2 = gaussian_elimination(L_IP_2)
            
            results.append({
                "metric_name": "rho",
                "metric_value": rho_L_G,
                "instances_tested": 1,
                "conjecture_holds": rho_L_G <= math.log(n) and rho_L_IP_2 >= n**2,
                "counterexample": ""
            })
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = (sum((result["metric_value"] - mean_metric)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")