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
    
    def generate_random_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph
    
    def calculate_minimal_order(graph):
        n = len(graph)
        if n == 0:
            return 0
        order = 1
        while True:
            found_new_node = False
            for u in range(n):
                if len(graph[u]) < order:
                    continue
                neighbors = set(graph[u])
                for v in range(u + 1, n):
                    if len(graph[v]) >= order and all(v not in graph[w] for w in neighbors):
                        graph[v].append(u)
                        found_new_node = True
            if not found_new_node:
                break
            order += 1
        return order
    
    def is_d_regular_graph(graph, d):
        n = len(graph)
        for u in range(n):
            if len(graph[u]) != d:
                return False
        return True
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_random_d_regular_graph(n, 2)
        if not is_d_regular_graph(graph, 2):
            continue
        order = calculate_minimal_order(graph)
        results.append((n, order))
    
    if len(results) < 30:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results) if results else 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_order = sum(order for _, order in results) / len(results)
    std_order = math.sqrt(sum((order - mean_order) ** 2 for _, order in results) / len(results))
    support_fraction = sum(1 for _, order in results if abs(order - n ** 1.5) <= 0.1 * n ** 1.5) / len(results)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            break
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_order = sum(result["metric_value"] for result in results) / len(results)
        std_order = math.sqrt(sum((result["metric_value"] - mean_order) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=seeds[0]) if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")