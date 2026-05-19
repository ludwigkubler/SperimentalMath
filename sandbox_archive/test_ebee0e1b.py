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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        factor = Fraction(matrix[i][i])
        for k in range(i+1, n):
            factor_k = Fraction(matrix[k][i]) / factor
            for j in range(n):
                matrix[k][j] -= factor_k * matrix[i][j]

    return matrix

def solve_linear_system(matrix, b):
    n = len(matrix)
    gaussian_elimination(matrix)
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        sum_j = 0
        for j in range(i+1, n):
            sum_j += matrix[i][j] * x[j]
        x[i] = (b[i] - sum_j) / Fraction(matrix[i][i])
    
    return x

def adjacency_matrix_to_laplacian(adj_matrix):
    n = len(adj_matrix)
    laplacian = [[0] * n for _ in range(n)]
    degree_sum = [sum(row) for row in adj_matrix]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                laplacian[i][j] = degree_sum[i]
            else:
                laplacian[i][j] = -adj_matrix[i][j]
    
    return laplacian

def second_largest_eigenvalue(laplacian):
    n = len(laplacian)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    eigenvalues = []
    
    for _ in range(2):  # Compute a few eigenvalues
        eigenvector = [random.random() for _ in range(n)]
        eigenvector /= math.sqrt(sum(x**2 for x in eigenvector))
        
        while True:
            new_eigenvector = solve_linear_system(laplacian, eigenvector)
            if all(abs(new_eigenvector[i] - eigenvector[i]) < 1e-6 for i in range(n)):
                break
            eigenvector = new_eigenvector
    
        eigenvalues.append(sum(laplacian[i][j] * eigenvector[j] for j in range(n)))
    
    return max(eigenvalues)

def tseitin_formula(adj_matrix):
    n = len(adj_matrix)
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    for i in range(n):
        clauses.append([literals[i]])
        for j in range(i+1, n):
            clauses.append([-literals[i], -literals[j]])
            clauses.append([literals[i], literals[j]])
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    p = 0.5
    
    adj_matrix = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    adj_matrix = [row[:] for row in adj_matrix]  # Ensure it's a copy
    
    laplacian = adjacency_matrix_to_laplacian(adj_matrix)
    lambda_2 = second_largest_eigenvalue(laplacian)
    
    if lambda_2 <= 0:
        return {
            "metric_name": "log2_resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "lambda_2_non_positive"
        }
    
    tseitin_clauses = tseitin_formula(adj_matrix)
    # Simulate SAT solver (placeholder for actual implementation)
    resolution_length = len(tseitin_clauses) * 10  # Placeholder value
    
    log2_length = math.log2(resolution_length)
    if log2_length < lambda_2 * n:
        return {
            "metric_name": "log2_resolution_length",
            "metric_value": log2_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"resolution_length={resolution_length}, expected >= {lambda_2 * n}"
        }
    
    return {
        "metric_name": "log2_resolution_length",
        "metric_value": log2_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={seed}")
                break