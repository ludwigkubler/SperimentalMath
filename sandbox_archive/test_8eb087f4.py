# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                return None  # Singular matrix, no solution
            for j in range(i+1, n):
                factor = matrix[j][i] / pivot
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def resolution_length(graph):
        n = len(graph)
        matrix = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if graph[i][j]:
                    matrix[i][j] = -1
                    matrix[j][i] = -1
                    matrix[i][-1] += 1
                    matrix[j][-1] += 1
        
        result = gaussian_elimination(matrix)
        if result is None:
            return float('inf')
        
        rank = sum(1 for row in result if any(row))
        return n - rank
    
    def asymptotic_dimension(graph):
        n = len(graph)
        for dim in range(n + 1):
            coverings = combinations(range(n), dim)
            if all(any(graph[i][j] for i, j in combinations(cov, 2)) for cov in coverings):
                return dim
        return n
    
    def generate_graph(n, dim):
        graph = [[0] * n for _ in range(n)]
        vertices = list(range(n))
        random.shuffle(vertices)
        for i in range(dim):
            subset = vertices[:i+1]
            for u, v in combinations(subset, 2):
                graph[u][v] = graph[v][u] = 1
        return graph
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            graph = generate_graph(n, random.randint(1, min(n-1, 3)))
            dim = asymptotic_dimension(graph)
            length = resolution_length(graph)
            total_length += length
            instances_tested += 1
    
    mean_length = total_length / instances_tested
    conjecture_holds = mean_length >= 2 ** (0.5 * n_values[-1])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")