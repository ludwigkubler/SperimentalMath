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
    
    def generate_3_regular_graph(m):
        while True:
            vertices = list(range(m))
            edges = []
            for v in vertices:
                neighbors = random.sample(vertices, 2)
                if v not in neighbors and (v, neighbors[0]) not in edges and (v, neighbors[1]) not in edges:
                    edges.append((v, neighbors[0]))
                    edges.append((v, neighbors[1]))
            if len(edges) == 3 * m // 2:
                return vertices, edges
    
    def compute_edge_expansion(vertices, edges):
        n = len(vertices)
        min_cut_size = float('inf')
        for i in range(1, n // 2 + 1):
            for S in itertools.combinations(vertices, i):
                cut_size = sum(1 for u, v in edges if (u in S and v not in S) or (v in S and u not in S))
                min_cut_size = min(min_cut_size, cut_size)
        return min_cut_size / n
    
    def compute_median_edge_bipartition(edges):
        sorted_edges = sorted(edges)
        mid = len(sorted_edges) // 2
        first_half = sorted_edges[:mid]
        second_half = sorted_edges[mid:]
        return (first_half, second_half)
    
    def compute_truth_table(vertices, edges, sigma):
        n = len(vertices)
        m = len(edges)
        truth_table = [[0] * (1 << m) for _ in range(1 << n)]
        for i in range(1 << n):
            for j in range(1 << m):
                value = 1
                for v in vertices:
                    if sigma[v] == 1 - ((i >> v) & 1):
                        value *= (-1)
                truth_table[i][j] = value
        return truth_table
    
    def compute_rank(matrix):
        rank = 0
        m, n = len(matrix), len(matrix[0])
        for col in range(n):
            pivot_row = -1
            for row in range(m):
                if matrix[row][col] != 0:
                    if pivot_row == -1:
                        pivot_row = row
                    else:
                        factor = matrix[pivot_row][col] / matrix[row][col]
                        for c in range(n):
                            matrix[row][c] -= factor * matrix[pivot_row][c]
        rank = sum(1 for row in range(m) if any(matrix[row]))
        return rank
    
    n_values = [4, 6, 8, 10, 12, 14]
    results = []
    
    for n in n_values:
        m = 3 * n // 2
        for _ in range(5):  # Ensure we test at least 30 instances per seed
            vertices, edges = generate_3_regular_graph(m)
            sigma = {v: random.choice([0, 1]) for v in vertices}
            h_G = compute_edge_expansion(vertices, edges)
            first_half, second_half = compute_median_edge_bipartition(edges)
            truth_table = compute_truth_table(vertices, first_half + second_half, sigma)
            rank = compute_rank(truth_table)
            
            results.append({
                "metric_name": "log2_rank",
                "metric_value": math.log2(rank),
                "instances_tested": 1,
                "conjecture_holds": math.log2(rank) >= 0.25 * h_G * m,
                "counterexample": "" if math.log2(rank) >= 0.25 * h_G * m else f"m={m}, rank={rank}"
            })
    
    return {
        "seed": seed,
        "metric_name": "log2_rank",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")