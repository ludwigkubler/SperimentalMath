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
        graph = {i: set() for i in range(n)}
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        random.shuffle(edges)
        for u, v in edges[:n-1]:
            graph[u].add(v)
            graph[v].add(u)
        return graph
    
    def communication_complexity_rank_variance(graph):
        # Placeholder for actual computation
        # This is a dummy function that returns a random value for demonstration
        return random.random()
    
    def minimal_representation_degree(graph):
        # Placeholder for actual computation
        # This is a dummy function that returns a random value for demonstration
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        d_G = minimal_representation_degree(graph)
        r_G = communication_complexity_rank_variance(graph)
        results.append((n, d_G, r_G))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    d_values = [d_G for _, d_G, _ in results]
    r_values = [r_G for _, _, r_G in results]
    
    mean_d = sum(d_values) / len(d_values)
    mean_r = sum(r_values) / len(r_values)
    variance_d = sum((x - mean_d) ** 2 for x in d_values) / len(d_values)
    variance_r = sum((x - mean_r) ** 2 for x in r_values) / len(r_values)
    
    correlation_coefficient = (sum((d_values[i] - mean_d) * (r_values[i] - mean_r) for i in range(len(results))) /
                               math.sqrt(variance_d * variance_r))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")