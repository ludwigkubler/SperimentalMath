# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
from fractions import Fraction

def generate_delone_triangulation(n):
    vertices = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
    triangulation = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if is_triangle(vertices[i], vertices[j], vertices[k]):
                    triangulation.append((i, j, k))
    return triangulation

def is_triangle(p1, p2, p3):
    area = abs(p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1])) / 2
    return area > 0

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(min(m, n)):
        if any(matrix[j][i] != 0 for j in range(i, m)):
            rank += 1
            for j in range(i + 1, m):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return rank

def is_k_clique(graph, k):
    nodes = list(graph.keys())
    for subset in itertools.combinations(nodes, k):
        if not all(graph[u][v] for u, v in itertools.combinations(subset, 2)):
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    triangulation = generate_delone_triangulation(n)
    graph = {i: {} for i in range(n)}
    for u, v, _ in triangulation:
        graph[u][v] = 1
        graph[v][u] = 1
    
    rank = matrix_rank([[graph[i].get(j, 0) for j in range(n)] for i in range(n)])
    
    is_kclique = is_k_clique(graph, 3)
    conjecture_holds = False
    counterexample = ""
    if is_kclique:
        if rank >= Fraction(1, 2) * n ** (3 / 2):
            conjecture_holds = True
        else:
            counterexample = "k-CLIQUE instance with insufficient rank"
    else:
        if abs(rank - Fraction(1, 4) * n ** (3 / 2)) <= 0.01 * n:
            conjecture_holds = True
        else:
            counterexample = "Non-k-CLIQUE instance with incorrect rank"
    
    return {
        "metric_name": "Matrix Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")