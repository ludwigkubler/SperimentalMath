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
        graph = [[] for _ in range(n)]
        edges_added = 0
        while edges_added < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v]:
                graph[u].append(v)
                graph[v].append(u)
                edges_added += 1
        return graph
    
    def compute_minimal_hodge_diamond_width(graph):
        n = len(graph)
        hodge_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        hodge_matrix[0][0] = 1
        for j in range(1, n + 1):
            for i in range(j + 1):
                if i == 0:
                    hodge_matrix[j][i] = sum(hodge_matrix[j - k][i] for k in range(1, j + 1))
                else:
                    hodge_matrix[j][i] = sum(hodge_matrix[j - k][i - 1] for k in range(j + 1))
        return max(max(row) for row in hodge_matrix)
    
    def compute_circuit_monotone_width(graph):
        n = len(graph)
        if n == 0:
            return 0
        depth = [0] * n
        stack = [(0, -1)]
        while stack:
            node, parent = stack.pop()
            for neighbor in graph[node]:
                if neighbor != parent and depth[neighbor] < depth[node] + 1:
                    depth[neighbor] = depth[node] + 1
                    stack.append((neighbor, node))
        return max(depth)
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_max = 40
    instances_tested = 0
    hdw_values = []
    s_values = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        d = random.randint(2, min(n - 1, 3))
        graph = generate_d_regular_graph(n, d)
        if len(graph) != n or any(len(neighbors) != d for neighbors in graph):
            continue
        instances_tested += 1
        hdw = compute_minimal_hodge_diamond_width(graph)
        s = compute_circuit_monotone_width(graph)
        hdw_values.append(hdw)
        s_values.append(s)
    
    if instances_tested == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Invalid d-regular graph generated"
        }
    
    pearson_corr = pearson_correlation_coefficient(hdw_values, s_values)
    mean_abs_diff = sum(abs(a - b) for a, b in zip(hdw_values, s_values)) / instances_tested
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.8 and mean_abs_diff <= 3,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")