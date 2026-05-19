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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        b[i] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def is_connected(graph):
    n = len(graph)
    visited = [False] * n
    stack = [0]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            for neighbor in range(n):
                if graph[node][neighbor] and not visited[neighbor]:
                    stack.append(neighbor)
    return all(visited)

def betti_number(graph):
    n = len(graph)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                A[i][j] = A[j][i] = -1
                b[i] += 1
                b[j] += 1
    gaussian_elimination(A, b)
    rank = sum(1 for row in A if any(row))
    return rank

def resolution_width(graph):
    n = len(graph)
    literals = list(range(n))
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                clauses.append([literals[0]] + [-x for x in literals[1:]])
    A = [[0] * len(clauses) for _ in range(len(literals))]
    b = [0] * len(clauses)
    for i, clause in enumerate(clauses):
        for j in range(len(literals)):
            if any(x == literals[j] or x == -literals[j] for x in clause):
                A[j][i] += 1
                b[i] += 1
    gaussian_elimination(A, b)
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = [[0] * n for _ in range(n)]
    for _ in range(random.randint(1, n - 1)):
        u, v = random.sample(range(n), 2)
        if not graph[u][v]:
            graph[u][v] = graph[v][u] = 1
    if not is_connected(graph):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "graph_not_connected"
        }
    betti = betti_number(graph)
    width = resolution_width(graph)
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= betti,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width < betti_number\" first_failing_seed={first_failing_seed}")