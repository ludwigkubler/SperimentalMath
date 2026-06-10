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
        if (d * n) % 2 != 0 or d >= n:
            return None
        adj = [set() for _ in range(n)]
        edges_added = set()
        for i in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                adj[u].add(v)
                adj[v].add(u)
                edges_added.add((u, v))
                break
        return adj

    def hodge_de_rham_cohomology_dimension(adj):
        n = len(adj)
        if n == 0:
            return 0
        max_dim = 0
        for i in range(n):
            visited = [False] * n
            stack = [i]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for v in adj[u]:
                        if not visited[v]:
                            stack.append(v)
            max_dim = max(max_dim, sum(1 for x in visited if x))
        return max_dim

    def circuit_satisfiability_complexity(adj):
        n = len(adj)
        if n == 0:
            return 0
        # Simplified complexity measure based on graph structure
        return len([u for u in range(n) if len(adj[u]) > 1])

    instances_tested = 0
    h_dim_values = []
    c_phi_G_values = []

    for _ in range(30):
        n = random.randint(5, 40)
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        h_dim = hodge_de_rham_cohomology_dimension(graph)
        c_phi_G = circuit_satisfiability_complexity(graph)
        if h_dim is not None and c_phi_G is not None:
            h_dim_values.append(h_dim)
            c_phi_G_values.append(c_phi_G)
            instances_tested += 1

    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, n),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    h_dim_mean = sum(h_dim_values) / len(h_dim_values)
    c_phi_G_mean = sum(c_phi_G_values) / len(c_phi_G_values)

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)

    correlation_coefficient = pearson_correlation(h_dim_values, c_phi_G_values)

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(5, n),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.7 else f"correlation={correlation_coefficient:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results):.2f} std={math.sqrt(sum((r['metric_value'] - sum(r['metric_value'] for r in results) / len(results)) ** 2 for r in results) / len(results)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")