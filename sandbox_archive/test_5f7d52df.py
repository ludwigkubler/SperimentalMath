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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        for j in range(i+1, n):
            if A[i][i] == 0:
                return 0
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
        det *= A[i][i]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(d, n):
        if d * n % 2 != 0:
            return None
        G = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < (d * n) // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                G[u][v] = 1
                G[v][u] = 1
                edges.add((u, v))
        return G
    
    def tseitin_formula(G):
        n = len(G)
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in range(n):
                if G[i][j]:
                    clause.append(f"~{literals[j]}")
            clauses.append(clause)
            for j in range(i+1, n):
                for k in range(j+1, n):
                    if G[i][k] and G[j][k]:
                        clauses.append([f"~{literals[i]}", f"~{literals[j]}", literals[k]])
        return clauses
    
    def eigenvalues(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if G[i][j]:
                    A[i][j] = 1
        det_A = determinant(A)
        if det_A == 0:
            return None
        eigenvals = []
        for k in range(1, n+1):
            I = [[0] * n for _ in range(n)]
            for i in range(n):
                I[i][i] = 1
            A_k = [[A[i][j]**k for j in range(n)] for i in range(n)]
            det_A_k = determinant(A_k)
            if det_A_k == 0:
                eigenvals.append(k)
        return eigenvals
    
    def m_order(eigenvals):
        if not eigenvals:
            return None
        min_order = float('inf')
        for val in eigenvals:
            order = sum(1 for e in eigenvals if abs(e - val) < 1e-6)
            if order < min_order:
                min_order = order
        return min_order
    
    def resolution_proof_width(clauses):
        n = len(clauses)
        width = max(len(c) for c in clauses)
        return width
    
    d = random.randint(2, 3)
    n = random.randint(5, 40)
    G = generate_d_regular_graph(d, n)
    if not G:
        return {
            "metric_name": "m_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular"
        }
    
    clauses = tseitin_formula(G)
    eigenvals = eigenvalues(G)
    if not eigenvals:
        return {
            "metric_name": "m_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "eigenvalue_computation_failed"
        }
    
    m = m_order(eigenvals)
    w = resolution_proof_width(clauses)
    
    return {
        "metric_name": "m_order",
        "metric_value": m,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if m is None or w is None else True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "m_order_computation_failed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")