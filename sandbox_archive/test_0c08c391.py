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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) == d and len(graph[j]) == d:
                    continue
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for neighbor in graph[i]:
                clause.append(f'-{literals[neighbor]}')
            clauses.append(clause)
        return clauses

    def kostant_multi_index(formula):
        # Placeholder function to simulate the computation of Kostant multi-index
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)

    def resolution_proof_width(formula):
        # Placeholder function to simulate the computation of resolution proof width
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        phi = tseitin_formula(graph)
        kmi_value = kostant_multi_index(phi)
        w_value = resolution_proof_width(phi)
        results.append((kmi_value, w_value))
    
    if len(results) < 100:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if generate_d_regular_graph(n, 3) is not None),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    kmi_values = [r[0] for r in results]
    w_values = [r[1] for r in results]
    mean_kmi = sum(kmi_values) / len(kmi_values)
    mean_w = sum(w_values) / len(w_values)
    covariance = sum((kmi_values[i] - mean_kmi) * (w_values[i] - mean_w) for i in range(len(results))) / len(results)
    variance_kmi = sum((kmi_values[i] - mean_kmi) ** 2 for i in range(len(results))) / len(results)
    variance_w = sum((w_values[i] - mean_w) ** 2 for i in range(len(results))) / len(results)
    correlation_coefficient = covariance / (math.sqrt(variance_kmi) * math.sqrt(variance_w))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if generate_d_regular_graph(n, 3) is not None),
        "conjecture_holds": correlation_coefficient >= 0.8,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_instances")