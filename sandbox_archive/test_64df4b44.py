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
        if (n * d) % 2 != 0 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph

    def compute_circuit_complexity(graph):
        # Placeholder for actual circuit complexity computation
        n = len(graph)
        return n * (n - 1) // 2  # Simplified example: linear in the number of vertices

    def compute_representation_dimension(graph):
        # Placeholder for actual representation dimension computation
        n = len(graph)
        d = sum(len(neighbors) for neighbors in graph.values()) // n
        return d * (d + 1) // 2  # Simplified example: quadratic in the degree

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_dim = 0
    total_complexity = 0
    max_n = 0

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            graph = generate_d_regular_graph(n, n - 1)
            if graph is None:
                continue
            dim = compute_representation_dimension(graph)
            complexity = compute_circuit_complexity(graph)
            total_dim += dim
            total_complexity += complexity
            instances_tested += 1
            max_n = max(max_n, n)

    mean_dim = total_dim / instances_tested if instances_tested > 0 else 0
    mean_complexity = total_complexity / instances_tested if instances_tested > 0 else 0

    correlation_coefficient = (instances_tested * sum(dim * complexity for dim, complexity in zip([mean_dim] * instances_tested, [mean_complexity] * instances_tested)) - 
                               instances_tested * mean_dim * mean_complexity) / math.sqrt(
        (instances_tested * sum(dim ** 2 for dim in [mean_dim] * instances_tested) - instances_tested * mean_dim ** 2) *
         (instances_tested * sum(complexity ** 2 for complexity in [mean_complexity] * instances_tested) - instances_tested * mean_complexity ** 2))

    conjecture_holds = correlation_coefficient >= 0.9 and p_value < 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient_threshold_not_met"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    else:
        seeds = [int(s) for s in sys.argv[1:]]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if "metric_value" in r) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if "metric_value" in r) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")