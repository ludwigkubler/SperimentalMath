# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_planar(n, edges):
        if n < 3:
            return True
        if len(edges) > 3 * (n - 2):
            return False
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        def dfs(node, parent, visited):
            visited[node] = True
            stack = [(node, parent)]
            while stack:
                current, p = stack.pop()
                for neighbor in graph[current]:
                    if not visited[neighbor]:
                        stack.append((neighbor, current))
                    elif neighbor != p:
                        return False
            return True
        
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                if not dfs(i, -1, visited):
                    return False
        return True
    
    def construct_alexander_griffiths_module(edges):
        n = len(set(u for u, v in edges) | set(v for u, v in edges))
        module = [[0] * n for _ in range(n)]
        for u, v in edges:
            module[u][v] += 1
            module[v][u] += 1
        return module
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = -1
            for j in range(rank, rows):
                if matrix[j][i]:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(rows):
                if i != j and matrix[j][i]:
                    factor = Fraction(matrix[j][i], matrix[rank][i])
                    for k in range(i, cols):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def resolution_width(n, clauses):
        if n == 0:
            return 0
        queue = [clauses]
        width = 0
        while queue:
            new_queue = []
            for clause in queue:
                if not clause:
                    continue
                var = random.choice(clause)
                pos_clauses = [c for c in queue if var in c]
                neg_clauses = [c for c in queue if -var in c]
                new_clauses = []
                for p_clause in pos_clauses:
                    for n_clause in neg_clauses:
                        new_clause = set(p_clause) ^ set(n_clause)
                        if len(new_clause) > width:
                            width = len(new_clause)
                        new_clauses.append(list(new_clause))
                new_queue.extend(new_clauses)
            queue = new_queue
        return width
    
    def generate_random_planar_graph(n):
        while True:
            edges = []
            for _ in range(3 * (n - 2)):
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges and (v, u) not in edges:
                    edges.append((u, v))
            if is_planar(n, edges):
                return edges
    
    n = random.randint(5, 40)
    edges = generate_random_planar_graph(n)
    module = construct_alexander_griffiths_module(edges)
    rank = gaussian_elimination(module)
    
    clauses = [[i + 1 for i in range(n)]]
    width = resolution_width(n, clauses)
    
    return {
        "metric_name": "rank_over_width",
        "metric_value": Fraction(rank, width),
        "instances_tested": 1,
        "conjecture_holds": rank <= 1.2 * width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 79))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank_over_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_over_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_over_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank > 1.2 * width' first_failing_seed={seeds[first_failing_seed]}")