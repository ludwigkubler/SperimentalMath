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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u][v] = 1
            graph[v][u] = 1
            edges.add((u, v))
        return graph
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = -1
            for j in range(rank, m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(n):
                if j == i:
                    matrix[rank][j] = 1 / matrix[rank][j]
                else:
                    matrix[rank][j] *= -matrix[rank][i]
            for j in range(m):
                if j != rank:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def min_categorical_dimension(graph):
        n = len(graph)
        adjacency_matrix = [[graph[i][j] for j in range(n)] for i in range(n)]
        rank = gaussian_elimination(adjacency_matrix)
        return rank
    
    def communication_complexity_rank(graph):
        n = len(graph)
        total_edges = sum(sum(row) for row in graph) // 2
        if total_edges == 0:
            return 0
        min_cut = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                cut_size = sum(graph[i][k] + graph[j][k] for k in range(n) if k != i and k != j)
                min_cut = min(min_cut, cut_size)
        return min_cut
    
    def is_d_regular(graph, d):
        n = len(graph)
        degrees = [sum(row) for row in graph]
        return all(deg == d for deg in degrees)
    
    results = []
    for n in range(5, 41):
        for _ in range(30):
            d = random.randint(2, min(n - 1, 10))
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            if not is_d_regular(graph, d):
                continue
            min_dim = min_categorical_dimension(graph)
            r = communication_complexity_rank(graph)
            results.append((n, d, min_dim, r))
    
    if not results:
        return {
            "metric_name": "min_dim_over_r",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_dim_over_r = [min_dim / r for n, d, min_dim, r in results if r > 0]
    if not min_dim_over_r:
        return {
            "metric_name": "min_dim_over_r",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_rank_zero"
        }
    
    mean = sum(min_dim_over_r) / len(min_dim_over_r)
    std = math.sqrt(sum((x - mean) ** 2 for x in min_dim_over_r) / len(min_dim_over_r))
    support_fraction = sum(1 for x in min_dim_over_r if x >= 0.5 * mean) / len(min_dim_over_r)
    
    return {
        "metric_name": "min_dim_over_r",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n for n, d, min_dim, r in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_dim_over_r < 0.5 * mean\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")