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
        if (n * d) % 2 != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    graph[i].add(j)
                    graph[j].add(i)
                    edges.append((i, j))
        return graph, edges

    def frege_proof_width(edges):
        width = 0
        for u, v in edges:
            if u > v:
                u, v = v, u
            width = max(width, u + 1)
        return width

    def p_adic_valuation_rank(graph):
        n = len(graph)
        valrank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if j not in graph[i]:
                    continue
                count = 0
                while j % 2 == 0:
                    j //= 2
                    count += 1
                valrank = max(valrank, count)
        return valrank

    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)

    def mean_difference(x, y):
        n = len(x)
        return sum(abs(x[i] - y[i]) for i in range(n)) / n

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n <= 1:
            continue
        graph, edges = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        valrank = p_adic_valuation_rank(graph)
        width = frege_proof_width(edges)
        results.append((valrank, width))

    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    valranks, widths = zip(*results)
    corr_coeff = correlation_coefficient(valranks, widths)
    mean_diff = mean_difference(valranks, widths)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == len(graph) for graph, _ in results)),
        "conjecture_holds": abs(corr_coeff) >= 0.8 and mean_diff <= 3,
        "counterexample": "" if abs(corr_coeff) >= 0.8 and mean_diff <= 3 else "correlation_threshold_not_met"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        std_corr_coeff = math.sqrt(sum((result["metric_value"] - mean_corr_coeff) ** 2 for result in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")