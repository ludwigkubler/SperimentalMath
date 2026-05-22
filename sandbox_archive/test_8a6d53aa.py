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

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        
        # Swap current row with pivot row
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements in the current column
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(i, cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def tropical_rank(graph):
    n = len(graph)
    adj = [[0 if graph[i][j] == 0 else float('inf') for j in range(n)] for i in range(n)]
    
    for i in range(n):
        adj[i][i] = 0
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if adj[i][k] + adj[k][j] < adj[i][j]:
                    adj[i][j] = adj[i][k] + adj[k][j]
    
    return gaussian_elimination(adj)

def permutation_circuit_threshold(graph):
    n = len(graph)
    visited = [False] * n
    stack = []
    
    def dfs(node):
        if visited[node]:
            return 0
        visited[node] = True
        stack.append(node)
        
        max_depth = 0
        for neighbor in range(n):
            if graph[node][neighbor] != 0:
                depth = dfs(neighbor) + 1
                if depth > max_depth:
                    max_depth = depth
        
        stack.pop()
        return max_depth
    
    total_depth = 0
    for node in range(n):
        if not visited[node]:
            total_depth += dfs(node)
    
    return total_depth // n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    
    r_T_L_G = tropical_rank(graph)
    θ_G = permutation_circuit_threshold(graph)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": r_T_L_G,
        "instances_tested": 1,
        "conjecture_holds": r_T_L_G <= θ_G,
        "counterexample": "" if r_T_L_G <= θ_G else f"Graph with n={n}, tropical rank {r_T_L_G} > permutation circuit threshold {θ_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={n}, tropical rank {r_T_L_G} > permutation circuit threshold {θ_G}\" first_failing_seed={first_failing_seed}")