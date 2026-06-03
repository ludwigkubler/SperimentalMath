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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < n - 1 or d > n - 1:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                edges_added.add((v, u))
        return graph

    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = set(graph[i])
            rank += len(neighbors) + 1
        return rank // 2

    def quantum_group_representation_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            rank += len(graph[i]) + 1
        return rank // 2

    def linear_regression(x, y):
        if len(x) != len(y):
            return None
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept

    def mean_absolute_difference(x, y):
        if len(x) != len(y):
            return None
        return sum(abs(xi - yi) for xi, yi in zip(x, y)) / len(x)

    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = min(n - 1, max(1, int((n * (n - 1)) / (2 * n))))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        w_G = communication_complexity_rank(graph)
        Rank_R_G = quantum_group_representation_rank(graph)
        results.append((w_G, Rank_R_G))

    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    x, y = zip(*results)
    slope, intercept = linear_regression(x, y)
    if slope is None:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(graph) for _, graph in results),
            "conjecture_holds": False,
            "counterexample": "linear_regression_failed"
        }

    mean_absolute_diff = mean_absolute_difference(x, y)
    if mean_absolute_diff is None:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(graph) for _, graph in results),
            "conjecture_holds": False,
            "counterexample": "mean_absolute_difference_failed"
        }

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": slope,
        "instances_tested": len(results),
        "n_max": max(len(graph) for _, graph in results),
        "conjecture_holds": abs(slope - 1) <= 0.2 and mean_absolute_diff <= 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results))) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds_or_counterexamples_found")