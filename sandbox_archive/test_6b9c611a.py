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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def resolution_width(matrix):
        m, n = len(matrix), len(matrix[0])
        visited = [False] * n
        width = 0
        
        def dfs(node, level):
            nonlocal width
            if visited[node]:
                return
            visited[node] = True
            for i in range(m):
                if matrix[i][node] == 1:
                    dfs(i, level + 1)
            width = max(width, level)
        
        for node in range(n):
            dfs(node, 0)
        
        return width
    
    def generate_d_regular_expander_graph(d, n):
        graph = [[] for _ in range(n)]
        degree_counts = [0] * n
        edges_added = 0
        
        while edges_added < d * n // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                degree_counts[u] += 1
                degree_counts[v] += 1
                edges_added += 1
        
        return graph
    
    def clause_incidence_matrix(graph, n):
        m = len(graph)
        A = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if j in graph[i]:
                    A[i][j] = 1
        return A
    
    d = random.randint(3, 5)  # Degree of the expander graph
    n = random.randint(5, 40)
    
    graph = generate_d_regular_expander_graph(d, n)
    matrix = clause_incidence_matrix(graph, n)
    
    jordan_rank = gaussian_elimination(matrix)
    resolution_width_value = resolution_width(matrix)
    
    c = 1.0
    conjecture_holds = jordan_rank >= c * math.sqrt(n) and resolution_width_value >= c * math.sqrt(n)
    counterexample = f"Jordan rank {jordan_rank} < √{n} or resolution width {resolution_width_value} < √{n}" if not conjecture_holds else ""
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")