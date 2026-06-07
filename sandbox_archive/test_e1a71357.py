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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for col in range(n):
            pivot_row = -1
            for row in range(col, n):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            for row in range(pivot_row + 1, n):
                factor = Fraction(matrix[row][col], matrix[pivot_row][col])
                for c in range(col, n):
                    matrix[row][c] -= factor * matrix[pivot_row][c]
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return n - rank
    
    def del_pezzo_degree(graph):
        n = len(graph)
        degree_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            degree_matrix[u][v] = 1
            degree_matrix[v][u] = 1
        return n - gaussian_elimination(degree_matrix)
    
    def circuit_entanglement_complexity(graph):
        # Placeholder function. Replace with actual implementation.
        return sum(1 for u, v in graph if u != v)
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0:
            raise ValueError("Invalid degree for a regular graph")
        graph = set()
        while len(graph) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in graph and (v, u) not in graph:
                graph.add((u, v))
        return list(graph)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    
    for d in [5, 10, 15, 20, 30, 40]:
        if n_max >= 40:
            break
        
        for _ in range(5):
            graph = generate_d_regular_graph(n_max + 1, d)
            del_pezzo = del_pezzo_degree(graph)
            entanglement_complexity = circuit_entanglement_complexity(graph)
            
            if del_pezzo == 0 or entanglement_complexity == 0:
                continue
            
            metric_values.append(del_pezzo / entanglement_complexity)
            instances_tested += 1
            n_max = max(n_max, len(graph))
    
    if not metric_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    r = pearson_correlation(metric_values, [Fraction(i) for i in range(1, len(metric_values) + 1)])
    if r < 0.7:
        conjecture_holds = False
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[support_fraction < 0.8][0]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=metric_saturation n_tested={len(results)}")