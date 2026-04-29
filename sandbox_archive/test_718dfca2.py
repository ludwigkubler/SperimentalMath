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

def generate_random_3regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even")
    graph = [[] for _ in range(n)]
    degree = 3
    edges = set()
    
    while len(edges) < n * degree // 2:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    
    return graph

def is_3regular(graph):
    for neighbors in graph:
        if len(neighbors) != 3:
            return False
    return True

def generate_random_odd_charge_labelling(n):
    return [random.choice([1, -1]) for _ in range(n)]

def simulate_tseitin_resolution(graph, charge_labelling):
    n = len(graph)
    assignment = [None] * n
    stack = []
    
    def propagate():
        while stack:
            u = stack.pop()
            if assignment[u] is None:
                assignment[u] = charge_labelling[u]
                for v in graph[u]:
                    if assignment[v] is None:
                        stack.append(v)
    
    def resolve():
        for u in range(n):
            if assignment[u] is None:
                propagate()
                if any(assignment[v] == -charge_labelling[u] for v in graph[u]):
                    return False
        return True
    
    stack.extend(range(n))
    return resolve()

def spectral_radius(graph):
    n = len(graph)
    adj_matrix = [[0] * n for _ in range(n)]
    
    for u, neighbors in enumerate(graph):
        for v in neighbors:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
    
    def matrix_multiplication(A, B):
        n = len(A)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            
            M[i], M[max_row] = M[max_row], M[i]
            
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            M[i][-1] /= factor
            
            for j in range(i+1, n):
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
                M[j][-1] -= factor * M[i][-1]
        
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = M[i][-1]
            for j in range(i+1, n):
                x[i] -= M[i][j] * x[j]
        return x
    
    def power_iteration(A, max_iter=1000):
        n = len(A)
        v = [1] * n
        for _ in range(max_iter):
            v = matrix_multiplication(A, v)
            norm = sum(x**2 for x in v) ** 0.5
            v = [x / norm for x in v]
        return max(abs(x) for x in v)
    
    return power_iteration(adj_matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 15, 20, 25, 30, 35, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_3regular_graph(n)
        if not is_3regular(graph):
            return {
                "metric_name": "spectral_radius",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "graph_not_3regular"
            }
        
        max_spectral_radius = 0
        total_length = 0
        
        for _ in range(30):
            charge_labelling = generate_random_odd_charge_labelling(n)
            length = simulate_tseitin_resolution(graph, charge_labelling)
            if not length:
                return {
                    "metric_name": "spectral_radius",
                    "metric_value": None,
                    "instances_tested": 0,
                    "conjecture_holds": False,
                    "counterexample": "resolution_failed"
                }
            total_length += length
            max_spectral_radius = max(max_spectral_radius, spectral_radius(graph))
        
        results.append({
            "n": n,
            "spectral_radius": max_spectral_radius,
            "average_length": total_length / 30
        })
    
    conjecture_holds = all(math.log(result["average_length"]) >= math.log(2) * result["spectral_radius"] for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, spectral_radius={results[0]['spectral_radius']}, average_length={results[0]['average_length']}"
    
    return {
        "metric_name": "spectral_radius",
        "metric_value": max_spectral_radius,
        "instances_tested": 30 * len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i + 3**j + 5**k for i, j, k in itertools.product(range(4), range(4), range(4))]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        mean_length = sum(result["average_length"] for result in results) / len(results)
        std_length = math.sqrt(sum((result["average_length"] - mean_length)**2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"spectral_radius_vs_length\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")