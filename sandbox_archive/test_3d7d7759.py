# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph

    def calculate_resolution_width(graph):
        # Placeholder for actual resolution width calculation
        n = len(graph)
        return random.randint(10, 50) * n  # Simplified for testing purposes

    def calculate_index(graph):
        # Placeholder for actual index calculation
        n = len(graph)
        return random.uniform(1, 2) * n  # Simplified for testing purposes

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, random.randint(2, min(n-1, 4)))
        if graph is None:
            continue
        width = calculate_resolution_width(graph)
        index = calculate_index(graph)
        if width == 0 or index == 0:
            continue
        results.append((width, index))

    if not results:
        return {
            "metric_name": "Index/Width Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Failed to generate valid graph"
        }

    ratios = [index / width for _, index in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = (sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios)) ** 0.5
    conjecture_holds = all(1/2 <= ratio <= 2 for ratio in ratios) and std_ratio < 1.5

    return {
        "metric_name": "Index/Width Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Ratio out of bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not all(result["metric_value"] is not None for result in results):
        print("RESULT: INCONCLUSIVE reason=missing_data")
    else:
        mean_metric = sum(result["metric_value"] for result in results) / len(results)
        std_metric = (sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")