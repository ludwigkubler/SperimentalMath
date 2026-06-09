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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is not invertible")
    adjoint = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = (-1)**(i+j) * determinant(submatrix)
            adjoint[j][i] = cofactor
    inv_A = matrix_multiplication(adjoint, [[Fraction(1, det_A)]*n for _ in range(n)])
    return inv_A

def local_inductive_dimension(vertices, edges):
    n = len(vertices)
    adjacency_matrix = [[0]*n for _ in range(n)]
    for u, v in edges:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    laplacian_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency_matrix[i])
        laplacian_matrix[i][i] = degree
        for j in range(i+1, n):
            laplacian_matrix[i][j] = -adjacency_matrix[i][j]
            laplacian_matrix[j][i] = -adjacency_matrix[j][i]
    
    eigenvalues = []
    for i in range(n):
        eigenvector = [Fraction(1, math.sqrt(n))] * n
        if i == 0:
            eigenvector[0] = Fraction(1)
        else:
            eigenvector[i] = Fraction(1)
        
        while True:
            new_vector = matrix_multiplication(laplacian_matrix, eigenvector)
            norm = sum(x**2 for x in new_vector)**0.5
            if abs(norm - 1) < 1e-6:
                eigenvalues.append(sum(new_vector))
                break
            eigenvector = [x / norm for x in new_vector]
    
    return max(eigenvalues)

def generate_random_cnf(n, m):
    clauses = []
    variables = list(range(1, n+1))
    for _ in range(m):
        clause = random.sample(variables, 2)
        clause.append(random.choice([-1, 1]) * random.choice(clause))
        clauses.append(clause)
    return clauses

def resolution_width(cnf):
    stack = []
    while cnf:
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if not unit_clause:
            break
        literal = unit_clause[0]
        cnf.remove(unit_clause)
        for clause in cnf[:]:
            if literal in clause:
                cnf.remove(clause)
            elif -literal in clause:
                new_clause = [l for l in clause if l != -literal]
                if len(new_clause) == 1:
                    stack.append(new_clause[0])
                else:
                    cnf.append(new_clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_random_cnf(n, n * (n - 1) // 2)
        width = resolution_width(cnf)
        
        vertices = list(range(n))
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        l_d = local_inductive_dimension(vertices, edges)
        
        results.append({
            "n": n,
            "width": width,
            "l_d": l_d
        })
    
    correlation_coefficient = 0
    if len(results) > 1:
        x_mean = sum(r["width"] for r in results) / len(results)
        y_mean = sum(r["l_d"] for r in results) / len(results)
        
        numerator = sum((r["width"] - x_mean) * (r["l_d"] - y_mean) for r in results)
        denominator = math.sqrt(sum((r["width"] - x_mean)**2 for r in results)) * math.sqrt(sum((r["l_d"] - y_mean)**2 for r in results))
        
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in [r["l_d"] / r["width"] for r in results]),
        "counterexample": "" if correlation_coefficient >= 0.8 else "correlation_coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and all(corr >= 0.5 for corr in [r["l_d"] / r["width"] for r in results]):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")