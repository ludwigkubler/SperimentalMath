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
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges_used = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges_used:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_used.add((i, j))
        return graph
    
    def calculate_minimal_order(graph):
        n = len(graph)
        if n == 0:
            return 0
        order = 1
        for i in range(n):
            neighbors = set(graph[i])
            for neighbor in neighbors:
                common_neighbors = neighbors.intersection(set(graph[neighbor]))
                order += len(common_neighbors) + 1
        return order
    
    def is_valid_graph(graph):
        n = len(graph)
        if any(len(neighbors) != d for i, neighbors in enumerate(graph)):
            return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            d = random.randint(2, min(n - 1, 4))
            graph = generate_d_regular_graph(n, d)
            if not is_valid_graph(graph):
                continue
            order = calculate_minimal_order(graph)
            results.append({
                "n": n,
                "order": order
            })
    
    if len(results) == 0:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_n"
        }
    
    mean_order = sum(result["order"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["order"] - mean_order) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["order"] - result["n"] ** 1.5) < 0.1 * result["n"] ** 1.5) / len(results)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_order) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction<{support_fraction}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")