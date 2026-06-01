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

def generate_planar_graph(n):
    if n < 3:
        return []
    vertices = list(range(n))
    edges = set()
    while len(edges) < n - 1:
        u, v = random.sample(vertices, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            for w in vertices:
                if (w, u) in edges or (w, v) in edges:
                    continue
                if len(edges - {(u, v), (v, u)}) == n - 2 and is_planar(vertices, edges):
                    return list(edges)
    return []

def is_planar(V, E):
    if len(E) > 3 * len(V) - 6:
        return False
    for u, v in combinations(V, 3):
        neighbors = [w for w in V if (u, w) in E or (v, w) in E]
        if len(neighbors) >= 5 and any((neighbors[i], neighbors[j]) in E for i in range(len(neighbors)) for j in range(i + 1, len(neighbors))):
            return False
    return True

def compute_hyperbolic_volume(G):
    n = len(G)
    if n < 3:
        return 0
    volume = 0
    for u, v in G:
        neighbors_u = [w for w in range(n) if (u, w) in G or (w, u) in G]
        neighbors_v = [w for w in range(n) if (v, w) in G or (w, v) in G]
        common_neighbors = set(neighbors_u).intersection(neighbors_v)
        volume += len(common_neighbors) / (len(neighbors_u) * len(neighbors_v))
    return volume

def compute_communication_complexity(G):
    n = len(G)
    if n < 3:
        return 0
    complexity = 0
    for u, v in G:
        neighbors_u = [w for w in range(n) if (u, w) in G or (w, u) in G]
        neighbors_v = [w for w in range(n) if (v, w) in G or (w, v) in G]
        common_neighbors = set(neighbors_u).intersection(neighbors_v)
        complexity += len(common_neighbors)
    return complexity

def compute_correlation(x, y):
    n = len(x)
    if n < 2:
        return 0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
    if denominator == 0:
        return 0
    return numerator / denominator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_planar_graph(n)
        if not G:
            continue
        mvol_G = compute_hyperbolic_volume(G)
        ccom_G = compute_communication_complexity(G)
        results.append((mvol_G, ccom_G))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    mvol_G, ccom_G = zip(*results)
    correlation_coefficient = compute_correlation(mvol_G, ccom_G)
    mean_absolute_difference = sum(abs(a - b) for a, b in zip(mvol_G, ccom_G)) / len(mvol_G)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_absolute_difference <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_absolute_difference <= 3 else f"Pearson Correlation Coefficient < 0.8 or Mean Absolute Difference > 3"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        print(f"RESULT: FALSIFIED counterexample=\"Pearson Correlation Coefficient < 0.8 or Mean Absolute Difference > 3\" first_failing_seed={first_failing_seed}")