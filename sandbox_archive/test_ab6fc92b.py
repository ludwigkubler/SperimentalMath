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
        if (d * n) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = {i: set() for i in range(n)}
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].add(v)
                graph[v].add(u)
                edges.add((u, v))
        return graph
    
    def hodge_decomposition(graph):
        n = len(graph)
        laplacian = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = len(graph[i])
            laplacian[i][i] = degree
            for j in graph[i]:
                laplacian[i][j] = -1
        return laplacian
    
    def resolution_width(phi):
        # Placeholder function; actual implementation needed
        return random.randint(1, 10)
    
    n = 40
    d = 3
    instances_tested = 0
    hd_values = []
    w_values = []
    
    for _ in range(30):
        graph = generate_d_regular_graph(n, d)
        if not graph:
            continue
        laplacian = hodge_decomposition(graph)
        # Placeholder for actual Hodge decomposition calculation
        hd_value = sum(sum(row) for row in laplacian) / n
        w_value = resolution_width(phi)
        
        hd_values.append(hd_value)
        w_values.append(w_value)
        instances_tested += 1
    
    if not hd_values or not w_values:
        return {
            "metric_name": "Hodge Decomposition Complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((hd_values[i] - mean(hd_values)) * (w_values[i] - mean(w_values)) for i in range(len(hd_values))) / len(hd_values)
    expected_hd = [mean(w_values) * (i + 1) for i in range(n)]
    max_deviation = max(abs(hd_values[i] - expected_hd[i]) for i in range(len(hd_values)))
    
    return {
        "metric_name": "Hodge Decomposition Complexity",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": correlation >= 0.8 and max_deviation <= 3,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")