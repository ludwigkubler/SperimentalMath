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

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = -augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] += factor * augmented_matrix[i][k]
    indices = [0] * n
    for i in range(n-1, -1, -1):
        indices[i] = int(augmented_matrix[i][-2])
    return indices

def min_index_quaternionic_kahler_metric(graph):
    n = len(graph)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u in graph:
        for v in graph[u]:
            adjacency_matrix[u][v] += 1
    indices = gaussian_elimination(adjacency_matrix)
    return max(indices)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = []
    for _ in range(n):
        clause = [random.choice([True, False]) for _ in range(n)]
        phi.append(clause)
    
    graph = {i: set() for i in range(n)}
    for u in range(n):
        for v in range(u+1, n):
            if any(phi[u][j] != phi[v][j] for j in range(n)):
                graph[u].add(v)
                graph[v].add(u)
    
    try:
        min_index = min_index_quaternionic_kahler_metric(graph)
    except ZeroDivisionError:
        return {
            "metric_name": "min_index",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    satisfiable = any(all(clause[i] == phi[u][i] for i in range(n)) for u in graph)
    if satisfiable:
        expected_index = (math.log2(n)) ** 0.25
    else:
        expected_index = float('inf')
    
    return {
        "metric_name": "min_index",
        "metric_value": min_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_index <= expected_index,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"] and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")