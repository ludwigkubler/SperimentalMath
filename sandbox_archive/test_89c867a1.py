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
    
    def generate_d_regular_graph(d, n):
        if d * n % 2 != 0:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        degrees = [d] * n
        for i in range(n):
            available = [j for j in range(n) if j != i and degrees[j] > 0]
            if len(available) < d:
                return None
            neighbors = random.sample(available, d)
            for neighbor in neighbors:
                adj_matrix[i][neighbor] = 1
                adj_matrix[neighbor][i] = 1
                degrees[neighbor] -= 1
        return adj_matrix
    
    def compute_minimal_order(adj_matrix):
        n = len(adj_matrix)
        if n == 0:
            return None
        order = 1
        while True:
            found = False
            for i in range(n):
                for j in range(i + 1, n):
                    if adj_matrix[i][j] == 1 and all(adj_matrix[k][i] != adj_matrix[k][j] for k in range(n) if k != i and k != j):
                        found = True
                        break
                if found:
                    break
            if not found:
                return order
            order += 1
    
    def compute_circuit_depth(adj_matrix):
        n = len(adj_matrix)
        if n == 0:
            return None
        depth = 0
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1:
                    depth += 1
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(2, min(n - 1, 4))
            graph = generate_d_regular_graph(d, n)
            if graph is None:
                continue
            minimal_order = compute_minimal_order(graph)
            circuit_depth = compute_circuit_depth(graph)
            if minimal_order is not None and circuit_depth is not None:
                results.append((minimal_order, circuit_depth))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y):
            return None
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    x, y = zip(*results)
    correlation = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation is not None and abs(correlation) >= 0.8,
        "counterexample": "" if correlation is not None and abs(correlation) >= 0.8 else "low_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] == "low_correlation" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] == "low_correlation")
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")