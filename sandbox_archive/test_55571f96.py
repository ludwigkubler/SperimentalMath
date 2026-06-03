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
        if (n * d) % 2 != 0 or d < 1 or n < d:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph
    
    def is_valid_d_regular_graph(graph, d):
        for neighbors in graph.values():
            if len(neighbors) != d:
                return False
        return True
    
    def compute_minimal_hodge_diamond_width(graph):
        n = len(graph)
        hodge_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        hodge_matrix[0][0] = 1
        for i in range(1, n + 1):
            hodge_matrix[i][i] = 1
            for j in range(i - 1, -1, -1):
                hodge_matrix[j][i] = sum(hodge_matrix[j + k][i - 1] for k in range(j + 1))
        return max(max(row) for row in hodge_matrix)
    
    def compute_circuit_monotone_width(graph):
        n = len(graph)
        if not is_valid_d_regular_graph(graph, d):
            return float('inf')
        
        # Simplified monotone circuit width calculation
        return n * (n - 1) // 2
    
    def pearson_correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        return numerator / denominator if denominator != 0 else float('nan')
    
    def mean_absolute_difference(x, y):
        return sum(abs(xi - yi) for xi, yi in zip(x, y)) / len(x)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Invalid d-regular graph generated"
        }
    
    hdw = compute_minimal_hodge_diamond_width(graph)
    w_m = compute_circuit_monotone_width(graph)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient([hdw], [w_m]),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": pearson_correlation_coefficient([hdw], [w_m]) >= 0.8 and mean_absolute_difference([hdw], [w_m]) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")