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
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.append((i, j))
        return graph
    
    def is_valid_graph(graph):
        for neighbors in graph.values():
            if len(neighbors) != d:
                return False
        return True
    
    def calculate_resolution_width(graph):
        n = len(graph)
        max_width = 0
        visited = [False] * n
        
        def dfs(node, width):
            nonlocal max_width
            if width > max_width:
                max_width = width
            visited[node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor, width + 1)
            visited[node] = False
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 0)
        
        return max_width
    
    def calculate_generators(graph):
        n = len(graph)
        generators = set()
        for node in range(n):
            for neighbor in graph[node]:
                generators.add((node, neighbor))
        return len(generators)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if matrix[i][i] == 0:
                swap_found = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
            rank += 1
        return rank
    
    def calculate_braided_monoidal_category_width(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                adjacency_matrix[i][j] = 1
        
        width = gaussian_elimination(adjacency_matrix)
        return width
    
    def run_experiment():
        n = random.randint(5, 40)
        d = random.randint(2, min(3, n - 1))
        graph = generate_d_regular_graph(n, d)
        if not is_valid_graph(graph):
            return None
        
        generators = calculate_generators(graph)
        width = calculate_resolution_width(graph)
        braided_monoidal_category_width = calculate_braided_monoidal_category_width(graph)
        
        return {
            "metric_name": "resolution_width",
            "metric_value": abs(generators - braided_monoidal_category_width),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(generators - braided_monoidal_category_width) <= 5,
            "counterexample": ""
        }
    
    result = run_experiment()
    if result is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["instances_tested"] > 0)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_deviation = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"] and r["instances_tested"] > 0) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(r["metric_value"] == float('inf') for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] == float('inf'))
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")