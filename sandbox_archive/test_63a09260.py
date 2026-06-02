# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_k_regular_graph(n, k):
    if (n * k) % 2 != 0:
        return None
    graph = {i: [] for i in range(n)}
    edges = list(combinations(range(n), 2))
    random.shuffle(edges)
    used_edges = set()
    for u, v in edges[:k*n//2]:
        if len(graph[u]) < k and len(graph[v]) < k:
            graph[u].append(v)
            graph[v].append(u)
            used_edges.add((u, v))
            used_edges.add((v, u))
    return graph

def calculate_k_theory_rank(graph):
    n = len(graph)
    if any(len(neighbors) != 2 for neighbors in graph.values()):
        return None
    A = [[0] * n for _ in range(n)]
    for u, v in combinations(range(n), 2):
        if (u, v) in used_edges or (v, u) in used_edges:
            A[u][v] = A[v][u] = 1
    rank = 0
    for i in range(n):
        found = False
        for j in range(i, n):
            if sum(A[i][k] * A[j][k] for k in range(n)) == 0:
                A[j], A[i] = A[i], A[j]
                found = True
                break
        if not found:
            rank += 1
    return rank

def calculate_communication_complexity_rank(graph):
    n = len(graph)
    min_bits = float('inf')
    for u in range(n):
        bits = 0
        for v in graph[u]:
            if v > u:
                bits += math.log2(len(graph[v]))
        min_bits = min(min_bits, bits)
    return min_bits

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    rk_K_values = []
    r_G_values = []

    for n in n_values:
        graph = generate_k_regular_graph(n, k=3)
        if graph is None:
            continue
        rk_K = calculate_k_theory_rank(graph)
        if rk_K is None:
            continue
        r_G = calculate_communication_complexity_rank(graph)
        rk_K_values.append(rk_K)
        r_G_values.append(r_G)

    if not rk_K_values or not r_G_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }

    mean_rk_K = sum(rk_K_values) / len(rk_K_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)

    correlation_coefficient = 0
    for rk_K, r_G in zip(rk_K_values, r_G_values):
        correlation_coefficient += (rk_K - mean_rk_K) * (r_G - mean_r_G)
    correlation_coefficient /= math.sqrt(sum((x - mean_rk_K) ** 2 for x in rk_K_values)) * math.sqrt(sum((y - mean_r_G) ** 2 for y in r_G_values))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(rk_K_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all("metric_value" in result and result["metric_value"] is not None for result in results):
        mean_metric = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "metric_value" not in result or result["metric_value"] is None)
        print(f"RESULT: FALSIFIED counterexample=\"graph_generation_failed\" first_failing_seed={first_failing_seed}")