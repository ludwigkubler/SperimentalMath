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
        edges = set()
        while len(edges) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u > v:
                u, v = v, u
            if (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def hodge_cohomology_dimension(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    A[i][j] = A[j][i] = 1
        return gaussian_elimination(A)
    
    def circuit_monotone_width(graph):
        n = len(graph)
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    path = [i]
                    visited = set()
                    while path:
                        current = path[-1]
                        found = False
                        for k in range(n):
                            if k not in visited and graph[current][k]:
                                path.append(k)
                                visited.add(k)
                                found = True
                                break
                        if not found:
                            width += 1
                            path.pop()
        return width
    
    def run_test(n, d):
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            return {"metric_name": "Hodge Cohomology Dimension", "metric_value": None, "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "Graph generation failed"}
        h = hodge_cohomology_dimension(graph)
        w = circuit_monotone_width(graph)
        if h is None:
            return {"metric_name": "Hodge Cohomology Dimension", "metric_value": None, "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "Gaussian elimination failed"}
        return {"metric_name": "Hodge Cohomology Dimension", "metric_value": h / w if w != 0 else float('inf'), "instances_tested": 1, "n_max": n, "conjecture_holds": True, "counterexample": ""}
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        d = random.randint(2, min(n - 1, 8))
        result = run_test(n, d)
        if result["metric_value"] is None:
            return {"metric_name": "Hodge Cohomology Dimension", "metric_value": None, "instances_tested": 30, "n_max": n, "conjecture_holds": False, "counterexample": "Test failed for some n"}
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    instances_tested = sum(r["instances_tested"] for r in results)
    n_max = max(r["n_max"] for r in results)
    conjecture_holds = all(0.7 <= v <= 1.3 for v in metric_values) and len(metric_values) >= 24
    counterexample = "" if conjecture_holds else "Hodge Cohomology Dimension not within expected range"
    
    return {"metric_name": "Hodge Cohomology Dimension", "metric_value": sum(metric_values) / instances_tested if instances_tested > 0 else None, "instances_tested": instances_tested, "n_max": n_max, "conjecture_holds": conjecture_holds, "counterexample": counterexample}

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'n_max': {result['n_max']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / instances_tested} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=All trials used n=1")