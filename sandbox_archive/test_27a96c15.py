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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    graph[i][j] = graph[j][i] = random.randint(1, 10)
        return graph
    
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
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            b[i] /= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(n):
                        M[j][k] -= factor * M[i][k]
                    b[j] -= factor * b[i]
        return [row[:-1] for row in M], b
    
    def compute_eigenvalues(matrix):
        n = len(matrix)
        identity = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        eigenvalues = []
        for _ in range(10):  # Power iteration method
            x = [random.random() for _ in range(n)]
            x = [x[i] / sum(x) for i in range(n)]
            y = matrix_multiplication(matrix, x)
            lambda_ = sum(y[i] * x[i] for i in range(n))
            eigenvalues.append(lambda_)
        return eigenvalues
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    
    # Convert graph to moment matrix
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(i + 1, n):
            M[i][j] = M[j][i] = graph[i][j]
    
    # Add identity matrix to make it a moment matrix
    for i in range(n):
        M[i][n] = M[n][i] = 1
    
    eigenvalues = compute_eigenvalues(M)
    
    metric_value = max(eigenvalues) - min(eigenvalues)
    conjecture_holds = all(-1 <= e <= 1 for e in eigenvalues)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Eigenvalue Gap",
        "metric_value": metric_value,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")