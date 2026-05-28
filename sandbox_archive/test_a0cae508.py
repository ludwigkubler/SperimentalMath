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

def gaussian_elimination(A):
    n = len(A)
    m = len(A[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(m, 2*m)] for i, row in enumerate(A)]
    
    def swap_rows(i, j):
        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
    
    def scale_row(i, factor):
        augmented_matrix[i] = [factor * x for x in augmented_matrix[i]]
    
    def add_multiple_of_row(i, j, factor):
        augmented_matrix[j] = [augmented_matrix[j][k] + factor * augmented_matrix[i][k] for k in range(2*m)]
    
    def find_pivot(row):
        for i in range(m):
            if augmented_matrix[row][i] != 0:
                return i
        return -1
    
    row, col = 0, 0
    while row < n and col < m:
        pivot_row = row
        for i in range(row + 1, n):
            if abs(augmented_matrix[i][col]) > abs(augmented_matrix[pivot_row][col]):
                pivot_row = i
        
        if augmented_matrix[pivot_row][col] == 0:
            col += 1
            continue
        
        swap_rows(row, pivot_row)
        
        scale_row(row, 1 / augmented_matrix[row][col])
        
        for i in range(n):
            if i != row:
                add_multiple_of_row(row, i, -augmented_matrix[i][col])
        
        row += 1
        col += 1
    
    return [row[m:] for row in augmented_matrix]

def rank(matrix):
    rref = gaussian_elimination(matrix)
    return sum(1 for row in rref if any(x != 0 for x in row))

def k_clique_instance(n, k):
    vertices = list(range(n))
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < (k / (n - 1)):
                edges.append((i, j))
    return vertices, edges

def quasi_metric_space(edges):
    n = len(edges)
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = A[v][u] = random.random()
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = min(n // 2, 3)  # Ensure k is at least 1 and not too large
        vertices, edges = k_clique_instance(n, k)
        dist = quasi_metric_space(edges)
        rank_value = rank(dist)
        results.append((n, rank_value))
    
    mean_rank = sum(rank for n, rank in results) / len(results)
    std_dev = math.sqrt(sum((rank - mean_rank) ** 2 for n, rank in results) / len(results))
    
    conjecture_holds = all(mean_rank >= n**k - 0.5*n**k and mean_rank <= n**k + 0.5*n**k for n, _ in results)
    counterexample = "" if conjecture_holds else "n^k bounds not met"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n^k bounds not met\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")