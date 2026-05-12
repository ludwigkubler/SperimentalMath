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

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(n):
    I = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    return I

def inverse(A):
    n = len(A)
    I = identity_matrix(n)
    for k in range(n):
        pivot = A[k][k]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def eigenvalues(A):
    n = len(A)
    lambda_values = []
    for _ in range(10):  # Simple power iteration method
        x = [random.random() for _ in range(n)]
        x_norm = sum(x[i] ** 2 for i in range(n)) ** 0.5
        x = [x_i / x_norm for x_i in x]
        for _ in range(10):
            y = matrix_multiplication(A, x)
            y_norm = sum(y[i] ** 2 for i in range(n)) ** 0.5
            y = [y_i / y_norm for y_i in y]
            lambda_new = sum(x[i] * y[i] for i in range(n))
            if abs(lambda_new - lambda_values[-1]) < 1e-6:
                break
        lambda_values.append(lambda_new)
    return sorted(lambda_values)

def tseitin_formula(G, root):
    n = len(G)
    literals = [f"v{i+1}" for i in range(n)]
    clauses = []
    for u in range(n):
        if G[u][root] == 1:
            clauses.append([literals[u]])
        else:
            clauses.append([-literals[u]])
        for v in range(u + 1, n):
            if G[u][v] == 1:
                clauses.append([literals[u], -literals[v]])
                clauses.append([-literals[u], literals[v]])
    return literals, clauses

def d_regular_expander(n, d):
    A = [[0 for _ in range(n)] for _ in range(n)]
    degree = [0] * n
    for u in range(n):
        while degree[u] < d:
            v = random.randint(0, n - 1)
            if u != v and degree[v] < d and A[u][v] == 0:
                A[u][v] = 1
                A[v][u] = 1
                degree[u] += 1
                degree[v] += 1
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2 * n // (n - 1)
    G = d_regular_expander(n, d)
    lambda_2 = eigenvalues(G)[1]
    literals, clauses = tseitin_formula(G, 0)
    
    def sat_solver(clauses):
        assignment = [False] * len(literals)
        stack = []
        for clause in clauses:
            found_unassigned = False
            for literal in clause:
                var_index = abs(literal) - 1
                if not assignment[var_index]:
                    assignment[var_index] = literal > 0
                    stack.append((var_index, literal))
                    found_unassigned = True
                    break
            if not found_unassigned:
                return False
        while stack:
            var_index, literal = stack.pop()
            for clause in clauses:
                if literal in clause and -literal in clause:
                    return False
        return True
    
    proof_length = 0
    for _ in range(10):  # Sample multiple instances
        if not sat_solver(clauses):
            proof_length += 1
    
    conjecture_holds = lambda_2 * proof_length > 1.5 * n ** 1.5
    counterexample = "" if conjecture_holds else f"n={n}, d={d}, λ₂={lambda_2}, proof_length={proof_length}"
    
    return {
        "metric_name": "Proof Length",
        "metric_value": proof_length,
        "instances_tested": 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")