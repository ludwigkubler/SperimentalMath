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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges_added:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_added.add((i, j))
        return graph
    
    def circuit_monotone_width(graph):
        n = len(graph)
        if n == 0:
            return 0
        visited = [False] * n
        width = 0
        
        def dfs(node, parent, level):
            nonlocal width
            visited[node] = True
            max_level = level
            for neighbor in graph[node]:
                if neighbor != parent:
                    child_level = dfs(neighbor, node, level + 1)
                    max_level = max(max_level, child_level)
            width = max(width, max_level - level + 1)
            return max_level
        
        for i in range(n):
            if not visited[i]:
                dfs(i, -1, 0)
        
        return width
    
    def order_of_quotient_space(graph):
        n = len(graph)
        if n == 0:
            return 0
        visited = [False] * n
        
        def dfs(node, parent):
            visited[node] = True
            count = 1
            for neighbor in graph[node]:
                if neighbor != parent and not visited[neighbor]:
                    count += dfs(neighbor, node)
            return count
        
        components = 0
        for i in range(n):
            if not visited[i]:
                components += 1
                dfs(i, -1)
        
        return n // components
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)  # Assuming d=2 for simplicity
        if graph is None:
            continue
        
        width = circuit_monotone_width(graph)
        order = order_of_quotient_space(graph)
        
        if width == 0 or order == 0:
            continue
        
        results.append({
            "n": n,
            "width": width,
            "order": order
        })
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    n_values = [result["n"] for result in results]
    widths = [result["width"] for result in results]
    orders = [result["order"] for result in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = (sum((xi - mean_x) ** 2 for xi in x) * sum((yi - mean_y) ** 2 for yi in y)) ** 0.5
        return numerator / denominator if denominator != 0 else 0
    
    correlation_coefficient = pearson_correlation(orders, widths)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["metric_value"] is not None for result in results):
        mean_metric = sum(result["metric_value"] for result in results) / len(results)
        std_metric = (sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"No significant correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Some seeds did not produce a valid metric value")