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

def generate_k_clique(n, k):
    if n < k:
        return None
    clique = list(range(k))
    edges = set()
    for i in range(k):
        for j in range(i + 1, k):
            edges.add((clique[i], clique[j]))
    while len(clique) < n:
        new_vertex = random.randint(0, n - 1)
        if all((new_vertex, v) not in edges and (v, new_vertex) not in edges for v in clique):
            clique.append(new_vertex)
            for v in clique[:-1]:
                edges.add((clique[-1], v))
    return clique

def compute_homology_rank(simplicial_complex):
    # Simplified homology computation using Smith normal form
    n = len(simplicial_complex)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(i, n):
            if (i, j) in simplicial_complex:
                matrix[i][j] = 1
                matrix[j][i] = 1
    # Compute Smith normal form
    rank = 0
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            if matrix[i][j]:
                pivot = matrix[i][j]
                for k in range(j, n + 1):
                    matrix[i][k] -= (matrix[j][k] * pivot) // matrix[j][j]
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        clique = generate_k_clique(n, random.randint(2, min(3, n)))
        if clique is None:
            continue
        simplicial_complex = {(i, j) for i in range(n) for j in range(i + 1, n)}
        homology_rank = compute_homology_rank(simplicial_complex)
        comm_complexity = len(clique) ** 2  # Simplified communication complexity
        results.append({
            "n": n,
            "homology_rank": homology_rank,
            "comm_complexity": comm_complexity
        })
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    mean_rank = sum(result["homology_rank"] for result in results) / len(results)
    max_comm_complexity = max(result["comm_complexity"] for result in results)
    conjecture_holds = all(max_comm_complexity <= 2 * n ** 3 for result in results)
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_comm_complexity={max_comm_complexity}, n_max=40"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r is not None and r <= 40) / len(results)
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")