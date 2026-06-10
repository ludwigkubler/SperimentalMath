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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_inverse(A):
    rows = len(A)
    cols = len(A[0])
    if rows != cols:
        raise ValueError("Matrix must be square")
    augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(A)]
    for i in range(rows):
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i, cols * 2):
            augmented_matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, cols * 2):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    inverse = [row[cols:] for row in augmented_matrix]
    return inverse

def gaussian_elimination(A, b):
    rows = len(A)
    cols = len(A[0])
    if rows != cols:
        raise ValueError("Matrix must be square")
    augmented_matrix = [A[i] + [b[i]] for i in range(rows)]
    for i in range(rows):
        pivot_row = i
        for j in range(i+1, rows):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[pivot_row][i]):
                pivot_row = j
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, cols + 1):
            augmented_matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, cols + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return [row[-1] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n*3)
    
    # Generate a random CNF formula
    phi = []
    variables = list(range(1, n+1))
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        phi.append(clause)
    
    # Construct the corresponding groupoid G(φ)
    G = {}
    for var in variables:
        G[var] = set()
    for clause in phi:
        for lit in clause:
            if lit > 0:
                G[lit].add(-lit)
                G[-lit].add(lit)
    
    # Compute the minimal groupoid homology rank min_homrank(G(φ))
    def find_cycle(graph):
        visited = set()
        stack = []
        
        def dfs(node):
            if node in visited:
                return True
            if node in stack:
                return False
            visited.add(node)
            stack.append(node)
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            stack.pop()
            return True
        
        for node in graph:
            if not dfs(node):
                return True
        return False
    
    homology_rank = 0
    while find_cycle(G):
        homology_rank += 1
        # Remove a cycle from the graph
        for node in G:
            if len(G[node]) == 2 and list(G[node])[0] != -list(G[node])[1]:
                u, v = list(G[node])
                del G[u][v]
                del G[v][u]
    
    # Calculate the clause satisfiability complexity sat_complexity(φ)
    def dpll(phi):
        if not phi:
            return True
        literals = set()
        for clause in phi:
            literals.update(clause)
        literals = list(literals)
        
        for lit in literals:
            new_phi = [clause for clause in phi if lit not in clause and -lit not in clause]
            if dpll(new_phi):
                return True
        
        for lit in literals:
            new_phi = [clause for clause in phi if -lit not in clause]
            if dpll(new_phi):
                return True
        
        return False
    
    sat_complexity = 1 if dpll(phi) else 0
    
    # Correlation analysis
    correlation_coefficient = (homology_rank * sat_complexity - n * m / 2) / math.sqrt(n * m * (n + m) / 4)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")