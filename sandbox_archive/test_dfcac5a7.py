# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def generate_k_regular_graph(n, k):
    degree_counts = [0] * n
    graph = [[] for _ in range(n)]
    
    for i in range(k * n // 2):
        while True:
            u, v = random.sample(range(n), 2)
            if u == v or len(graph[u]) >= k or len(graph[v]) >= k or (u in graph[v] or v in graph[u]):
                continue
            graph[u].append(v)
            graph[v].append(u)
            degree_counts[u] += 1
            degree_counts[v] += 1
            break
    
    return graph

def laplacian_eigenvalues(graph):
    n = len(graph)
    D = [sum(1 for _ in neighbors) for neighbors in graph]
    L = [[0] * n for _ in range(n)]
    
    for u, neighbors in enumerate(graph):
        L[u][u] = -len(neighbors)
        for v in neighbors:
            L[u][v] = 1
    
    eigenvalues = []
    for i in range(n):
        eigenvector = [0] * n
        eigenvector[i] = 1
        value = sum(L[i][j] * eigenvector[j] for j in range(n))
        eigenvalues.append(value)
    
    return sorted(eigenvalues)

def max_cut(graph):
    n = len(graph)
    best_cut_value = 0
    
    def dfs(u, visited, cut_value, current_cut):
        visited[u] = True
        if u in current_cut:
            cut_value += sum(1 for v in graph[u] if not visited[v])
        else:
            cut_value -= sum(1 for v in graph[u] if not visited[v])
        
        for v in graph[u]:
            if not visited[v]:
                dfs(v, visited, cut_value, current_cut)
    
    for i in range(2 ** n):
        current_cut = [j for j in range(n) if (i >> j) & 1]
        visited = [False] * n
        dfs(0, visited, 0, current_cut)
        best_cut_value = max(best_cut_value, abs(cut_value))
    
    return best_cut_value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n, k in [(8, 3), (10, 3), (12, 3), (14, 3), (16, 3), (10, 4), (12, 4), (14, 4)]:
        for _ in range(30):
            graph = generate_k_regular_graph(n, k)
            eigenvalues = laplacian_eigenvalues(graph)
            h_G = len(set(eigenvalue for eigenvalue in eigenvalues if eigenvalue != 0))
            lambda_max = max(eigenvalues)
            MC_G = max_cut(graph)
            rho_G = n * lambda_max / (4 * MC_G) - 1
            r = n * rho_G / (h_G * math.log2(n + 1))
            
            results.append(r)
    
    if any(r >= 2 for r in results):
        return {
            "metric_name": "r",
            "metric_value": max(results),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"max(r) = {max(results)} ≥ 2"
        }
    
    mean_r = sum(results) / len(results)
    return {
        "metric_name": "r",
        "metric_value": max(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial["metric_value"])
    
    mean_r = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r < 2) / len(results)
    if all(r < 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0 support_fraction={support_fraction}")
    elif any(r >= 2 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='max(r) ≥ 2' first_failing_seed={first_failing_seed}")