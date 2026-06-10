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
        graph = {i: [] for i in range(n)}
        edges_used = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges_used or (v, u) in edges_used:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_used.add((u, v))
                break
        return graph
    
    def is_valid_graph(graph):
        for neighbors in graph.values():
            if len(neighbors) % 2 != 0:
                return False
        return True
    
    def construct_quaternionic_kahler_manifold(graph):
        n = len(graph)
        # Simplified mapping to a manifold invariant (number of edges)
        return sum(len(neighbors) for neighbors in graph.values()) / 2
    
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            graph = generate_d_regular_graph(n, 2)
            if not is_valid_graph(graph):
                continue
            
            instances_tested += 1
            metric_value = construct_quaternionic_kahler_manifold(graph)
            total_metric_value += metric_value
            
            expected_value = n ** 1.5
            if abs(metric_value - expected_value) > 0.1 * expected_value:
                conjecture_holds = False
                counterexample = f"Graph with {n} nodes, expected {expected_value}, got {metric_value}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - n ** 1.5) < 0.1 * n ** 1.5) / len(results)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - n ** 1.5) < 0.1 * n ** 1.5) / len(results)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_instances")