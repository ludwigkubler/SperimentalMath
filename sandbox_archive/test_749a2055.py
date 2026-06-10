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
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(i + 1, n), d - len(graph[i]))
            for j in neighbors:
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph

    def calculate_geometric_complexity(graph):
        n = len(graph)
        degree_sum = sum(len(neighbors) for neighbors in graph)
        if degree_sum == 0:
            return 0
        return Fraction(degree_sum, n)

    def calculate_boolean_circuit_size(graph):
        n = len(graph)
        d = max(len(neighbors) for neighbors in graph)
        if d == 0:
            return 0
        return n * (d + 1)

    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(1, min(n - 1, 3))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        geoc = calculate_geometric_complexity(graph)
        s = calculate_boolean_circuit_size(graph)
        results.append((geoc, s))

    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Failed to generate valid d-regular graph"
        }

    geoc_values = [r[0] for r in results]
    s_values = [r[1] for r in results]

    mean_geoc = sum(geoc_values) / len(geoc_values)
    mean_s = sum(s_values) / len(s_values)

    n_max = max(len(graph) for _, _ in results)
    instances_tested = len(results)

    correlation_coefficient = 0
    if len(geoc_values) > 1:
        numerator = sum((x - mean_geoc) * (y - mean_s) for x, y in results)
        denominator = math.sqrt(sum((x - mean_geoc) ** 2 for x in geoc_values)) * math.sqrt(sum((y - mean_s) ** 2 for y in s_values))
        if denominator != 0:
            correlation_coefficient = numerator / denominator

    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "Pearson correlation coefficient < 0.8"

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not results:
        print("RESULT: INCONCLUSIVE No valid trials generated")
        sys.exit(0)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Fewer than 80% seeds support the conjecture")