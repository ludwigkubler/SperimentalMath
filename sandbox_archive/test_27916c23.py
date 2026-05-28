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

# Helper functions for matrix operations
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m = len(A)
    n = len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    return [row[-1] for row in augmented_matrix]

def matrix_inverse(A):
    m = len(A)
    n = len(A[0])
    identity = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(m)]
    augmented_matrix = [A[i] + identity[i] for i in range(m)]
    
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        for j in range(n*2):
            augmented_matrix[i][j] /= pivot
        
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n*2):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    inverse = [row[n:] for row in augmented_matrix]
    return inverse

def matrix_determinant(A):
    m = len(A)
    if m != len(A[0]):
        raise ValueError("Matrix must be square")
    
    if m == 1:
        return A[0][0]
    
    det = Fraction(0, 1)
    for j in range(m):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += ((-1) ** j) * A[0][j] * matrix_determinant(submatrix)
    
    return det

def is_full_rank(A):
    return matrix_determinant(A) != Fraction(0, 1)

# Function to compute the minimal rank of a quandle from a graph
def quandle_rank(graph_edges):
    n = len(graph_edges)
    adjacency_matrix = [[Fraction(0, 1)] * n for _ in range(n)]
    
    for u, v in graph_edges:
        if u < n and v < n:
            adjacency_matrix[u][v] = Fraction(1, 1)
            adjacency_matrix[v][u] = Fraction(1, 1)
    
    return len(gaussian_elimination(adjacency_matrix, [Fraction(0, 1)] * n))

# Function to generate a random graph
def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < 0.5:
                edges.add((i, j))
    return list(edges)

# Function to compute the Tseitin formula and its resolution refutation length
def tseitin_formula_and_refutation_length(graph_edges):
    n = len(graph_edges)
    literals = {f"x{i}": i for i in range(n)}
    clauses = []
    
    # Add clauses for each edge
    for u, v in graph_edges:
        literals_uv = f"u{u}{v}"
        literals_vu = f"v{v}{u}"
        clauses.append([literals[u], literals[v], -literals_uv])
        clauses.append([literals[v], literals[u], -literals_vu])
        clauses.append([-literals[u], -literals[v], literals_uv, literals_vu])
    
    # Add clauses for each vertex
    for i in range(n):
        literals_i = f"x{i}"
        literals_neg_i = f"neg_x{i}"
        clauses.append([literals_i, literals_neg_i])
        for j in range(i+1, n):
            literals_j = f"x{j}"
            literals_neg_j = f"neg_x{j}"
            clauses.append([-literals_i, -literals_j, literals_neg_i, literals_neg_j])
    
    # Convert to CNF and compute resolution refutation length
    cnf = clauses
    refutation_length = 0
    while True:
        new_clauses = []
        for clause1 in cnf:
            for clause2 in cnf:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = [l for l in clause1 + clause2 if l not in clause1 and l not in clause2]
                    if len(new_clause) == 0:
                        return refutation_length
                    new_clauses.append(new_clause)
        cnf.extend(new_clauses)
        refutation_length += 1
    
    return refutation_length

# Function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph_edges = generate_random_graph(n)
    quandle_r = quandle_rank(graph_edges)
    refutation_length = tseitin_formula_and_refutation_length(graph_edges)
    
    return {
        "metric_name": "quandle_rank",
        "metric_value": quandle_r,
        "instances_tested": 1,
        "conjecture_holds": quandle_r > 0 and refutation_length >= 2 ** quandle_r,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")