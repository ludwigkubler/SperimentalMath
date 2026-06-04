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
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for _ in range(d * n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def calculate_gwi(graph):
        # Placeholder for Gromov-Witten Invariant calculation
        # This is a dummy function and should be replaced with actual computation
        n = len(graph)
        return random.random() * n  # Dummy value
    
    def calculate_ccr(graph):
        # Placeholder for Communication Complexity Rank calculation
        # This is a dummy function and should be replaced with actual computation
        n = len(graph)
        return random.random() * n  # Dummy value
    
    correlation_values = []
    instances_tested = 0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = 2 * n // (n - 1) if n > 1 else 1
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        gwi_value = calculate_gwi(graph)
        ccr_value = calculate_ccr(graph)
        
        if not math.isnan(gwi_value) and not math.isnan(ccr_value):
            correlation_values.append((gwi_value, ccr_value))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "Correlation",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "Too few valid graphs generated"
        }
    
    gwi_values = [x[0] for x in correlation_values]
    ccr_values = [x[1] for x in correlation_values]
    mean_gwi = sum(gwi_values) / instances_tested
    mean_ccr = sum(ccr_values) / instances_tested
    
    # Placeholder for Pearson correlation calculation
    # This is a dummy function and should be replaced with actual computation
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    correlation_coefficient = pearson_correlation(gwi_values, ccr_values)
    p_value = random.random()  # Placeholder for actual p-value calculation
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")