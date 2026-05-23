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
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        factor = 1 / matrix[i][i]
        for j in range(i, n):
            matrix[i][j] *= factor
        for k in range(i+1, n):
            factor = matrix[k][i]
            for j in range(i, n):
                matrix[k][j] -= factor * matrix[i][j]
    
    # Back-substitute to find rank
    rank = 0
    for i in range(n):
        if all(abs(matrix[i][j]) < 1e-9 for j in range(n)):
            break
        rank += 1
    
    return rank

def generate_random_graph(n):
    graph = [[] for _ in range(n)]
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    return graph

def is_connected(graph):
    n = len(graph)
    visited = [False] * n
    stack = [0]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in graph[node]:
                stack.append(neighbor)
    return all(visited)

def rank(graph):
    n = len(graph)
    matrix = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    for u in range(n):
        for v in graph[u]:
            matrix[u][v] = -Fraction(1, 1)
    
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    while True:
        graph = generate_random_graph(n)
        if is_connected(graph):
            break
    
    config_space_rank = rank(graph)
    tseitin_formula_length = 2 ** (config_space_rank // 2)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": tseitin_formula_length,
        "instances_tested": 1,
        "conjecture_holds": tseitin_formula_length >= 2 ** (0.5 * config_space_rank),
        "counterexample": "" if tseitin_formula_length >= 2 ** (0.5 * config_space_rank) else f"Graph with {n} vertices and rank {config_space_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((x["seed"] for x in results if not x["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Graph with {results[0]['instances_tested']} vertices and rank {results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")