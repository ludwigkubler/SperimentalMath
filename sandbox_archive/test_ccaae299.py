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

def generate_graph(n, max_degree):
    graph = [[] for _ in range(n)]
    degrees = [0] * n
    edges_added = 0
    
    while edges_added < min(n - 1, max_degree * (n - 1) // 2):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        
        if u != v and v not in graph[u] and degrees[u] < max_degree and degrees[v] < max_degree:
            graph[u].append(v)
            graph[v].append(u)
            degrees[u] += 1
            degrees[v] += 1
            edges_added += 1
    
    return graph

def dpll_length(graph):
    n = len(graph)
    
    def dfs(node, parent, path):
        if node in path:
            return len(path) - path.index(node)
        
        path.append(node)
        min_length = float('inf')
        
        for neighbor in graph[node]:
            if neighbor != parent:
                length = dfs(neighbor, node, path)
                if length < min_length:
                    min_length = length
        
        path.pop()
        return min_length
    
    max_length = 0
    for i in range(n):
        length = dfs(i, -1, [])
        if length > max_length:
            max_length = length
    
    return max_length

def gaussian_elimination(A):
    n = len(A)
    m = len(A[0])
    
    def swap_rows(A, i, j):
        A[i], A[j] = A[j], A[i]
    
    def scale_row(A, i, factor):
        for j in range(m):
            A[i][j] *= factor
    
    def add_multiple_of_row(A, i, j, factor):
        for k in range(m):
            A[i][k] += factor * A[j][k]
    
    def find_pivot(A, row):
        for col in range(m):
            if A[row][col] != 0:
                return col
        return -1
    
    def forward_elimination(A):
        i = 0
        j = 0
        
        while i < n and j < m:
            pivot_col = find_pivot(A, i)
            
            if pivot_col == -1:
                i += 1
                continue
            
            swap_rows(A, i, j)
            scale_row(A, i, Fraction(1, A[i][pivot_col]))
            
            for k in range(n):
                if k != i and A[k][pivot_col] != 0:
                    add_multiple_of_row(A, k, i, -A[k][pivot_col])
            
            i += 1
            j += 1
    
    forward_elimination(A)
    
    rank = sum(1 for row in A if any(x != 0 for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    max_degree = min(n - 1, 3)
    graph = generate_graph(n, max_degree)
    
    dpll_len = dpll_length(graph)
    
    if dpll_len == 0:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    # Construct the polynomial f
    A = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            A[u][v] += 1
    
    rank = gaussian_elimination(A)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= dpll_len,
        "counterexample": f"Graph with DPLL length {dpll_len} and rank {rank}" if rank < dpll_len else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with DPLL length {result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")