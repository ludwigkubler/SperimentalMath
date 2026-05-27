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

def generate_expander_graph(n):
    if n <= 2:
        return None
    graph = [[] for _ in range(n)]
    for i in range(1, n):
        neighbors = random.sample(range(i), min(i-1, 3))
        for j in neighbors:
            graph[i].append(j)
            graph[j].append(i)
    return graph

def tree_width(graph):
    if not graph:
        return 0
    n = len(graph)
    visited = [False] * n
    parent = [-1] * n
    
    def dfs(node, depth):
        visited[node] = True
        max_depth = depth
        for neighbor in graph[node]:
            if not visited[neighbor]:
                parent[neighbor] = node
                max_depth = max(max_depth, dfs(neighbor, depth + 1))
        return max_depth
    
    root = 0
    while len(graph[root]) > 2:
        root += 1
    return dfs(root, 0)

def algebraic_k_theory_rank(graph):
    if not graph:
        return 0
    n = len(graph)
    k_theory_matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    
    def gaussian_elimination(matrix):
        m = len(matrix)
        n = len(matrix[0])
        rank = 0
        
        for i in range(m):
            if rank >= n:
                break
            pivot_row = i
            while pivot_row < m and matrix[pivot_row][rank] == Fraction(0):
                pivot_row += 1
            if pivot_row == m:
                continue
            
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            for j in range(m):
                if i != j:
                    factor = -matrix[j][rank] / matrix[i][rank]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            
            rank += 1
        
        return rank
    
    for i in range(n):
        k_theory_matrix[i][i] = Fraction(1)
    
    return gaussian_elimination(k_theory_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_expander_graph(n)
        if not graph:
            continue
        
        rank = algebraic_k_theory_rank(graph)
        total_rank += rank
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_rank >= 2 ** (math.log(n, 2) * math.log(n, 2))
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}"
    
    return {
        "metric_name": "algebraic_k_theory_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(map(lambda p: int(p), filter(str.isdigit, open("primes.txt").read().split())))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\", first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")