# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = 1 / matrix[i][i]
        for j in range(n):
            if j != i:
                matrix[j][i] *= factor
        
        # Eliminate above the pivot
        for j in range(i+1, n):
            factor = matrix[j][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def max_cut(G):
    n = len(G)
    best_cut_value = 0
    for cut in combinations(range(n), n//2):
        cut_value = sum(G[u][v] if (u, v) in G else G[v][u] for u in cut for v in cut if (u, v) not in G and (v, u) not in G)
        best_cut_value = max(best_cut_value, cut_value)
    return best_cut_value

def bonami_beckner_kurtosis(G):
    n = len(G)
    K = 20000
    sum_g_G_x = 0
    sum_g_G_x_squared = 0
    for _ in range(K):
        x = [random.choice([-1, 1]) for _ in range(n)]
        g_G_x = sum(x[i] * G[i][j] if (i, j) in G else x[j] * G[i][j] for i, j in combinations(range(n), 2))
        sum_g_G_x += g_G_x
        sum_g_G_x_squared += g_G_x ** 2
    E_g_G_x = sum_g_G_x / K
    E_g_G_x_squared = sum_g_G_x_squared / K
    return (E_g_G_x**4 / E_g_G_x_squared**2) - 3

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10 + (seed % 5) * 4  # n ∈ {10, 14, 18, 20}
    G = {}
    degree_sum = 0
    while degree_sum < 3 * n:
        u, v = random.sample(range(n), 2)
        if (u, v) not in G and (v, u) not in G:
            G[(u, v)] = 1
            degree_sum += 2
    
    max_cut_value = max_cut(G)
    A = [[G.get((i, j), 0) for j in range(n)] for i in range(n)]
    DP_G = n / 2 + n * min(eigenvalue.real for eigenvalue in gaussian_elimination(A).diagonal()) / 4
    kappa_G = bonami_beckner_kurtosis(G)
    
    lhs = (DP_G - max_cut_value) / len(G)
    rhs = 0.5 * max(kappa_G, 1/n)**(1/4)
    
    return {
        "metric_name": "(DP-G) - MaxCut",
        "metric_value": lhs,
        "instances_tested": 1,
        "conjecture_holds": lhs <= rhs,
        "counterexample": "" if lhs <= rhs else f"Counterexample for n={n}, seed={seed}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")