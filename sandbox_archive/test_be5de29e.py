# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_regular_graph(n, k):
    if (n * k) % 2 != 0:
        return None
    edges = set()
    for i in range(n):
        neighbors = random.sample(range(n), k)
        for j in neighbors:
            if i < j:
                edges.add((i, j))
    return list(edges)

def laplacian_matrix(graph, n):
    L = [[0] * n for _ in range(n)]
    degree = [sum(1 for edge in graph if edge[0] == node or edge[1] == node) for node in range(n)]
    for i in range(n):
        L[i][i] = degree[i]
    for u, v in graph:
        L[u][v] -= 1
        L[v][u] -= 1
    return L

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def eigenvalue_lower_bound(L):
    n = len(L)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    L_plus_identity = [[L[i][j] + identity[i][j] for j in range(n)] for i in range(n)]
    det_L_plus_identity = determinant(L_plus_identity)
    lambda_2 = (det_L_plus_identity - n) / (n * (n - 1))
    return lambda_2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_random_regular_graph(n, k=3)
        if not graph:
            return {
                "metric_name": "Resolution length",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "graph_not_possible"
            }
        L = laplacian_matrix(graph, n)
        lambda_2 = eigenvalue_lower_bound(L)
        if lambda_2 <= 0:
            continue
        resolution_length = 2 ** (n * lambda_2)
        results.append(resolution_length)
    metric_value = sum(results) / len(results)
    conjecture_holds = all(length >= 2**(n*lambda_2) for length in results)
    counterexample = "" if conjecture_holds else "resolution_length_too_short"
    return {
        "metric_name": "Resolution length",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 2**(n*lambda_2)) / len(results)
    print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")