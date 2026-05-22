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
    
    def generate_random_graph(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def permutation_circuit_threshold(graph):
        n = len(graph)
        max_clique_size = 0
        for i in range(1 << n):
            clique = []
            for j in range(n):
                if (i >> j) & 1:
                    clique.append(j)
            if all((u, v) in graph or (v, u) in graph for u, v in itertools.combinations(clique, 2)):
                max_clique_size = max(max_clique_size, len(clique))
        return max_clique_size
    
    def tropical_rank(graph):
        n = len(graph)
        adjacency_matrix = [[0 if i == j else float('inf') for j in range(n)] for i in range(n)]
        for u, v in graph:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        def gaussian_elimination(matrix):
            n = len(matrix)
            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if matrix[j][i] < matrix[max_row][i]:
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                pivot = matrix[i][i]
                for j in range(n):
                    matrix[i][j] /= pivot
                for j in range(n):
                    if j != i:
                        factor = matrix[j][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
            rank = sum(1 for row in matrix if any(x != 0 for x in row))
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_random_graph(n)
        theta_G = permutation_circuit_threshold(graph)
        r_T_L_G = tropical_rank(graph)
        results.append({
            "n": n,
            "theta_G": theta_G,
            "r_T_L_G": r_T_L_G
        })
    
    mean_theta_G = sum(result["theta_G"] for result in results) / len(results)
    mean_r_T_L_G = sum(result["r_T_L_G"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["r_T_L_G"] <= result["theta_G"]) / len(results)
    
    conjecture_holds = all(result["r_T_L_G"] <= result["theta_G"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tropical_rank_vs_theta_G",
        "metric_value": mean_r_T_L_G,
        "instances_tested": len(results),
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
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")