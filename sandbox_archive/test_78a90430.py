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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def determinant(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def inverse_matrix(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            minor = determinant(submatrix)
            adjoint[i][j] = (-1) ** (i+j) * minor
    
    inv_A = matrix_multiply(adjoint, identity_matrix(n))
    return [[inv_A[i][j] / det_A for j in range(n)] for i in range(n)]

def geometric_entropy(matrix):
    n = len(matrix)
    eigenvalues = []
    A = copy.deepcopy(matrix)
    while A:
        eigenvector = gaussian_elimination(A)
        lambda_val = sum(eigenvector[i] * matrix[i][j] for i, j in enumerate(range(n)))
        eigenvalues.append(lambda_val)
        A = [[A[i][j] - lambda_val * eigenvector[j] for j in range(n)] for i in range(n)]
    
    entropy = 0
    for val in eigenvalues:
        if val != 0:
            entropy -= val * math.log(val)
    return entropy

def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, num_vars) * (-1 if random.choice([True, False]) else 1)]
        while len(clause) < 3:
            var = random.randint(1, num_vars)
            if var not in clause:
                clause.append(var * (-1 if random.choice([True, False]) else 1))
        cnf.append(clause)
    return cnf

def adjacency_matrix(cnf):
    n = len(cnf)
    adj = [[0] * (n+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(i+1, n):
            if any(abs(cnf[i][k]) == abs(cnf[j][l]) and (cnf[i][k] != cnf[j][l]) for k in range(len(cnf[i])) for l in range(len(cnf[j]))):
                adj[i][j] = 1
                adj[j][i] = 1
    return adj

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        num_clauses = random.randint(n // 2, n * 2)
        cnf = generate_cnf(n, num_clauses)
        adj_matrix = adjacency_matrix(cnf)
        
        try:
            H_min = geometric_entropy(adj_matrix)
        except ValueError as e:
            return {
                "metric_name": "geometric_entropy",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
        
        results.append({
            "n": n,
            "H_min": H_min,
            "num_clauses": num_clauses
        })
    
    if len(results) < 16:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    H_min_values = [result["H_min"] for result in results]
    num_clauses_values = [result["num_clauses"] for result in results]
    
    mean_H_min = sum(H_min_values) / len(H_min_values)
    std_H_min = math.sqrt(sum((x - mean_H_min) ** 2 for x in H_min_values) / len(H_min_values))
    correlation_coefficient = sum((H_min_values[i] - mean_H_min) * (num_clauses_values[i] - mean_num_clauses) for i in range(len(results))) / (len(results) * std_H_min * std_num_clauses)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_H_min = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_H_min = math.sqrt(sum((r["metric_value"] - mean_H_min) ** 2 for r in results if r["conjecture_holds"]) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_min} std={std_H_min} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_H_min} std={std_H_min} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")