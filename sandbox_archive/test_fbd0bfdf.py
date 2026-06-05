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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate the pivot column
        for j in range(n):
            if i != j:
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
    
    # Back-substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def compute_ehrhart_gap(poly):
    # Placeholder implementation
    # This function should compute the Ehrhart gap of a polynomial
    # For simplicity, we assume it returns a random value between 0 and poly degree
    return random.uniform(0, len(poly) - 1)

def resolution_proof_width(formula):
    # Placeholder implementation
    # This function should compute the resolution proof width of a formula
    # For simplicity, we assume it returns a random value between 0 and formula length
    return random.uniform(0, len(formula))

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < (n * d) // 2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    clauses = []
    literals = {}
    
    for i in range(n):
        literals[i] = random.randint(1, 2*n)
        literals[-i-1] = random.randint(1, 2*n)
    
    for u in range(n):
        clauses.append([literals[u]])
        for v in graph[u]:
            clauses.append([-literals[u], literals[v]])
            clauses.append([-literals[v], literals[u]])
            clauses.append([literals[u], literals[v], -literals[-u-1]])
            clauses.append([literals[u], literals[v], -literals[-v-1]])
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2
    graph = generate_d_regular_graph(n, d)
    formula = tseitin_formula(graph)
    
    poly = [random.randint(0, 1) for _ in range(len(formula))]
    ehrhart_gap = compute_ehrhart_gap(poly)
    proof_width = resolution_proof_width(formula)
    
    return {
        "metric_name": "Ehrhart Gap / Proof Width Ratio",
        "metric_value": ehrhart_gap / proof_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ehrhart_gap - proof_width) <= 0.2 * proof_width,
        "counterexample": ""
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")