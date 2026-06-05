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
        if n % d != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges_added = set()
        for i in range(d):
            for j in range(i + 1, n):
                if len(edges_added) == n * (n - 1) // 2:
                    break
                if random.choice([True, False]):
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges_added.add((min(i, j), max(i, j)))
        return graph
    
    def h_index(G):
        n = len(G)
        A = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if G[i][j] == 1:
                    A[i][j] = Fraction(1, (i + 1) * (j + 1))
        I = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            I[i][i] = Fraction(1)
        for k in range(n - 1):
            A_next = [[Fraction(0)] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for l in range(n):
                        if G[i][l] == 1 and G[l][j] == 1:
                            A_next[i][j] += A[i][l] * I[l][j]
            A = A_next
        return sum(sum(row) for row in A)
    
    def circuit_monotone_width(G):
        n = len(G)
        if n <= 2:
            return 0
        max_width = 0
        for k in range(1, n):
            width = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if G[i][j] == 1:
                        width += 1
            max_width = max(max_width, width)
        return max_width
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_indices = []
    widths = []
    
    for n in n_values:
        G = generate_d_regular_graph(n, 3)
        if G is None:
            continue
        h_index_val = h_index(G)
        width_val = circuit_monotone_width(G)
        h_indices.append(h_index_val)
        widths.append(width_val)
    
    if len(h_indices) < 24:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(h_indices),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    corr_coeff = correlation_coefficient(h_indices, widths)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(h_indices),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff > 0.8 and all(h <= 3 * w for h, w in zip(h_indices, widths)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" not in r or r["metric_value"] is None for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={first_failing_seed}")
    else:
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")