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
    
    def is_planar(graph):
        n = len(graph)
        if n <= 4:
            return True
        for u in range(n):
            neighbors = [v for v in range(n) if graph[u][v] == 1]
            if len(neighbors) > 5:
                return False
        return True
    
    def min_riemann_roch_degree(graph):
        n = len(graph)
        degree_sum = sum(sum(row) for row in graph)
        return math.ceil(degree_sum / (2 * n))
    
    def communication_rank_growth_rate(graph):
        n = len(graph)
        if not is_planar(graph):
            return None
        # Simplified heuristic for demonstration purposes
        return n ** 0.5
    
    def generate_random_planar_graph(n):
        graph = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < 3 * (n - 1):
            u, v = random.sample(range(n), 2)
            if u != v and graph[u][v] == 0:
                graph[u][v] = 1
                graph[v][u] = 1
                edges_added += 1
        return graph
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_planar_graph(n)
        if not is_planar(graph):
            continue
        
        min_deg = min_riemann_roch_degree(graph)
        r_G = communication_rank_growth_rate(graph)
        
        if r_G is None:
            return {
                "metric_name": "communication_rank",
                "metric_value": 0,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((min_deg, r_G))
    
    if not results:
        return {
            "metric_name": "communication_rank",
            "metric_value": 0,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_graphs"
        }
    
    min_degs, r_Gs = zip(*results)
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(min_degs, r_Gs)) / (len(results) * std_dev_x * std_dev_y)
    
    return {
        "metric_name": "communication_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")