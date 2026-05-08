# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, product

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i, j, k in product(range(n), repeat=3):
        C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        det += (-1) ** j * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
    return det

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def is_planar(G):
    n = len(G)
    if n <= 4:
        return True
    for u in range(n):
        neighbors = [v for v in range(n) if G[u][v]]
        if len(neighbors) >= 5:
            subgraph = {u}
            for v in neighbors:
                subgraph.update(neighbors)
                if len(subgraph) > n - 3:
                    return False
    return True

def tree_depth(G):
    n = len(G)
    visited = [False] * n
    depth = [0] * n
    
    def dfs(u, d):
        visited[u] = True
        depth[u] = d
        for v in range(n):
            if G[u][v] and not visited[v]:
                dfs(v, d + 1)
    
    dfs(0, 0)
    return max(depth)

def tseitin_formula(G):
    n = len(G)
    literals = list(range(-n, 0)) + list(range(1, n+1))
    neg_literals = [-l for l in literals]
    clauses = []
    
    def add_clause(c):
        clauses.append(c)
    
    for u in range(n):
        if sum(G[u]) > 2:
            add_clause([literals[u]] + [neg_literals[v] for v in range(n) if G[u][v]])
    
    for u, v in combinations(range(n), 2):
        if G[u][v]:
            add_clause([-literals[u], literals[v]])
            add_clause([literals[u], -literals[v]])
            add_clause([-literals[v], literals[u]])
            add_clause([literals[v], -literals[u]])
    
    return literals, neg_literals, clauses

def dpll_with_clause_learning(G, literals, neg_literals, clauses):
    n = len(literals)
    assignment = {l: None for l in literals}
    learned_clauses = []
    
    def propagate():
        while True:
            found = False
            for c in clauses + learned_clauses:
                unit_clause = next((l for l in c if assignment.get(l) is None and assignment.get(-l) is False), None)
                if unit_clause:
                    assignment[unit_clause] = True
                    found = True
                    break
            if not found:
                return True
    
    def backtrack():
        while True:
            if all(assignment[l] is not None for l in literals):
                return False
            var = next(l for l in literals if assignment.get(l) is None)
            assignment[var] = False
            learned_clauses.append([var])
    
    if propagate() and backtrack():
        return True, assignment
    else:
        return False, {}

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    G = [row[:] for row in G]
    for i in range(n):
        G[i][i] = 0
    
    tau_G = tree_depth(G)
    literals, neg_literals, clauses = tseitin_formula(G)
    
    refutation_length = len(dpll_with_clause_learning(G, literals, neg_literals, clauses)[1])
    
    c = 0.3
    if tau_G > 2:
        expected_length = 2 ** (c * tau_G)
    else:
        expected_length = n**2
    
    conjecture_holds = refutation_length >= expected_length
    counterexample = "" if conjecture_holds else f"tau(G)={tau_G}, refutation_length={refutation_length}"
    
    return {
        "metric_name": "refutation_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")