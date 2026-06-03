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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < d * n // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u][v] = 1
            graph[v][u] = 1
            edges.add((u, v))
    return graph

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            return None
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank_of_matrix(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    if reduced_matrix is None:
        return 0
    n = len(reduced_matrix)
    rank = 0
    for row in reduced_matrix:
        if any(row[j] != 0 for j in range(n)):
            rank += 1
    return rank

def compute_hdw(graph):
    n = len(graph)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                matrix[i][j] = -1
                matrix[j][i] = -1
                matrix[i][n] += 1
                matrix[j][n] += 1
    return rank_of_matrix(matrix)

def compute_circuit_width(graph):
    n = len(graph)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if graph[i][j] == 1]
    min_width = float('inf')
    for d in range(2, n + 1):
        for s in range(2 ** (d - 1), 2 ** d):
            width = 0
            visited = [False] * n
            stack = []
            for u in range(n):
                if not visited[u]:
                    stack.append(u)
                    while stack:
                        v = stack.pop()
                        visited[v] = True
                        width += 1
                        for w in range(n):
                            if graph[v][w] == 1 and not visited[w]:
                                stack.append(w)
            min_width = min(min_width, width)
    return min_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, random.randint(2, min(n - 1, 3)))
            if graph is None:
                continue
            hdw_value = compute_hdw(graph)
            circuit_width = compute_circuit_width(graph)
            if hdw_value is not None and circuit_width is not None:
                correlation_sum += abs(hdw_value - circuit_width)
                instances_tested += 1
                n_max = max(n_max, n)

    mean_correlation = correlation_sum / instances_tested if instances_tested > 0 else float('inf')
    support_fraction = instances_tested / (len(n_values) * 5)
    
    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    elif mean_correlation > 3 or support_fraction < 0.8:
        conjecture_holds = False
        counterexample = f"mean_correlation={mean_correlation}, support_fraction={support_fraction}"

    return {
        "metric_name": "Mean Absolute Difference",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mean_correlation or support_fraction\" first_failing_seed={first_failing_seed}")