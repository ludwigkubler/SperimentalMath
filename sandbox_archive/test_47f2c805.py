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
        graph = [[] for _ in range(n)]
        edges_used = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    edge = (i, j)
                    reverse_edge = (j, i)
                    if edge not in edges_used and reverse_edge not in edges_used:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges_used.add(edge)
        return graph

    def euler_characteristic(graph):
        n = len(graph)
        m = sum(len(neighbors) for neighbors in graph) // 2
        v = n
        return v - e + f
    
    def resolution_width(graph):
        # Simplified Tseitin formula and resolution width calculation
        # This is a placeholder and should be replaced with actual implementation
        return len(graph)
    
    correlation_values = []
    instances_tested = 0
    n_max = 0
    
    for d in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            n = random.randint(d + 1, min(n_max + 10, 40))
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            instances_tested += 1
            n_max = max(n_max, n)
            chi = euler_characteristic(graph)
            w = resolution_width(graph)
            correlation_values.append((chi, w))
    
    if not correlation_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    def correlation(x, y):
        mean_x = sum(xi for xi, _ in x) / len(x)
        mean_y = sum(yi for _, yi in y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in x) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi, _ in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for _, yi in y) / len(y))
        return cov / (std_x * std_y)
    
    correlation_coefficient = correlation(correlation_values, correlation_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")