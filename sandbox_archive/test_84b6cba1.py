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

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.add((i, j))
    return edges

def laplacian_matrix(G, n):
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if (i, j) in G or (j, i) in G)
        L[i][i] = -degree
        for j in range(i + 1, n):
            if (i, j) in G or (j, i) in G:
                L[i][j] = 1
                L[j][i] = 1
    return L

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = Fraction(1)
    for i in range(n):
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i + 1, n):
                A[j][k] -= factor * A[i][k]
        det *= A[i][i]
    return det

def algebraic_connectivity(G, n):
    L = laplacian_matrix(G, n)
    eigenvalues = []
    for i in range(n):
        identity = [[Fraction(1) if j == k else Fraction(0) for j in range(n)] for k in range(n)]
        A = [row[:] for row in L]
        A[i][i] -= 1
        det_A = determinant(A)
        eigenvalues.append(det_A / n)
    return min(eigenvalue for eigenvalue in eigenvalues if eigenvalue > 0)

def Tseitin_formula(G, n):
    literals = [f"x{i}" for i in range(n)]
    clauses = []
    for i in range(n):
        clause = [literals[i]]
        for j in range(i + 1, n):
            if (i, j) not in G and (j, i) not in G:
                clause.append(f"~{literals[j]}")
        clauses.append(clause)
    return literals, clauses

def resolution_length(clauses):
    queue = [clause[:] for clause in clauses]
    while queue:
        clause_i = queue.pop(0)
        if len(clause_i) == 1:
            return len(queue) + 1
        for clause_j in queue:
            common_lits = set(lit for lit in clause_i if f"~{lit}" in clause_j)
            if common_lits:
                new_clause = [lit for lit in clause_i + clause_j if lit not in common_lits and f"~{lit}" not in common_lits]
                queue.append(new_clause)
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(3, 40)
    G = generate_random_graph(n)
    μ = algebraic_connectivity(G, n)
    if μ <= 1/n:
        c = 1
    else:
        c = 1/10
    Tseitin_lits, Tseitin_clauses = Tseitin_formula(G, n)
    length = resolution_length(Tseitin_clauses)
    conjecture_holds = length >= 2**(c * μ)
    counterexample = "" if conjecture_holds else f"μ={μ}, length={length}"
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_length = sum(result["metric_value"] for result in results) / len(results)
    std_length = math.sqrt(sum((result["metric_value"] - mean_length)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")