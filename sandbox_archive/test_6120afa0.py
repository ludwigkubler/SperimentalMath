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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def inverse(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is not invertible")
    
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = (-1) ** (i+j) * determinant(submatrix)
            adjoint[j][i] = cofactor
    
    inv_A = matrix_multiplication(adjoint, [[Fraction(1, det_A)] * n for _ in range(n)])
    return inv_A

def local_inductive_dimension(vertices, edges):
    n = len(vertices)
    if n == 0:
        return -1
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    laplacian_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency_matrix[i])
        laplacian_matrix[i][i] = degree
        for j in range(i+1, n):
            laplacian_matrix[i][j] = -adjacency_matrix[i][j]
            laplacian_matrix[j][i] = -adjacency_matrix[i][j]
    
    try:
        inv_laplacian = inverse(laplacian_matrix)
    except ValueError:
        return -1
    
    null_space_basis = []
    for i in range(n):
        vector = [inv_laplacian[j][i] for j in range(n)]
        if all(abs(x) < 1e-9 for x in vector):
            null_space_basis.append(vector)
    
    if len(null_space_basis) == 0:
        return -1
    
    null_space_matrix = list(zip(*null_space_basis))
    rank_null_space = sum(1 for row in null_space_matrix if any(x != 0 for x in row))
    
    return n - rank_null_space

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n * (n - 1) // 2 > 1000:  # Skip if too many edges
            continue
        
        for _ in range(5):  # Sample 5 instances per size
            clauses = [random.sample(range(n), random.randint(1, n)) for _ in range(random.randint(1, n))]
            vertices = set()
            edges = []
            
            for clause in clauses:
                for literal in clause:
                    vertices.add(abs(literal) - 1)
                    for other_literal in clause:
                        if abs(other_literal) != abs(literal):
                            u, v = sorted([abs(literal) - 1, abs(other_literal) - 1])
                            edges.append((u, v))
            
            l_d = local_inductive_dimension(vertices, edges)
            if l_d == -1:
                continue
            
            w_phi = len(clauses)
            results.append({"n": n, "w_phi": w_phi, "l_d": l_d})
    
    if not results:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    metric_values = [result["w_phi"] for result in results]
    l_d_values = [result["l_d"] for result in results]
    
    if len(metric_values) < 30:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean = sum(metric_values) / len(metric_values)
    variance = sum((x - mean) ** 2 for x in metric_values) / len(metric_values)
    std_dev = math.sqrt(variance)
    
    correlation_coefficient = sum((metric_values[i] - mean) * (l_d_values[i] - mean) for i in range(len(metric_values))) / (len(metric_values) * std_dev * std_dev)
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean,
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    metric_values = [result["metric_value"] for result in seeds]
    instances_tested = sum(result["instances_tested"] for result in seeds)
    n_max = max(result["n_max"] for result in seeds)
    support_fraction = sum(1 for result in seeds if result["conjecture_holds"]) / len(seeds)
    
    if all(result["conjecture_holds"] for result in seeds):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / instances_tested} std={math.sqrt(sum((x - sum(metric_values) / instances_tested) ** 2 for x in metric_values) / instances_tested)} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] == "" for result in seeds):
        first_failing_seed = next(seed for seed, result in zip(seeds, seeds) if not result["conjecture_holds"] and result["counterexample"] == "")
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_max={n_max}")