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
        graph = [[0] * n for _ in range(n)]
        edges = []
        for i in range(n):
            neighbors = random.sample(range(n), d)
            while any(graph[i][j] for j in neighbors):
                neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i < j:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges.append((i, j))
        return graph
    
    def compute_automorphic_representation(graph):
        n = len(graph)
        # Simplified representation using degrees and adjacency matrix
        degrees = [sum(row) for row in graph]
        automorphic_rep = {tuple(degrees): sum(sum(row[i] * row[j] for j in range(n)) for i in range(n))}
        return automorphic_rep
    
    def compute_minimal_index(automorphic_rep):
        # Simplified minimal index calculation
        return len(automorphic_rep)
    
    def compute_circuit_monotone_width(graph):
        n = len(graph)
        width = 0
        for row in graph:
            width += max(row.count(1), (n - sum(row)).count(1))
        return width
    
    def pearson_correlation(x, y):
        if not x or not y or len(x) != len(y):
            return None
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n == 1:
            continue
        for _ in range(5):
            graph = generate_d_regular_graph(n, n - 1)
            if not graph:
                continue
            automorphic_rep = compute_automorphic_representation(graph)
            min_index = compute_minimal_index(automorphic_rep)
            circuit_width = compute_circuit_monotone_width(graph)
            results.append((min_index, circuit_width))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x, y = zip(*results)
    correlation_coefficient = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in [(5, 10, 15, 20, 30, 40)])
        if results else 1,
        "conjecture_holds": correlation_coefficient is not None and correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")