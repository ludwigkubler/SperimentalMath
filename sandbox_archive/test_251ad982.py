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
    
    def generate_graph(n, m):
        if n <= 0 or m < n - 1 or m > (n * (n - 1)) // 2:
            return None
        edges = set()
        while len(edges) < m:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)
    
    def adjacency_matrix(graph, n):
        adj = [[0] * n for _ in range(n)]
        for u, v in graph:
            adj[u][v] = 1
            adj[v][u] = 1
        return adj
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return rank(matrix[:i] + matrix[i+1:])
            for j in range(i + 1, m):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))
    
    def orbits(graph):
        n = len(graph)
        adj = adjacency_matrix(graph, n)
        visited = [False] * n
        orbit_count = 0
        
        def dfs(node):
            stack = [node]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for v in range(n):
                        if adj[u][v] == 1 and not visited[v]:
                            stack.append(v)
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
                orbit_count += 1
        
        return orbit_count
    
    def alpha(n):
        # Simple linear function for demonstration
        return n / 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_graph(n, random.randint(2 * n - 1, 3 * n - 1))
        if graph is None:
            continue
        orbit_count = orbits(graph)
        adj_rank = rank(adjacency_matrix(graph, n))
        if adj_rank == 0:
            continue
        ratio = Fraction(orbit_count, adj_rank)
        results.append({"n": n, "orbit_count": orbit_count, "adj_rank": adj_rank, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "Orbit Width Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Graph generation failed for all instances"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] >= alpha(result["n"]) for result in results)
    counterexample = "" if conjecture_holds else "Orbit: {}, Rank: {}".format(
        max(results, key=lambda x: x["orbit_count"])["orbit_count"],
        max(results, key=lambda x: x["adj_rank"])["adj_rank"]
    )
    
    return {
        "metric_name": "Orbit Width Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")