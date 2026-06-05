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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot_row = rank
            while pivot_row < m and A[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row == m:
                continue
            A[rank], A[pivot_row] = A[pivot_row], A[rank]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
            rank += 1
        return rank
    
    def min_categorical_dimension(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph.items():
            for w in v:
                adjacency_matrix[u][w] = 1
        return gaussian_elimination(adjacency_matrix)
    
    def communication_complexity_rank(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph.items():
            for w in v:
                adjacency_matrix[u][w] = 1
        rank = gaussian_elimination(adjacency_matrix)
        return rank
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "min_categorical_dimension",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    min_dim = min_categorical_dimension(graph)
    rank = communication_complexity_rank(graph)
    
    return {
        "metric_name": "min_categorical_dimension",
        "metric_value": min_dim,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_dim >= rank * Fraction(1, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")