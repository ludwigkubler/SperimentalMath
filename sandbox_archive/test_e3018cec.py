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
        adj_list = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(adj_list[i]) < d and len(adj_list[j]) < d and (i, j) not in edges_added:
                    adj_list[i].append(j)
                    adj_list[j].append(i)
                    edges_added.add((i, j))
        return adj_list
    
    def hodge_de_rham_cohomology_dimension(graph):
        n = len(graph)
        if n == 0:
            return 0
        max_degree = max(len(neighbors) for neighbors in graph)
        return max_degree + 1
    
    def circuit_satisfiability_complexity(graph):
        n = len(graph)
        if n == 0:
            return 0
        # Simplified complexity measure based on number of edges and vertices
        return (n * (n - 1)) // 2
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_dim_values = []
    c_phi_G_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)  # Example: d=2
        if graph is None:
            continue
        h_dim = hodge_de_rham_cohomology_dimension(graph)
        c_phi_G = circuit_satisfiability_complexity(graph)
        h_dim_values.append(h_dim)
        c_phi_G_values.append(c_phi_G)
    
    if len(h_dim_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(h_dim_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation_coefficient = pearson_correlation_coefficient(h_dim_values, c_phi_G_values)
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(h_dim_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_above_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")