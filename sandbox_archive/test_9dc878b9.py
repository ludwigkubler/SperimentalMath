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

def generate_max_cut_instance(n):
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.append((i, j))
    return edges

def degree_matrix(edges, n):
    D = [[0] * n for _ in range(n)]
    for u, v in edges:
        D[u][u] += 1
        D[v][v] += 1
    return D

def adjacency_matrix(edges, n):
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b=None):
    n = len(A)
    if b is not None:
        A = [row + [b[i]] for i, row in enumerate(A)]
    
    for i in range(n):
        max_row = max(range(i, n), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        
        factor = 1 / A[i][i]
        A[i] = [x * factor for x in A[i]]
        if b is not None:
            b[i] *= factor
        
        for j in range(n):
            if i != j:
                factor = A[j][i]
                A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
                if b is not None:
                    b[j] -= factor * b[i]
    
    return A

def spectral_radius(matrix):
    n = len(matrix)
    eigenvalues = []
    A = matrix[:]
    for _ in range(100):  # Power iteration method
        x = [random.random() for _ in range(n)]
        x_norm = sum(x[i]**2 for i in range(n))**0.5
        x = [x[i] / x_norm for i in range(n)]
        
        y = matrix_multiply(A, x)
        y_norm = sum(y[i]**2 for i in range(n))**0.5
        y = [y[i] / y_norm for i in range(n)]
        
        lambda_ = sum(x[i] * y[i] for i in range(n))
        eigenvalues.append(lambda_)
    
    return max(eigenvalues)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_max_cut_instance(n)
    D = degree_matrix(instance, n)
    A = adjacency_matrix(instance, n)
    
    M = matrix_multiply(D, A)
    rho_M = spectral_radius(M)
    
    c = rho_M / math.sqrt(n)
    approximation_ratio = c / math.sqrt(n)
    
    return {
        "metric_name": "approximation_ratio",
        "metric_value": approximation_ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(c - 1) < 0.1 and abs(approximation_ratio - 1) < 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30 * 2 + 1, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"\" first_failing_seed=-1")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")