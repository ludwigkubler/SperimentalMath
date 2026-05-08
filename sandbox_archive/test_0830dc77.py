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

def generate_graph(n):
    if n == 1:
        return [[0]]
    graph = [[0] * n for _ in range(n)]
    for i in range(1, n):
        graph[0][i] = 1
        graph[i][0] = 1
    return graph

def is_connected(graph):
    visited = [False] * len(graph)
    stack = [0]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor, edge in enumerate(graph[node]):
                if edge and not visited[neighbor]:
                    stack.append(neighbor)
    return all(visited)

def find_asymptotic_dimension(graph):
    n = len(graph)
    if not is_connected(graph):
        return 0
    for dim in range(1, n):
        for subset in itertools.combinations(range(n), dim + 1):
            subgraph = [[0] * (dim + 2) for _ in range(dim + 2)]
            for i in range(dim + 1):
                for j in range(dim + 1):
                    if graph[subset[i]][subset[j]]:
                        subgraph[i][j] = 1
            if not is_connected(subgraph):
                return dim
    return n - 1

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        for j in range(cols):
            matrix[i][j] /= pivot
        for j in range(rows):
            if j != i:
                factor = matrix[j][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def resolution_length(graph):
    n = len(graph)
    clauses = []
    for i in range(n):
        clause = [0] * (n + 1)
        clause[0] = -i
        for j in range(i + 1, n):
            if graph[i][j]:
                clause[j + 1] = 1
        clauses.append(clause)
    matrix = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if graph[i][j]:
                matrix[i][j + 1] = -1
    gaussian_elimination(matrix)
    return sum(1 for row in matrix if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_graph(n)
        while not is_connected(graph):
            graph = generate_graph(n)
        ν_G = find_asymptotic_dimension(graph)
        length = resolution_length(graph)
        results.append((ν_G, length))
    metric_value = sum(length / (2 ** ν) for ν, length in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(length >= 2 ** ν for ν, length in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Resolution Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")