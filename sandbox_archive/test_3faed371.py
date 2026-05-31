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
from math import log2, ceil

def generate_d_regular_graph(n, d):
    if 2 * d > n or d == 0:
        return None
    graph = [[] for _ in range(n)]
    for i in range(n):
        neighbors = random.sample(range(i+1, min(n, i+d+1)), d-1)
        for neighbor in neighbors:
            graph[i].append(neighbor)
            graph[neighbor].append(i)
    return graph

def compute_entropy(graph):
    n = len(graph)
    degree_sum = sum(len(neighbors) for neighbors in graph)
    if degree_sum == 0:
        return 0
    avg_degree = degree_sum / n
    entropy = -avg_degree * log2(avg_degree) - (n-avg_degree) * log2(n-avg_degree)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        R_G = len(graph)  # Simplified for this example
        h_G = compute_entropy(graph)
        results.append((R_G, h_G))
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    R_G_values, h_G_values = zip(*results)
    correlation_coefficient = sum((R_G - mean(R_G_values)) * (h_G - mean(h_G_values)) for R_G, h_G in results) / (len(results) * std(R_G_values) * std(h_G_values))
    max_R_G = max(R_G_values)
    conjecture_holds = correlation_coefficient >= 0.7 and max_R_G <= 4 * max(h_G_values)
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max(R(G))={max_R_G} > 4*max(h(G))"
    }

def mean(values):
    return sum(values) / len(values)

def std(values):
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return variance ** 0.5

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = std([r["metric_value"] for r in results])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")