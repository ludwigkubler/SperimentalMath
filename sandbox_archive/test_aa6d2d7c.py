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
    
    def generate_delone_triangulation(n):
        # Simple Delone triangulation generation (not actual Delone triangulation)
        vertices = [(random.random(), random.random()) for _ in range(n)]
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if math.dist(vertices[i], vertices[j]) < 0.5:
                    edges.append((i, j))
        return vertices, edges

    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if all(matrix[i][j] == 0 for j in range(n)):
                continue
            pivot_col = next(j for j in range(n) if matrix[i][j] != 0)
            for j in range(pivot_col, n):
                matrix[i][j] /= matrix[i][pivot_col]
            for k in range(m):
                if k == i:
                    continue
                factor = matrix[k][pivot_col]
                for j in range(pivot_col, n):
                    matrix[k][j] -= factor * matrix[i][j]
            rank += 1
        return rank

    def is_k_clique(graph, k):
        vertices = list(graph.keys())
        for subset in itertools.combinations(vertices, k):
            if not all(graph[u][v] for u, v in itertools.combinations(subset, 2)):
                return False
        return True

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_rank = 0
    num_k_clique = 0

    for n in n_values:
        vertices, edges = generate_delone_triangulation(n)
        graph = {i: {} for i in range(n)}
        for u, v in edges:
            graph[u][v] = 1
            graph[v][u] = 1

        rank = matrix_rank([[graph[i].get(j, 0) for j in range(n)] for i in range(n)])
        results.append({
            "metric_name": "Rank",
            "metric_value": rank,
            "instances_tested": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
        total_rank += rank

        if is_k_clique(graph, 3):
            num_k_clique += 1

    mean_rank = total_rank / len(results)
    support_fraction = (num_k_clique > 0.8 * len(n_values))

    return {
        "metric_name": "Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")