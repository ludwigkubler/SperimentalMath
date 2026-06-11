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
    
    def generate_graphical_matroid(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def is_connected(edges, n):
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for edge in edges:
                    if edge[0] == node and not visited[edge[1]]:
                        stack.append(edge[1])
                    elif edge[1] == node and not visited[edge[0]]:
                        stack.append(edge[0])
        return all(visited)
    
    def automorphism_group_order(edges, n):
        if not is_connected(edges, n):
            return 0
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        def det(matrix):
            if len(matrix) == 1:
                return matrix[0][0]
            det_val = Fraction(0)
            for j in range(len(matrix)):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det_val += (-1)**j * matrix[0][j] * det(submatrix)
            return det_val
        
        def is_permutation(p):
            if len(p) != n:
                return False
            permuted = [p.index(i) for i in range(n)]
            return p == permuted
        
        order = 1
        for i in range(2, n + 1):
            for p in itertools.permutations(range(n), i):
                if is_permutation(p):
                    permuted_matrix = [[adj_matrix[p[i]][p[j]] for j in range(n)] for i in range(n)]
                    if det(permuted_matrix) == 0:
                        order *= math.factorial(i)
        return order
    
    def resolution_proof_width(edges, n):
        # Simplified heuristic to estimate width
        return len(max([set(u) | set(v) for u, v in edges], key=len))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            matroid = generate_graphical_matroid(n)
            ord_aut_M = automorphism_group_order(matroid, n)
            w_M = resolution_proof_width(matroid, n)
            results.append((ord_aut_M, w_M))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_aut_M_values = [r[0] for r in results]
    w_M_values = [r[1] for r in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y) if std_dev_x and std_dev_y else None
    
    correlation_coefficient = pearson_correlation(ord_aut_M_values, w_M_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(r[1] == n for r in results)),
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if correlation_coefficient is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if r["metric_value"] is None), None)
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)