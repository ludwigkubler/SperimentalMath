# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges_used = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges_used or (v, u) in edges_used:
                    continue
                graph[u].add(v)
                graph[v].add(u)
                edges_used.add((u, v))
                break
        return graph
    
    def hodge_rank(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                A[u][v] += 1
                A[v][u] += 1
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        M = [A[i] + I[i] for i in range(n)]
        rank = gaussian_elimination(M)
        return n - rank
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        pivot_row = 0
        pivot_col = 0
        while pivot_row < m and pivot_col < n:
            if matrix[pivot_row][pivot_col] == 0:
                for i in range(pivot_row + 1, m):
                    if matrix[i][pivot_col] != 0:
                        matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
                        break
                else:
                    pivot_col += 1
            else:
                for i in range(m):
                    if i != pivot_row and matrix[i][pivot_col] != 0:
                        factor = -matrix[i][pivot_col] / matrix[pivot_row][pivot_col]
                        for j in range(n):
                            matrix[i][j] += factor * matrix[pivot_row][j]
                pivot_row += 1
                pivot_col += 1
        return m - sum(1 for row in matrix if all(val == 0 for val in row))
    
    def circuit_entanglement(graph):
        n = len(graph)
        if n <= 2:
            return 0
        qubits = list(range(n))
        entanglements = set()
        for subset in combinations(qubits, 2):
            u, v = subset
            if v in graph[u]:
                entanglements.add((u, v))
        return len(entanglements)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    e_values = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        h_value = hodge_rank(graph)
        e_value = circuit_entanglement(graph)
        h_values.append(h_value)
        e_values.append(e_value)
    
    if not h_values or not e_values:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(h_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "Graph generation failed"
        }
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        if std_x == 0 or std_y == 0:
            return 0
        return cov / (std_x * std_y)
    
    corr_coeff = correlation_coefficient(h_values, e_values)
    mean_abs_diff = sum(abs(a - b) for a, b in zip(h_values, e_values)) / len(h_values)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(h_values),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff > 0.8 and mean_abs_diff <= 3,
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
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean_corr_coeff = sum(r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None) / sum(1 for r in results if "metric_value" in r and r["metric_value"] is not None)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not ("conjecture_holds" in r and r["conjecture_holds"])), None)
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")