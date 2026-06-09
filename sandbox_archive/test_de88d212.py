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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph

    def compute_braided_quantum_group_representation(graph):
        n = len(graph)
        dim = 1
        for neighbors in graph.values():
            dim *= len(neighbors) + 1
        return dim

    def compute_circuit_complexity(graph):
        # Placeholder function; actual implementation required
        return random.randint(10, 50)

    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, d=3)
        if graph is None:
            continue
        dim = compute_braided_quantum_group_representation(graph)
        circuit_complexity = compute_circuit_complexity(graph)
        metrics.append((dim, circuit_complexity))
    
    if len(metrics) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    dims = [m[0] for m in metrics]
    complexities = [m[1] for m in metrics]
    
    mean_dim = sum(dims) / len(dims)
    mean_complexity = sum(complexities) / len(complexities)
    
    covariance = sum((dims[i] - mean_dim) * (complexities[i] - mean_complexity) for i in range(len(dims))) / len(dims)
    variance_dim = sum((dims[i] - mean_dim) ** 2 for i in range(len(dims))) / len(dims)
    variance_complexity = sum((complexities[i] - mean_complexity) ** 2 for i in range(len(complexities))) / len(complexities)
    
    correlation_coefficient = covariance / (math.sqrt(variance_dim) * math.sqrt(variance_complexity))
    
    t_statistic = correlation_coefficient * math.sqrt(len(dims) - 2) / math.sqrt(1 - correlation_coefficient ** 2)
    p_value = 2 * (1 - math.erf(abs(t_statistic) / math.sqrt(2)))
    
    conjecture_holds = correlation_coefficient >= 0.9 and p_value < 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9 or p_value >= 0.05"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")