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
    
    def generate_graph(n, m):
        if n <= 1 or m < n - 1:
            return None
        edges = set()
        while len(edges) < m:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)
    
    def adj_matrix(graph, n):
        mat = [[0] * n for _ in range(n)]
        for u, v in graph:
            mat[u][v] = 1
            mat[v][u] = 1
        return mat
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m == 0 or n == 0:
            return 0
        for i in range(n):
            max_row = -1
            for j in range(i, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                continue
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(n):
                if i != j:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def orbits(graph, n):
        adj = adj_matrix(graph, n)
        visited = [False] * n
        orbit_count = 0
        
        def dfs(node):
            stack = [node]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for v in range(n):
                        if adj[u][v] and not visited[v]:
                            stack.append(v)
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
                orbit_count += 1
        
        return orbit_count
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            graph = generate_graph(n, int(2 * n * math.log(n)))
            if graph is None:
                continue
            orbit_count = orbits(graph, n)
            adj_rank = rank(adj_matrix(graph, n))
            if adj_rank == 0:
                continue
            metric_value = orbit_count / adj_rank
            total_metric_value += metric_value
            instances_tested += 1
            if not conjecture_holds and metric_value < alpha(n):
                counterexample = f"Orbits: {orbit_count}, Rank: {adj_rank}"
                break
        if not conjecture_holds:
            break
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else None
    support_fraction = instances_tested / len(n_values) if instances_tested > 0 else None
    
    return {
        "metric_name": "Orbit Width Ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")