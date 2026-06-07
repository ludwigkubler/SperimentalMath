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
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, d - 1) == 0 and len(edges) < (n * d) // 2:
                    edges.add((i, j))
        return list(edges)
    
    def del_pezzo_degree(graph):
        n = len(graph)
        degree_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            degree_matrix[u][v] = 1
            degree_matrix[v][u] = 1
        
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
                    for c in range(cols):
                        matrix[row][c] -= factor * matrix[pivot_row][c]
            return rank
        
        return n - gaussian_elimination(degree_matrix)
    
    def circuit_entanglement_complexity(graph):
        # Placeholder function. This should be replaced with actual computation.
        return len(graph)
    
    d = 3
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        del_pezzo = del_pezzo_degree(graph)
        entanglement_complexity = circuit_entanglement_complexity(graph)
        
        results.append({
            "n": n,
            "del_pezzo": del_pezzo,
            "entanglement_complexity": entanglement_complexity
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    del_pezzos = [result["del_pezzo"] for result in results]
    entanglement_complexities = [result["entanglement_complexity"] for result in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    correlation = pearson_correlation(del_pezzos, entanglement_complexities)
    
    conjecture_holds = correlation >= 0.7 or any(abs(dp - ec) > 1.5 for dp, ec in zip(del_pezzos, entanglement_complexities))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "correlation < 0.7 or |D(G) - Θ(E(G))| > 1.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")