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
        if (d * n) % 2 != 0 or d > n - 1:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if i + rank >= n:
                break
            max_row = i + rank
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                continue
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    if j != i and k >= i:
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def resolution_width(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    clauses.append([i + 1, -(j + 1)])
        stack = []
        assignment = [0] * (n + 1)
        def dpll():
            if not clauses:
                return True
            var = next((i for i in range(1, n + 1) if assignment[i] == 0), None)
            if var is None:
                return False
            assignment[var] = 1
            new_clauses = [c for c in clauses if not any(abs(lit) == var for lit in c)]
            if dpll():
                return True
            assignment[var] = -1
            new_clauses.extend([c for c in clauses if not any(abs(lit) == var for lit in c)])
            if dpll():
                return True
            return False
        return 1 + max(dpll() for _ in range(10))
    
    def tropicalized_cohomology_rank(graph):
        n = len(graph)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                if graph[i][j] == 1:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return gaussian_elimination(matrix)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, n - 1)
        if graph is None:
            continue
        rank = tropicalized_cohomology_rank(graph)
        width = resolution_width(graph)
        results.append((rank, width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_sum = sum(r for r, _ in results)
    width_sum = sum(w for _, w in results)
    correlation = (rank_sum * width_sum - len(results) * rank_sum * width_sum / len(results)) / \
                  math.sqrt((sum(r**2 for r, _ in results) - rank_sum**2 / len(results)) *
                            (sum(w**2 for _, w in results) - width_sum**2 / len(results)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation\" first_failing_seed={first_failing_seed}")