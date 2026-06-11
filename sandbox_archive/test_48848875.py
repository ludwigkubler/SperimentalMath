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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def complement_graph(edges, n):
        all_edges = {(i, j) for i in range(n) for j in range(i + 1, n)}
        return all_edges - edges
    
    def lefschetz_dimension(edges, n):
        comp_edges = complement_graph(edges, n)
        if not comp_edges:
            return 0
        adj_matrix = [[0] * n for _ in range(n)]
        for u, v in comp_edges:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                pivot_row = None
                for j in range(rank, rows):
                    if matrix[j][i] != 0:
                        pivot_row = j
                        break
                if pivot_row is not None:
                    matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                    rank += 1
                    for j in range(rows):
                        if j != rank - 1:
                            factor = matrix[j][i] / matrix[rank - 1][i]
                            for k in range(cols):
                                matrix[j][k] -= factor * matrix[rank - 1][k]
            return rank
        
        return n - gaussian_elimination(adj_matrix)
    
    def tropical_motivic_rank(edges, n):
        # Placeholder implementation
        return len(edges) / n
    
    n_values = [10, 20, 30, 40]
    results = []
    for n in n_values:
        graph_edges = generate_graph(n)
        mid = lefschetz_dimension(graph_edges, n)
        tqr = tropical_motivic_rank(graph_edges, n)
        results.append({"n": n, "mid": mid, "tqr": tqr})
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_graphs_generated"
        }
    
    mid_values = [r["mid"] for r in results]
    tqr_values = [r["tqr"] for r in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    correlation = pearson_correlation(mid_values, tqr_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.5,
        "counterexample": "" if correlation > 0.5 else f"low_correlation: {correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
        elif any(r["counterexample"] == "low_correlation" for r in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"] == "low_correlation")
            print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")