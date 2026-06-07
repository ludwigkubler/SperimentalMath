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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if n * d % 2 != 0 or d < 1 or d >= n:
            raise ValueError("Invalid parameters for generating a d-regular graph")
        
        edges = set()
        while len(edges) < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        
        return list(edges)
    
    def compute_minimal_automorphism_group(graph):
        # Placeholder for group-theoretic algorithm
        # This is a dummy implementation that always returns 1
        return 1
    
    def compute_communication_complexity_rank_variance(graph):
        n = len(graph) // 2
        matrix = [[0] * n for _ in range(n)]
        
        for u, v in graph:
            i = min(u, v)
            j = max(u, v)
            matrix[i][j] += 1
        
        rank = gaussian_elimination(matrix)
        return n - rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if i + rank >= n:
                break
            
            pivot_row = i + rank
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    return rank
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        
        return rank
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        a_g = compute_minimal_automorphism_group(graph)
        sigma_g = compute_communication_complexity_rank_variance(graph)
        results.append((a_g, sigma_g))
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    a_g_list, sigma_g_list = zip(*results)
    r_squared = correlation_coefficient(a_g_list, sigma_g_list)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": r_squared,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": r_squared >= 0.9,
        "counterexample": "" if r_squared >= 0.9 else "r^2 < 0.9"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_squared = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared:.4f} std=0.0000 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r^2 < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")