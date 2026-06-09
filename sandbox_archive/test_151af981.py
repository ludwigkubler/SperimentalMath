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
    
    def generate_random_graph(n):
        graph = {i: {} for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    graph[i][j] = True
                    graph[j][i] = True
        return graph
    
    def dpll_tree_height(graph):
        def dfs(node, visited):
            if node not in graph or all(visited[n] for n in graph[node]):
                return 1
            visited[node] = True
            height = 0
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    height = max(height, dfs(neighbor, visited))
            visited[node] = False
            return height + 1
        
        visited = {node: False for node in graph}
        max_height = 0
        for node in graph:
            max_height = max(max_height, dfs(node, visited.copy()))
        return max_height
    
    def min_categorical_dimension(graph):
        n = len(graph)
        if n == 0:
            return 0
        
        # Temperley-Lieb algebra implementation (simplified version)
        def tl_algebra(n):
            if n == 1:
                return [[1]]
            else:
                result = []
                for sub_result in tl_algebra(n - 2):
                    result.append([1] + [0] * (n - 2) + [1])
                    for i in range(1, n - 1):
                        new_row = [0] * (n - 1)
                        new_row[i] = 1
                        new_row[i + 1] = -1
                        result.append(new_row + [0])
                return result
        
        tl_matrix = tl_algebra(n)
        rank = 0
        for row in tl_matrix:
            if any(row):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        min_dim = min_categorical_dimension(graph)
        height = dpll_tree_height(graph)
        
        if min_dim == 0 or height == 0:
            continue
        
        results.append({
            "n": n,
            "min_dim": min_dim,
            "height": height
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    n_values = [r["n"] for r in results]
    min_dims = [r["min_dim"] for r in results]
    heights = [r["height"] for r in results]
    
    mean_min_dim = sum(min_dims) / len(min_dims)
    mean_height = sum(heights) / len(heights)
    
    correlation_coefficient = 0
    if len(n_values) > 1:
        numerator = sum((min_dims[i] - mean_min_dim) * (heights[i] - mean_height) for i in range(len(n_values)))
        denominator = math.sqrt(sum((min_dims[i] - mean_min_dim) ** 2 for i in range(len(n_values))) *
                                sum((heights[i] - mean_height) ** 2 for i in range(len(n_values))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(min_dim - (height * 1.5)) <= 3 for min_dim, height in zip(min_dims, heights)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")