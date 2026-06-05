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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u in range(n):
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(f'-{literals[v]}')
            clauses.append(clause)
        for u in range(n):
            for v in range(u+1, n):
                if v not in graph[u] and u not in graph[v]:
                    clauses.append([f'{literals[u]}', f'{literals[v]}'])
                    clauses.append([f'-{literals[u]}', f'-{literals[v]}'])
        return clauses
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def minimal_tropical_hodge_dimension(clauses):
        n = len(clauses)
        matrix = [[0] * (n+1) for _ in range(n)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal.startswith('x'):
                    j = int(literal[1:])
                    matrix[i][j] += 1
                elif literal.startswith('-x'):
                    j = int(literal[2:])
                    matrix[i][j] -= 1
        reduced_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in reduced_matrix if any(row))
        return n - rank
    
    def circuit_depth(clauses):
        depth = 0
        visited = [False] * len(clauses)
        stack = []
        for i, clause in enumerate(clauses):
            if not visited[i]:
                stack.append((i, 1))
                while stack:
                    node, current_depth = stack.pop()
                    visited[node] = True
                    depth = max(depth, current_depth)
                    for literal in clause:
                        if literal.startswith('x'):
                            j = int(literal[1:])
                            if not visited[j]:
                                stack.append((j, current_depth + 1))
        return depth
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n-1, 6))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "minimal_tropical_hodge_dimension",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    clauses = tseitin_formula(graph)
    mhd = minimal_tropical_hodge_dimension(clauses)
    depth = circuit_depth(clauses)
    
    return {
        "metric_name": "minimal_tropical_hodge_dimension",
        "metric_value": mhd,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mhd <= 1.5 * depth,
        "counterexample": "" if mhd <= 1.5 * depth else f"mhd(G) = {mhd}, d(φ_G) = {depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 2 * r["n_max"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] > 2 * r["n_max"])
        print(f"RESULT: FALSIFIED counterexample=\"mhd(G) > 2 * d(φ_G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")