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
    n = 40
    d = 3
    
    # Generate a random d-regular graph with n vertices
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d >= n:
            raise ValueError("Invalid parameters for generating a d-regular graph")
        
        adjacency_matrix = [[0] * n for _ in range(n)]
        edges_added = set()
        
        def add_edge(u, v):
            if u == v or (u, v) in edges_added or (v, u) in edges_added:
                return False
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
            edges_added.add((u, v))
            edges_added.add((v, u))
            return True
        
        for i in range(n):
            neighbors = random.sample(range(n), d)
            while not all(add_edge(i, j) for j in neighbors):
                neighbors = random.sample(range(n), d)
        
        return adjacency_matrix
    
    graph = generate_d_regular_graph(n, d)
    
    # Compute the order of the minimal automorphism group |A_G|
    def is_automorphism(graph, perm):
        n = len(graph)
        for i in range(n):
            for j in range(i + 1, n):
                if (graph[i][j] != graph[perm[i]][perm[j]]):
                    return False
        return True
    
    def find_minimal_automorphism_group(graph):
        n = len(graph)
        identity = list(range(n))
        automorphisms = [identity]
        
        for perm in itertools.permutations(range(n)):
            if is_automorphism(graph, perm) and all(perm[i] != i for i in range(n)):
                automorphisms.append(perm)
        
        return automorphisms
    
    A_G = find_minimal_automorphism_group(graph)
    order_A_G = len(A_G)
    
    # Compute the communication complexity rank variance σ(G)
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if all(matrix[i][j] == 0 for j in range(n)):
                continue
            pivot_row = i
            for j in range(i + 1, m):
                if matrix[j][i] != 0:
                    matrix[pivot_row], matrix[j] = matrix[j], matrix[pivot_row]
                    break
            else:
                continue
            rank += 1
            for j in range(m):
                if j == pivot_row:
                    continue
                factor = -matrix[j][i] / matrix[pivot_row][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[pivot_row][k]
        return rank
    
    sigma_G = matrix_rank(graph)
    
    # Compute the correlation coefficient r^2 between |A_G| and σ(G)
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy ** 2
    
    x = [order_A_G]
    y = [sigma_G]
    
    r_squared = correlation_coefficient(x, y)
    
    # Determine if the conjecture holds
    conjecture_holds = r_squared >= 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": r_squared,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_squared = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")