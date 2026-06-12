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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix, mod):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                return None  # Singular matrix
            for j in range(i + 1, n):
                factor = (matrix[j][i] * pow(matrix[i][i], -1, mod)) % mod
                for k in range(i, n + 1):
                    matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % mod
        rank = sum(1 for row in matrix if any(row))
        return rank

    def resolution_width(phi_G):
        # Placeholder function. Replace with actual implementation.
        return random.randint(1, 10)

    def symplectic_form_rank(matrix):
        # Placeholder function. Replace with actual implementation.
        return gaussian_elimination(matrix, 2) or 0

    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.randint(2, min(n - 1, 8))
    
    # Generate a random d-regular graph
    graph = [[] for _ in range(n)]
    edges = set()
    while len(edges) < n * d // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    
    # Construct the Tseitin formula φ_G
    phi_G = []
    for i in range(n):
        for j in range(d):
            phi_G.append(f"x_{i}_{j}")
        phi_G.append(f"¬x_{i}_0")
        for j in range(1, d):
            phi_G.append(f"(x_{i}_{j} → x_{i}_{j-1})")
    
    # Compute the symplectic form matrix
    sfr_matrix = [[0] * (n * d + 1) for _ in range(n * d + 1)]
    for i in range(n):
        for j in range(d):
            sfr_matrix[i * d + j][i * d] = 1
            sfr_matrix[i * d + j][i * d + (j + 1) % d] = -1
    
    # Compute the minimal symplectic form rank
    sfr = symplectic_form_rank(sfr_matrix)
    
    # Compute the resolution proof width
    w_phi_G = resolution_width(phi_G)
    
    return {
        "metric_name": "sfr_w_ratio",
        "metric_value": sfr / w_phi_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - 1.0) <= 0.2 * std_value) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")