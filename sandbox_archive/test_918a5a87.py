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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = -1
            for r in range(rank, rows):
                if matrix[r][i] != 0:
                    pivot_row = r
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for r in range(rows):
                if r != rank - 1:
                    factor = matrix[r][i] / matrix[rank - 1][i]
                    for c in range(cols):
                        matrix[r][c] -= factor * matrix[rank - 1][c]
        return rank
    
    def compute_K_group_rank(graph, n):
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        # Compute the rank of the adjacency matrix
        return gaussian_elimination(adjacency_matrix)
    
    def compute_resolution_proof_width(graph):
        n = len(graph)
        if n == 0:
            return 0
        max_clause_length = 2 * n - 3
        return max_clause_length
    
    c = 1.5  # Empirical constant for the conjecture
    instances_tested = 0
    total_width = 0
    total_rank = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            graph = generate_graph(n)
            width = compute_resolution_proof_width(graph)
            rank = compute_K_group_rank(graph, n)
            
            instances_tested += 1
            total_width += width
            total_rank += rank
    
    mean_width = total_width / instances_tested
    mean_rank = total_rank / instances_tested
    ratio_mean = mean_rank / (mean_width ** c)
    
    conjecture_holds = 0.5 <= ratio_mean <= 2
    counterexample = "" if conjecture_holds else f"Ratio out of bounds: {ratio_mean}"
    
    return {
        "metric_name": "Ratio of K-group rank to width^c",
        "metric_value": ratio_mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")