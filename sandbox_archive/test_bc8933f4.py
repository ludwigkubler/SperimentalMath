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
    
    def generate_k_colorable_graph(n, k):
        if n <= 1 or k < 2:
            return None
        graph = {i: set() for i in range(n)}
        colors = list(range(k))
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 0:
                    color = random.choice(colors)
                    graph[i].add(j)
                    graph[j].add(i)
        return graph
    
    def polynomial_representation(graph):
        n = len(graph)
        poly = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            poly[0][i] = 1
            for j in graph[i]:
                poly[j][i] = 1
        return poly
    
    def min_local_ring_norm(poly):
        n = len(poly)
        rank = 0
        for row in poly:
            if any(row):
                rank += 1
        return rank
    
    def communication_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * n
        queue = []
        for i in range(n):
            if not visited[i]:
                queue.append(i)
                while queue:
                    node = queue.pop(0)
                    if not visited[node]:
                        visited[node] = True
                        rank += 1
                        for neighbor in graph[node]:
                            if not visited[neighbor]:
                                queue.append(neighbor)
        return rank
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n))
        if var_x == 0 or var_y == 0:
            return 0
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_max = 40
    instances_tested = 30
    min_ring_norms = []
    communication_ranks = []
    
    for _ in range(instances_tested):
        k = random.randint(2, 5)
        graph = generate_k_colorable_graph(n_max, k)
        if graph is None:
            continue
        
        poly = polynomial_representation(graph)
        min_ring_norm = min_local_ring_norm(poly)
        communication_rank_val = communication_rank(graph)
        
        min_ring_norms.append(min_ring_norm)
        communication_ranks.append(communication_rank_val)
    
    if len(min_ring_norms) < instances_tested:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(min_ring_norms),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    correlation = correlation_coefficient(min_ring_norms, communication_ranks)
    expected_correlation = 0.5
    if abs(correlation - expected_correlation) <= 0.1:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Correlation {correlation} not within ±0.1 of expected {expected_correlation}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")