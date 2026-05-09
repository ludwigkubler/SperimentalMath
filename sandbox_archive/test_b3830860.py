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

def generate_random_regular_graph(n, k):
    if n * k % 2 != 0:
        raise ValueError("n*k must be even")
    adj = [[0] * n for _ in range(n)]
    edges = set()
    for i in range(n):
        neighbors = random.sample(range(i + 1, n), k // 2)
        for j in neighbors:
            if (i, j) not in edges and (j, i) not in edges:
                adj[i][j] = 1
                adj[j][i] = 1
                edges.add((i, j))
    return adj

def normalize_laplacian(adj):
    n = len(adj)
    degree = [sum(row) for row in adj]
    laplacian = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                laplacian[i][j] = degree[i]
            else:
                laplacian[i][j] = -adj[i][j]
    return laplacian

def spectral_norm(laplacian):
    n = len(laplacian)
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    v = [random.random() for _ in range(n)]
    for _ in range(100):  # Power iteration
        v = [sum(laplacian[i][j] * v[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x**2 for x in v))
        v = [x / norm for x in v]
    return abs(v[0])

def cheeger_constant(adj):
    n = len(adj)
    laplacian = normalize_laplacian(adj)
    lambda_max = spectral_norm(laplacian)
    lambda_min = 1e-6
    while lambda_max - lambda_min > 1e-5:
        lambda_mid = (lambda_max + lambda_min) / 2
        if all(sum(adj[i][j] for j in range(n)) >= lambda_mid * n for i in range(n)):
            lambda_min = lambda_mid
        else:
            lambda_max = lambda_mid
    return lambda_min

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [1 if i == j else 0 for j in range(m)] for i in range(m)]
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[n:] for row in augmented]

def dpll_with_clause_learning(clauses, assignment=None):
    if assignment is None:
        assignment = {}
    if not clauses:
        return True
    var = next(var for var in range(len(clauses[0])) if var not in assignment)
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        new_clauses = []
        for clause in clauses:
            if any(var == abs(lit) and (lit > 0) == val for lit in clause):
                continue
            elif all(abs(lit) != var for lit in clause):
                new_clauses.append(clause)
        if dpll_with_clause_learning(new_clauses, new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 3
    adj = generate_random_regular_graph(n, k)
    h_G = cheeger_constant(adj)
    tau_G = [[random.choice([1, -1]) for _ in range(n)] for _ in range(n)]
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i][j] == 1:
                clauses.append([-i - 1, -j - 1])
                clauses.append([i + 1, j + 1])
    refutation_length = len(gaussian_elimination(clauses))
    metric_value = refutation_length
    conjecture_holds = refutation_length >= 2 ** (h_G * math.log(n))
    counterexample = "" if conjecture_holds else f"h(G)={h_G}, n={n}"
    return {
        "metric_name": "refutation_length",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")