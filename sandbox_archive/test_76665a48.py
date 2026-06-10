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
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        degree_sum = n * d
        edges = degree_sum // 2
        vertices = list(range(n))
        
        for _ in range(edges):
            u = random.choice(vertices)
            v = random.choice(vertices)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
        
        return graph
    
    def calculate_geometric_complexity(graph):
        n = len(graph)
        degree_sum = sum(len(neighbors) for neighbors in graph)
        return Fraction(degree_sum, 2 * n)
    
    def calculate_boolean_circuit_size(n):
        # Simplified heuristic based on vertex count
        return n ** 2
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(2, min(n - 1, 3))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        geoc = calculate_geometric_complexity(graph)
        s_phi_G = calculate_boolean_circuit_size(n)
        
        results.append((geoc, s_phi_G))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    geoc_values, s_phi_G_values = zip(*results)
    n_max = max(n for _, _ in results)
    
    mean_geoc = sum(geoc_values) / len(geoc_values)
    mean_s_phi_G = sum(s_phi_G_values) / len(s_phi_G_values)
    
    covariance = sum((x - mean_geoc) * (y - mean_s_phi_G) for x, y in zip(geoc_values, s_phi_G_values))
    variance_geoc = sum((x - mean_geoc) ** 2 for x in geoc_values)
    variance_s_phi_G = sum((y - mean_s_phi_G) ** 2 for y in s_phi_G_values)
    
    if variance_geoc == 0 or variance_s_phi_G == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = covariance / (math.sqrt(variance_geoc) * math.sqrt(variance_s_phi_G))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")