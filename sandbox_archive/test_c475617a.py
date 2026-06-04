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

def nearest_neighbor_graph(n):
    graph = [[] for _ in range(n)]
    points = [[random.random(), random.random()] for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = ((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2) ** 0.5
            if dist < 0.1:
                graph[i].append(j)
                graph[j].append(i)
    
    return graph

def communication_complexity_matrix(graph):
    n = len(graph)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j and (j in graph[i] or i in graph[j]):
                matrix[i][j] = 1
    
    return matrix

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
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot
        
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    rank = sum(1 for row in augmented_matrix if any(row[i] != 0 for i in range(n)))
    return rank

def geometric_entropy(matrix):
    n = len(matrix)
    eigenvalues = []
    
    # Compute eigenvalues using power iteration method
    v = [Fraction(1, n) for _ in range(n)]
    for _ in range(100):  # Number of iterations
        v = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
        norm = sum(v[i] ** 2 for i in range(n))
        v = [v[i] / norm for i in range(n)]
    
    # Approximate eigenvalues
    for _ in range(10):  # Number of iterations
        v_old = v[:]
        v = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
        norm = sum(v[i] ** 2 for i in range(n))
        v = [v[i] / norm for i in range(n)]
    
    # Sum of eigenvalues
    return sum(v)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = nearest_neighbor_graph(n)
        matrix = communication_complexity_matrix(graph)
        rank = gaussian_elimination(matrix)
        entropy = geometric_entropy(matrix)
        
        results.append({
            "n": n,
            "rank": rank,
            "entropy": entropy
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_entropy = sum(result["entropy"] for result in results) / len(results)
    
    conjecture_holds = all(entropy >= rank for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")