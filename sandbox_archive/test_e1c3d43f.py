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
    
    def generate_k_regular_graph(n, k):
        if (n * k) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < k and len(graph[j]) < k and (i, j) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph
    
    def calculate_k_theory_rank(graph):
        # Simplified K-theory rank calculation for demonstration
        n = len(graph)
        rank = 0
        for node in graph:
            if len(graph[node]) == k:
                rank += 1
        return rank
    
    def calculate_communication_complexity_rank(graph):
        # Simplified communication complexity rank calculation for demonstration
        n = len(graph)
        rank = 0
        for node in graph:
            rank += len(graph[node])
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    rk_K_values = []
    r_G_values = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            graph = generate_k_regular_graph(n, k=3)
            if graph is None:
                continue
            rk_K = calculate_k_theory_rank(graph)
            r_G = calculate_communication_complexity_rank(graph)
            rk_K_values.append(rk_K)
            r_G_values.append(r_G)
    
    if not rk_K_values or not r_G_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_rk_K = sum(rk_K_values) / len(rk_K_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)
    variance_rk_K = sum((x - mean_rk_K) ** 2 for x in rk_K_values) / len(rk_K_values)
    variance_r_G = sum((x - mean_r_G) ** 2 for x in r_G_values) / len(r_G_values)
    
    if variance_rk_K == 0 or variance_r_G == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(rk_K_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    covariance = sum((rk_K_values[i] - mean_rk_K) * (r_G_values[i] - mean_r_G) for i in range(len(rk_K_values)))
    correlation_coefficient = covariance / (math.sqrt(variance_rk_K) * math.sqrt(variance_r_G))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(rk_K_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")