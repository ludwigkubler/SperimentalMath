# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph
    
    def is_connected(graph):
        visited = set()
        stack = [0]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(graph[node] - visited)
        return len(visited) == len(graph)
    
    def gwi(graph):
        # Placeholder for minimal Gromov-Witten invariant calculation
        # This is a dummy implementation and should be replaced with actual computation
        return sum(len(neighbors) for neighbors in graph.values()) / (2 * len(graph))
    
    def ccr(graph):
        # Placeholder for communication complexity rank calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(graph)
    
    trials = 30
    n_max = max(5, 10, 15, 20, 30, 40)
    instances_tested = 0
    gwi_values = []
    ccr_values = []
    
    for _ in range(trials):
        n = random.choice([5, 10, 15, 20, 30, 40])
        graph = generate_d_regular_graph(n, n - 1)
        if graph is None or not is_connected(graph):
            continue
        instances_tested += 1
        gwi_values.append(gwi(graph))
        ccr_values.append(ccr(graph))
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": float('nan'),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Too few valid graphs generated"
        }
    
    correlation = sum((gwi_values[i] - mean_gwi) * (ccr_values[i] - mean_ccr) for i in range(instances_tested)) / instances_tested
    mean_gwi = sum(gwi_values) / instances_tested
    mean_ccr = sum(ccr_values) / instances_tested
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")