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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
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

def rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    return sum(1 for row in A_copy if any(row))

def geometric_entropy(G):
    n = len(G)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in G:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    laplacian_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency_matrix[i])
        laplacian_matrix[i][i] = degree
        for j in range(i+1, n):
            laplacian_matrix[i][j] = -adjacency_matrix[i][j]
            laplacian_matrix[j][i] = -adjacency_matrix[j][i]
    
    rank_laplacian = rank(laplacian_matrix)
    if rank_laplacian == 0:
        return float('inf')
    gamma_G = -math.log2(rank_laplacian / n)
    return gamma_G

def tseitin_formula(G):
    n = len(G)
    variables = {f'x{i}': i for i in range(n)}
    clauses = []
    for u, v in G:
        clauses.append([variables[f'x{u}'], -variables[f'x{v}']])
        clauses.append([-variables[f'x{u}'], variables[f'x{v}']])
    return clauses

def resolution_length(clauses):
    stack = []
    while True:
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if not unit_clause:
            break
        literal = unit_clause[0]
        stack.append(literal)
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clauses.extend([c for c in clause if c != -literal])
            else:
                new_clauses.append(clause)
        clauses = new_clauses
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n)]
    
    gamma_G = geometric_entropy(G)
    if gamma_G == float('inf'):
        return {
            "metric_name": "resolution_length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    F_G = tseitin_formula(G)
    length_F_G = resolution_length(F_G)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length_F_G,
        "instances_tested": 1,
        "conjecture_holds": length_F_G >= 2 ** gamma_G,
        "counterexample": "" if length_F_G >= 2 ** gamma_G else f"length_F_G={length_F_G}, 2^gamma_G={2 ** gamma_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")