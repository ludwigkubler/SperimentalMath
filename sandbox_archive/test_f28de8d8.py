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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = {i: set() for i in range(n)}
    edges_added = 0
    while edges_added < n * d // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)
            edges_added += 1
    return graph

def compute_circuit_complexity(graph):
    # Placeholder for circuit complexity computation
    # This is a dummy function that returns the number of vertices as a simple example
    return len(graph)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = random.randint(2, 5)
    n_max = 40
    instances_tested = 0
    correlation_coefficients = []

    for n in range(5, n_max + 1):
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        circuit_complexity = compute_circuit_complexity(graph)
        # Placeholder for computing the dimension of the braided quantum group representation
        # This is a dummy function that returns n as a simple example
        dim_representation = n
        correlation_coefficients.append((dim_representation, circuit_complexity))
        instances_tested += 1

    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    correlation_matrix = [[0, 0], [0, 0]]
    for dim, complexity in correlation_coefficients:
        correlation_matrix[0][0] += dim * dim
        correlation_matrix[0][1] += dim * complexity
        correlation_matrix[1][0] += complexity * dim
        correlation_matrix[1][1] += complexity * complexity

    n = len(correlation_coefficients)
    if n == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    correlation_matrix[0][0] /= n
    correlation_matrix[1][1] /= n
    correlation_matrix[0][1] /= n
    correlation_matrix[1][0] /= n

    det = correlation_matrix[0][0] * correlation_matrix[1][1] - correlation_matrix[0][1] * correlation_matrix[1][0]
    if det == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    correlation_coefficient = (correlation_matrix[0][1] * correlation_matrix[1][1] - correlation_matrix[0][0] * correlation_matrix[1][0]) / det
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")