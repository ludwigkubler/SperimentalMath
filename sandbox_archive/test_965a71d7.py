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
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def is_connected(graph):
        n = len(graph)
        visited = [False] * n
        stack = [0]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in range(n):
                    if graph[u][v] == 1 and not visited[v]:
                        stack.append(v)
        return all(visited)
    
    def find_orbits(graph):
        n = len(graph)
        orbits = []
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                orbit = []
                queue = [i]
                while queue:
                    u = queue.pop()
                    if not visited[u]:
                        visited[u] = True
                        orbit.append(u)
                        for v in range(n):
                            if graph[u][v] == 1 and not visited[v]:
                                queue.append(v)
                orbits.append(orbit)
        return orbits
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            pivot = None
            for j in range(i, m):
                if matrix[j][i] != 0:
                    pivot = j
                    break
            if pivot is not None:
                rank += 1
                for k in range(n):
                    matrix[i][k], matrix[pivot][k] = matrix[pivot][k], matrix[i][k]
                for j in range(m):
                    if j != i:
                        factor = -matrix[j][i] / matrix[i][i]
                        for k in range(n):
                            matrix[j][k] += factor * matrix[i][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            graph = generate_graph(n, int(3 * n / 4))
            if not is_connected(graph):
                continue
            orbits = find_orbits(graph)
            rank = matrix_rank(graph)
            if rank == 0:
                continue
            metric_value = len(orbits) / rank
            total_metric_value += metric_value
            instances_tested += 1
            n_max = max(n_max, n)
            
            if conjecture_holds and metric_value < n:
                conjecture_holds = False
                counterexample = f"Orbits: {len(orbits)}, Rank: {rank}, Ratio: {metric_value}"
    
    return {
        "metric_name": "Orbit Width Ratio",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")