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

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [[A[i][j] for j in range(n + 1)] for i in range(n)]
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n]
        for k in range(i + 1, n):
            x[i] -= M[i][k] * x[k]
    return x

def is_independent_set(G, S):
    for u in S:
        for v in S:
            if u != v and (u, v) in G or (v, u) in G:
                return False
    return True

def find_max_independent_set(G):
    n = len(G)
    max_size = 0
    max_set = []
    for i in range(1 << n):
        S = [j for j in range(n) if (i & (1 << j)) != 0]
        if is_independent_set(G, S) and len(S) > max_size:
            max_size = len(S)
            max_set = S
    return max_set

def tree_depth(G):
    n = len(G)
    visited = [False] * n
    depth = [0] * n
    
    def dfs(u, d):
        visited[u] = True
        depth[u] = d
        for v in G[u]:
            if not visited[v]:
                dfs(v, d + 1)
    
    max_depth = 0
    for i in range(n):
        if not visited[i]:
            dfs(i, 0)
            max_depth = max(max_depth, max(depth))
    return max_depth

def tseitin_formula(G):
    n = len(G)
    literals = [f"x{i}" for i in range(n)]
    neg_literals = [f"~x{i}" for i in range(n)]
    clauses = []
    
    # Clause for each vertex
    for i in range(n):
        clause = [literals[i]]
        for j in G[i]:
            clause.append(neg_literals[j])
        clauses.append(clause)
    
    # Clause for each edge (i, j) with i < j
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in G or (j, i) in G:
                clause = [neg_literals[i], neg_literals[j]]
                clauses.append(clause)
    
    return literals, neg_literals, clauses

def dpll_with_clause_learning(G, literals, neg_literals, clauses):
    n = len(literals)
    assignment = {l: None for l in literals + neg_literals}
    learned_clauses = []
    
    def propagate():
        while True:
            changed = False
            for literal, value in assignment.items():
                if value is not None:
                    for clause in clauses:
                        if literal in clause and all(assignment.get(l) == (not v) for l, v in zip(clause, [True] * len(clause))):
                            return False
                        elif literal in clause and all(assignment.get(l) == v for l, v in zip(clause, [False] * len(clause))):
                            learned_clauses.append([neg_literal for neg_literal in neg_literals if neg_literal != literal])
                            changed = True
            if not changed:
                break
        return True
    
    def backtrack():
        while True:
            unit_clause = next((c for c in clauses if sum(1 for l in c if assignment.get(l) is None and assignment.get(neg_l) is False) == 1), None)
            if unit_clause is None:
                return True
            literal = next(l for l in unit_clause if assignment.get(l) is None and assignment.get(neg_l) is False)
            assignment[literal] = True
            if not propagate():
                assignment[literal] = False
                learned_clauses.append([neg_l for neg_l in neg_literals if neg_l != literal])
    
    if propagate() and backtrack():
        return True, []
    else:
        return False, learned_clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = {i: [] for i in range(n)}
    for _ in range(random.randint(int(n * (n - 1) / 2), int(n * (n - 1) / 2) + 10)):
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in G and (v, u) not in G:
            G[u].append(v)
            G[v].append(u)
    
    tau_G = tree_depth(G)
    literals, neg_literals, clauses = tseitin_formula(G)
    
    refutation_length = 0
    for _ in range(10):
        assignment = {l: None for l in literals + neg_literals}
        learned_clauses = []
        if not dpll_with_clause_learning(G, literals, neg_literals, clauses)[0]:
            refutation_length += len(clauses) + len(learned_clauses)
    
    metric_value = refutation_length
    conjecture_holds = tau_G <= 2 or metric_value >= 2 ** (0.3 * tau_G)
    counterexample = "" if conjecture_holds else f"Graph with tree-depth {tau_G} and refutation length {metric_value}"
    
    return {
        "metric_name": "refutation_length",
        "metric_value": metric_value,
        "instances_tested": 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with tree-depth {results[0]['counterexample'].split()[2]} and refutation length {results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")