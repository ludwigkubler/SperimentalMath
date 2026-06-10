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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        n = len(A)
        r = 0
        for i in range(n):
            if any(A[i][j] != 0 for j in range(n)):
                r += 1
        return r

    def generate_d_regular_graph(d, n):
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u in range(n):
            clause = [f'-{literals[u]}']
            for v in graph[u]:
                clause.append(f'{literals[v]}')
            clauses.append(clause)
        return clauses

    def tropical_rank_ratio(graph, d, n):
        clauses = tseitin_formula(graph)
        A = [[0] * (n + len(clauses)) for _ in range(n + len(clauses))]
        for i in range(n):
            A[i][i] = 1
            for j in graph[i]:
                A[j][i] = -1
        for k, clause in enumerate(clauses):
            A[n + k][n + k] = 1
            for literal in clause:
                if literal.startswith('x'):
                    var = int(literal[1:])
                    A[var][n + k] = -1
                elif literal.startswith('-x'):
                    var = int(literal[2:])
                    A[var][n + k] = 1
        rank_A = rank(gaussian_elimination(A))
        return rank_A / (n * math.log(d) / math.log(n))

    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        d = random.randint(2, min(n-1, 5))
        graph = generate_d_regular_graph(d, n)
        ratio = tropical_rank_ratio(graph, d, n)
        total_ratio += ratio
        instances_tested += len(graph)
        n_max = max(n_max, n)

    mean_val = Fraction(total_ratio, len(n_values))
    std_dev = 0
    for n in n_values:
        d = random.randint(2, min(n-1, 5))
        graph = generate_d_regular_graph(d, n)
        ratio = tropical_rank_ratio(graph, d, n)
        std_dev += (ratio - mean_val) ** 2
    std_dev = math.sqrt(std_dev / len(n_values))

    conjecture_holds = all(ratio <= 2 * std_dev for ratio in [tropical_rank_ratio(generate_d_regular_graph(random.randint(2, min(n-1, 5)), n), random.randint(2, min(n-1, 5)), n) for _ in range(30)])
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "tropical_rank_ratio",
        "metric_value": float(mean_val),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_val = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_val) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")