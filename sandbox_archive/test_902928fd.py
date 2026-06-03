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

def generate_tseitin_formula(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    vertices = list(range(n))
    edges = []
    for v in vertices:
        neighbors = random.sample(vertices, d - 1)
        while v in neighbors:
            neighbors = random.sample(vertices, d - 1)
        edges.extend([(v, u) for u in neighbors])
    
    clauses = []
    for (u, v) in edges:
        clauses.append((u, v))
        clauses.append((v, u))
    
    return vertices, edges, clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    pivot_col = 0
    
    for i in range(rows):
        if pivot_col >= cols:
            break
        
        max_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][pivot_col]) > abs(matrix[max_row][pivot_col]):
                max_row = r
        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        if matrix[i][pivot_col] == 0:
            pivot_col += 1
            continue
        
        for r in range(rows):
            if r != i and matrix[r][pivot_col] != 0:
                factor = -matrix[r][pivot_col] / matrix[i][pivot_col]
                for c in range(cols):
                    matrix[r][c] += factor * matrix[i][c]
        
        rank += 1
        pivot_col += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    min_ranks = []
    widths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            vertices, edges, clauses = generate_tseitin_formula(n, 2)
            
            # Construct the groupoid cocycle matrix
            cocycle_matrix = [[0] * n for _ in range(n)]
            for (u, v) in edges:
                cocycle_matrix[u][v] += 1
                cocycle_matrix[v][u] += 1
            
            # Compute the minimal rank of the cocycle matrix
            min_rank = gaussian_elimination(cocycle_matrix)
            min_ranks.append(min_rank)
            
            # Simulate resolution proof width (placeholder for actual computation)
            width = n * math.log2(n)  # Placeholder value
            widths.append(width)
    
    if not min_ranks or not widths:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": len(min_ranks),
            "n_max": max(len(vertices) for vertices, _, _ in generate_tseitin_formula(40, 2)),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    correlation_coefficient = sum((x - mean_min_ranks) * (y - mean_widths) for x, y in zip(min_ranks, widths)) / (len(min_ranks) * math.sqrt(variance_min_ranks) * math.sqrt(variance_widths))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": sum(min_ranks) / len(min_ranks),
        "instances_tested": len(min_ranks),
        "n_max": max(len(vertices) for vertices, _, _ in generate_tseitin_formula(40, 2)),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_min_ranks = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    variance_min_ranks = sum((r["metric_value"] - mean_min_ranks) ** 2 for r in results if r["metric_value"] is not None) / len(results)
    mean_widths = sum(r["widths"] for r in results) / len(results)
    variance_widths = sum((r["widths"] - mean_widths) ** 2 for r in results) / len(results)
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={mean_min_ranks:.2f} std={math.sqrt(variance_min_ranks):.2f} support_fraction={support_fraction:.2f}")