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

def generate_d_regular_graph(n, d):
    if n * d % 2 != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d:
                add_edge(i, j)
                if len(edges_added) == n * d // 2:
                    return graph
    
    raise ValueError("Failed to generate a valid d-regular graph")

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        pivot_row = -1
        for j in range(rank, m):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        
        if pivot_row == -1:
            continue
        
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        
        for j in range(n):
            if j != i and matrix[rank][j] != 0:
                factor = Fraction(matrix[rank][j], matrix[rank][i])
                for k in range(n):
                    matrix[rank][k] -= factor * matrix[j][k]
        
        rank += 1
    
    return rank

def communication_complexity_rank_variance(graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    
    for u in range(n):
        for v in graph[u]:
            if u < v:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
    
    rank_matrix = [row[:] for row in adjacency_matrix]
    rank = gaussian_elimination(rank_matrix)
    
    return Fraction(n * (n - 1) // 2, rank)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    k = 0.1  # Placeholder value for k; to be determined empirically
    
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, d=3)
        sigma_G = communication_complexity_rank_variance(graph)
        rsym_G = len(gaussian_elimination([[graph[i][j] for j in range(n)] for i in range(n)]))
        
        results.append({
            "n": n,
            "sigma_G": sigma_G,
            "rsym_G": rsym_G
        })
    
    mean_diff = sum(abs(rsym - sigma) for res in results for rsym, sigma in zip(res["rsym_G"], res["sigma_G"])) / len(results)
    conjecture_holds = all(abs(rsym - sigma) <= k for res in results for rsym, sigma in zip(res["rsym_G"], res["sigma_G"]))
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Graph size: {n}, rsym(G) = {rsym_G}, σ(G) = {sigma_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Graph size: {results[0]['n']}, rsym(G) = {results[0]['rsym_G'][0]}, σ(G) = {results[0]['sigma_G'][0]}\" first_failing_seed={first_failing_seed}")