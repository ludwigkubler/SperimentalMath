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

def random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                edges.add((i, j))
    return edges

def adjacency_matrix(graph, n):
    matrix = [[0] * n for _ in range(n)]
    for u, v in graph:
        matrix[u][v] = 1
        matrix[v][u] = 1
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def determinant(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError("Matrix must be square")
    n = len(matrix)
    det = Fraction(1)
    for i in range(n):
        det *= matrix[i][i]
    return det

def min_tropical_rank(matrix):
    n = len(matrix)
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    augmented_matrix = [row + col for row, col in zip(matrix, identity)]
    gaussian_eliminated = gaussian_elimination(augmented_matrix)
    min_tr = sum(1 for row in gaussian_eliminated if any(x != 0 for x in row))
    return min_tr

def circuit_size(graph):
    n = len(graph)
    edges = list(graph)
    vertices = set(range(n))
    visited = [False] * n
    stack = []
    
    def dfs(v):
        visited[v] = True
        stack.append(v)
        for u in range(n):
            if (v, u) in edges or (u, v) in edges:
                if not visited[u]:
                    dfs(u)
        stack.pop()
    
    connected_components = 0
    for v in vertices:
        if not visited[v]:
            connected_components += 1
            dfs(v)
    
    return len(edges) + connected_components - 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = random_graph(n)
        A = adjacency_matrix(graph, n)
        min_tr_G = min_tropical_rank(A)
        s_C_G = circuit_size(graph)
        
        if min_tr_G > 10:
            return {
                "metric_name": "min_tr(G)",
                "metric_value": min_tr_G,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Graph with {n} vertices has min_tr(G) = {min_tr_G} > 10"
            }
        
        results.append((min_tr_G, s_C_G))
    
    mean_metric_value = sum(min_tr for min_tr, _ in results) / len(results)
    std_metric_value = math.sqrt(sum((min_tr - mean_metric_value)**2 for min_tr, _ in results) / len(results))
    support_fraction = sum(1 for min_tr, s_C_G in results if min_tr <= 1.5 * s_C_G) / len(results)
    
    return {
        "metric_name": "min_tr(G)",
        "metric_value": mean_metric_value,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["min_tr(G)"] > 10 for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n=40 has min_tr(G) > 10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(seeds)}")