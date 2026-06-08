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
        if (n * d) % 2 != 0 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph

    def compute_G1(G):
        n = len(G)
        if n == 0:
            return 0
        G1 = 0
        for i in range(n):
            degree = len(G[i])
            G1 += (degree * (degree - 1)) // 2
        return G1

    def resolution_width(G):
        n = len(G)
        if n == 0:
            return 0
        width = 0
        for i in range(n):
            neighbors = set(G[i])
            while neighbors:
                new_neighbors = set()
                for j in neighbors:
                    new_neighbors.update(set(G[j]) - {i})
                neighbors = new_neighbors
                width += 1
        return width

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        G = generate_d_regular_graph(n, 2)
        if G is None:
            continue
        G1 = compute_G1(G)
        w = resolution_width(G)
        results.append({
            "metric_name": "G^1(φ_G)",
            "metric_value": G1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })

    if not results:
        return {
            "metric_name": "G^1(φ_G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    G1_values = [r["metric_value"] for r in results]
    widths = [r["n_max"] for r in results]

    if len(G1_values) < 30:
        return {
            "metric_name": "G^1(φ_G)",
            "metric_value": None,
            "instances_tested": len(G1_values),
            "n_max": max(widths),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept

    slope, _ = linear_regression(widths, G1_values)
    if slope <= 0:
        return {
            "metric_name": "G^1(φ_G)",
            "metric_value": None,
            "instances_tested": len(G1_values),
            "n_max": max(widths),
            "conjecture_holds": False,
            "counterexample": "non_positive_slope"
        }

    return {
        "metric_name": "G^1(φ_G)",
        "metric_value": slope,
        "instances_tested": len(G1_values),
        "n_max": max(widths),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    elif all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope_not_positive\" first_failing_seed={first_failing_seed}")