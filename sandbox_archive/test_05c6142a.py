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
        if (d * n) % 2 != 0:
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
    
    def hodge_de_rham_cohomology_dimension(graph):
        n = len(graph)
        if n == 0:
            return 0
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                adjacency_matrix[u][v] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for col in range(cols):
                pivot_row = -1
                for row in range(rank, rows):
                    if matrix[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row == -1:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for row in range(rank, rows):
                    factor = matrix[row][col] / matrix[pivot_row][col]
                    for j in range(cols):
                        matrix[row][j] -= factor * matrix[pivot_row][j]
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    def circuit_satisfiability_complexity(graph):
        n = len(graph)
        if n == 0:
            return 0
        # Simplified complexity measure based on the number of edges and vertices
        return len(graph) * (len(graph[0]) if graph else 0)
    
    instances_tested = 0
    h_dim_sum = 0
    c_phi_G_sum = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Aim for at least 30 instances per seed
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            h_dim = hodge_de_rham_cohomology_dimension(graph)
            c_phi_G = circuit_satisfiability_complexity(graph)
            if h_dim is not None and c_phi_G is not None:
                instances_tested += 1
                h_dim_sum += h_dim
                c_phi_G_sum += c_phi_G
    
    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max([5, 10, 15, 20, 30, 40]),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    h_dim_avg = h_dim_sum / instances_tested
    c_phi_G_avg = c_phi_G_sum / instances_tested
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = math.sqrt(sum((x[i] - x_mean) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - y_mean) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    correlation_coefficient = pearson_correlation_coefficient([h_dim_avg], [c_phi_G_avg])
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")