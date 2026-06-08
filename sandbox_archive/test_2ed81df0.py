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
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(n-1, i-1, -1):
                matrix[i][j] /= matrix[i][i]
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(n-1, i-1, -1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        rref = gaussian_elimination([row[:] for row in matrix])
        if rref is None:
            return 0
        rank = 0
        for row in rref:
            if any(row[j] != 0 for j in range(len(row))):
                rank += 1
        return rank
    
    def communication_complexity_rank_variance(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for u in graph:
            for v in graph[u]:
                A[u][v] = 1
                A[v][u] = 1
        return rank(A) / (n * (n - 1))
    
    def minimal_coherence_length(graph):
        n = len(graph)
        B = [[0] * n for _ in range(n)]
        for u in graph:
            for v in graph[u]:
                B[u][v] = 1
                B[v][u] = 1
        return sum(sum(row) for row in B) / (2 * n)
    
    def linear_regression(x, y):
        if len(x) != len(y):
            return None
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        if denominator == 0:
            return None
        slope = numerator / denominator
        intercept = mean_y - slope * mean_x
        r_squared = (numerator ** 2) / (denominator * sum((y[i] - mean_y) ** 2 for i in range(n)))
        return slope, intercept, r_squared
    
    n_values = [5, 10, 15, 20, 30, 40]
    mcl_values = []
    rho_values = []
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(2, n-1)
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            mcl_values.append(minimal_coherence_length(graph))
            rho_values.append(communication_complexity_rank_variance(graph))
    
    if not mcl_values or not rho_values:
        return {
            "metric_name": "minimal_coherence_length",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    slope, intercept, r_squared = linear_regression(mcl_values, rho_values)
    if slope is None or r_squared < 0.7:
        return {
            "metric_name": "minimal_coherence_length",
            "metric_value": 0,
            "instances_tested": len(mcl_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"r_squared={r_squared}"
        }
    
    return {
        "metric_name": "minimal_coherence_length",
        "metric_value": slope,
        "instances_tested": len(mcl_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_slope = sum(r["metric_value"] for r in results) / len(results)
        std_slope = math.sqrt(sum((r["metric_value"] - mean_slope) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_squared too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")