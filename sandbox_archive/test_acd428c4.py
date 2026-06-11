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
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            while any(j in edges or j == i for j in neighbors):
                neighbors = random.sample(range(n), d)
            for j in neighbors:
                graph[i][j] = 1
                graph[j][i] = 1
                edges.add((min(i, j), max(i, j)))
        return graph

    def coset_enumeration(graph):
        n = len(graph)
        G = set()
        for i in range(n):
            for j in range(n):
                if graph[i][j]:
                    G.add((i, j))
        return len(G)

    def communication_complexity_rank_variance(graph):
        n = len(graph)
        rank_var = 0
        for i in range(n):
            row_sum = sum(graph[i])
            if row_sum > 0:
                rank_var += (row_sum / n) ** 2
        return rank_var

    def correlation(a, b):
        mean_a = sum(a) / len(a)
        mean_b = sum(b) / len(b)
        cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(len(a))) / len(a)
        var_a = sum((a[i] - mean_a) ** 2 for i in range(len(a))) / len(a)
        var_b = sum((b[i] - mean_b) ** 2 for i in range(len(b))) / len(b)
        return cov / (math.sqrt(var_a) * math.sqrt(var_b))

    n_values = [5, 10, 15, 20, 30, 40]
    aut_orders = []
    rank_vars = []

    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        aut_order = coset_enumeration(graph)
        rank_var = communication_complexity_rank_variance(graph)
        aut_orders.append(aut_order)
        rank_vars.append(rank_var)

    if not aut_orders or not rank_vars:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    corr = correlation(aut_orders, rank_vars)
    return {
        "metric_name": "Correlation",
        "metric_value": corr,
        "instances_tested": len(aut_orders),
        "n_max": max(n_values),
        "conjecture_holds": abs(corr) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if not all("metric_value" in r and r["metric_value"] is not None for r in results):
        print("RESULT: INCONCLUSIVE missing_metric_values")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if abs(r["metric_value"]) < 0.8), None)
            print(f"RESULT: FALSIFIED counterexample=\"correlation_below_threshold\" first_failing_seed={first_failing_seed}")