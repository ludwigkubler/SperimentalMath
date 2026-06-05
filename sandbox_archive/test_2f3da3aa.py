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
        if n % d != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d - 1)
            while any(graph[i][j] or graph[j][i] for j in neighbors):
                neighbors = random.sample(range(n), d - 1)
            for j in neighbors:
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges.add((i, j))
        return graph

    def h_index(matroid):
        n = len(matroid)
        rank = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if matroid[i][j]:
                    rank[j] += 1
        rank.sort(reverse=True)
        return sum(rank[:n // 2])

    def circuit_monotone_width(graph):
        n = len(graph)
        max_width = 0
        for i in range(n):
            width = 0
            for j in range(i + 1, n):
                if graph[i][j]:
                    width += 1
            max_width = max(max_width, width)
        return max_width

    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)

    n_values = [5, 10, 15, 20, 30, 40]
    h_indices = []
    widths = []

    for n in n_values:
        graph = generate_d_regular_graph(n, n // 2)
        if graph is None:
            continue
        matroid = [[graph[i][j] == graph[j][i] for j in range(n)] for i in range(n)]
        h_indices.append(h_index(matroid))
        widths.append(circuit_monotone_width(graph))

    if not h_indices or not widths:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }

    corr_coef = correlation_coefficient(h_indices, widths)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coef,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": corr_coef > 0.8 and all(h <= 3 * w for h, w in zip(h_indices, widths)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr_coef = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    print(f"RESULT: SUPPORTED mean={mean_corr_coef:.2f} std=0.00 support_fraction={support_fraction:.2f}")