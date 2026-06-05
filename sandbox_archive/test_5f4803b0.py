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
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < n * d // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def hodge_rank(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                A[u][v] += 1
        rank = gaussian_elimination(A, n)
        return rank
    
    def gaussian_elimination(matrix, n):
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return n
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def circuit_entanglement(graph):
        n = len(graph)
        if n < 2:
            return 0
        entanglement = 0
        for u in range(n):
            for v in graph[u]:
                if u < v:
                    entanglement += 1
        return entanglement
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def mean_absolute_difference(x, y):
        return sum(abs(a - b) for a, b in zip(x, y)) / len(x)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        h_values = []
        e_values = []
        for _ in range(30):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            h_value = hodge_rank(graph)
            e_value = circuit_entanglement(graph)
            h_values.append(h_value)
            e_values.append(e_value)
        if len(h_values) < 30:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": len(h_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_samples"
            }
        corr_coeff = correlation_coefficient(h_values, e_values)
        m_ad = mean_absolute_difference(h_values, e_values)
        results.append((corr_coeff, m_ad))
    
    avg_corr_coeff = sum(c for c, _ in results) / len(results)
    avg_m_ad = sum(m for _, m in results) / len(results)
    support_fraction = sum(1 for c, _ in results if c > 0.8 and m <= 3) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": avg_corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for _, n in [(5, 10, 15, 20, 30, 40)[i] for i in range(len(results))]),
        "conjecture_holds": avg_corr_coeff > 0.8 and avg_m_ad <= 3,
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
    
    avg_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    avg_m_ad = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_corr_coeff} std={avg_m_ad} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient or m_ad did not meet criteria\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")