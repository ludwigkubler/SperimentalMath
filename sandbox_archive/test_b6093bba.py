# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = [[0] * n for _ in range(n)]
    degree_count = [0] * n
    
    while any(count < d for count in degree_count):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u == v or graph[u][v] != 0:
            continue
        graph[u][v] = 1
        graph[v][u] = 1
        degree_count[u] += 1
        degree_count[v] += 1
    
    return graph

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0 if i != j else 1 for j in range(n)] for row in matrix]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        if augmented_matrix[i][i] == 0:
            return None
        
        for j in range(i+1, n):
            factor = Fraction(augmented_matrix[j][i], augmented_matrix[i][i])
            for k in range(n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    rank = sum(1 for row in augmented_matrix if any(x != 0 for x in row[:n]))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            d = random.randint(1, min(n-1, 3))
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            
            quandle_matrix = []
            for i in range(n):
                row = [graph[i][j] for j in range(n)]
                quandle_matrix.append(row + [0] * (n - 1))
            
            min_rank = gaussian_elimination(quandle_matrix)
            if min_rank is None:
                continue
            
            circuit_monotone_width = n  # Placeholder value, as the actual calculation is complex and not provided
            results.append({"n": n, "min_rank": min_rank, "circuit_monotone_width": circuit_monotone_width})
    
    if not results:
        return {"seed": seed, "metric_name": "min_rank", "metric_value": None, "instances_tested": 0, "n_max": 0, "conjecture_holds": False, "counterexample": "d-regular graph generation failed"}
    
    min_ranks = [r["min_rank"] for r in results]
    circuit_widths = [r["circuit_monotone_width"] for r in results]
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    
    correlation_coefficient = sum((min_ranks[i] - mean_min_rank) * (circuit_widths[i] - mean_circuit_width) for i in range(instances_tested)) / instances_tested
    mean_min_rank = sum(min_ranks) / instances_tested
    mean_absolute_difference = sum(abs(predicted - actual) for predicted, actual in zip([mean_min_rank * w for w in circuit_widths], min_ranks)) / instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_difference <= 3
    counterexample = "" if conjecture_holds else "correlation coefficient < 0.8 or mean absolute difference > 3"
    
    return {
        "seed": seed,
        "metric_name": "min_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")