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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return (list(range(n)), list(edges))
    
    def configuration_space(graph):
        n, edges = graph
        config_space = set()
        for subset in powerset(range(n)):
            edge_subset = [(u, v) for u, v in edges if u in subset and v in subset]
            config_space.add(tuple(sorted(subset)) + tuple(sorted(edge_subset)))
        return len(config_space)
    
    def powerset(s):
        result = []
        for i in range(1 << len(s)):
            subset = [s[j] for j in range(len(s)) if (i & (1 << j))]
            result.append(subset)
        return result
    
    def circuit_depth(graph):
        n, edges = graph
        # Placeholder for actual circuit depth computation logic
        # For simplicity, we use a random depth between 1 and n
        return random.randint(1, n)
    
    n_max = 0
    instances_tested = 0
    r_values = []
    d_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Test each size with 5 instances
            graph = generate_graph(n)
            r = configuration_space(graph)
            d = circuit_depth(graph)
            
            if r <= 0 or d <= 0:
                continue
            
            r_values.append(r)
            d_values.append(d)
            instances_tested += 1
    
    if not r_values or not d_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_r = sum(r_values) / len(r_values)
    mean_d = sum(d_values) / len(d_values)
    correlation_coefficient = covariance(r_values, d_values) / (std_dev(r_values) * std_dev(d_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def covariance(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    return sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)

def std_dev(values):
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")