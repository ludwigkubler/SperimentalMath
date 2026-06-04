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
        if n * d % 2 != 0 or d == 1:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u != v and (u, v) not in edges and (v, u) not in edges:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges.add((u, v))
                    break
        return graph
    
    def compute_gwi(graph):
        n = len(graph)
        if n == 1:
            return 0
        gwi = 0
        for u in range(n):
            for v in range(u + 1, n):
                if v not in graph[u]:
                    continue
                count = 0
                for w in range(v + 1, n):
                    if w not in graph[v] and u != w:
                        count += 1
                gwi += count
        return gwi
    
    def compute_ccr(graph):
        n = len(graph)
        ccr = 0
        for u in range(n):
            for v in range(u + 1, n):
                if v not in graph[u]:
                    continue
                ccr += 1
        return ccr
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_gwi = 0
    total_ccr = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            gwi = compute_gwi(graph)
            ccr = compute_ccr(graph)
            total_gwi += gwi
            total_ccr += ccr
            instances_tested += 1
            max_n = max(max_n, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    gwi_avg = total_gwi / instances_tested
    ccr_avg = total_ccr / instances_tested
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    correlation = pearson_correlation([gwi_avg], [ccr_avg])
    p_value = None  # Not computable without actual data points
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": correlation >= 0.5 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")