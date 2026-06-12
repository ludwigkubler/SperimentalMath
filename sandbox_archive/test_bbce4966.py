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
    
    def is_planar(n, edges):
        if n <= 3:
            return True
        if len(edges) > 3 * (n - 2):
            return False
        for u in range(n):
            neighbors = [v for v in range(n) if (u, v) in edges or (v, u) in edges]
            if len(neighbors) >= 5:
                return False
        return True

    def geometric_entropy(G):
        n = len(G)
        total_edges = sum(len(v) for v in G.values())
        entropy = 0.0
        for v in range(n):
            degree = len(G[v])
            if degree > 1:
                entropy += math.log(degree, 2)
        return entropy / total_edges

    def communication_complexity_rank(G):
        n = len(G)
        rank = 0
        for u in range(n):
            neighbors = [v for v in range(n) if (u, v) in G or (v, u) in G]
            rank = max(rank, len(neighbors))
        return rank

    def generate_random_planar_graph(n):
        edges = set()
        while True:
            G = {i: [] for i in range(n)}
            for _ in range(3 * (n - 2)):
                u, v = random.sample(range(n), 2)
                if u != v and (u, v) not in edges and (v, u) not in edges:
                    G[u].append(v)
                    G[v].append(u)
                    edges.add((u, v))
            if is_planar(n, edges):
                return G

    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            G = generate_random_planar_graph(n)
            h_G = geometric_entropy(G)
            r_G = communication_complexity_rank(G)
            metric_values.append((h_G, r_G))
            instances_tested += 1
            n_max = max(n_max, n)

    if len(metric_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)

    h_values, r_values = zip(*metric_values)
    correlation_coefficient = pearson_correlation(h_values, r_values)

    if correlation_coefficient < 0.8:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"

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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"] != "")
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")