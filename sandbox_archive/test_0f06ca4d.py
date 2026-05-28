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

def generate_clique_instance(n, k):
    if n < k:
        return None, 0, []
    
    vertices = list(range(n))
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in vertices[:k]]
    random.shuffle(edges)
    edges = edges[:n * k // 2]
    
    return vertices, k, edges

def matrix_multiplication(A, B):
    m, p = len(A), len(B[0])
    result = [[sum(A[i][j] * B[j][k] for j in range(p)) for k in range(p)] for i in range(m)]
    return result

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            return None
        
        for j in range(n):
            augmented_matrix[i][j] /= pivot
        
        for r in range(n):
            if r != i:
                factor = augmented_matrix[r][i]
                for j in range(n):
                    augmented_matrix[r][j] -= factor * augmented_matrix[i][j]
    
    return [row[n:] for row in augmented_matrix]

def algebraic_curve_complexity(vertices, edges):
    n = len(vertices)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    rank = len(gaussian_elimination(adjacency_matrix))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    curve_complexities = []
    
    for n in n_values:
        k = min(n // 2, 5)  # Ensure k is at least 1 and at most n/2
        vertices, _, edges = generate_clique_instance(n, k)
        
        if vertices is None:
            return {
                "metric_name": "C(F)/n^k",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "k > n"
            }
        
        complexity = algebraic_curve_complexity(vertices, edges)
        curve_complexities.append(complexity / (n ** k))
    
    mean_value = sum(curve_complexities) / len(curve_complexities)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in curve_complexities) / len(curve_complexities))
    
    return {
        "metric_name": "C(F)/n^k",
        "metric_value": mean_value,
        "instances_tested": len(n_values),
        "conjecture_holds": abs(mean_value - 1) <= 0.1 and max(curve_complexities) <= 1.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] or r["metric_value"] is None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] is not None for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"C(F)/n^k > 1.1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no data points")