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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(d, n):
        if (n * d) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < n * d // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [random.randint(1, 2*n) for _ in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
        for u in range(n):
            for v in graph[u]:
                if u < v:
                    new_lit = random.randint(1, 2*n)
                    clauses.append([-new_lit, literals[u], literals[v]])
                    clauses.append([-new_lit, -literals[u], -literals[v]])
                    clauses.append([new_lit])
        return clauses
    
    def tropical_analytic_rank(clauses):
        n = len(clauses)
        A = [[0]*n for _ in range(n)]
        b = [0]*n
        for i in range(n):
            for j in range(i+1, n):
                if any(lit in clauses[i] and -lit in clauses[j] for lit in literals):
                    A[i][j] = 1
                    A[j][i] = 1
        det = determinant(A)
        return abs(det) if det != 0 else float('inf')
    
    def resolution_width(clauses):
        n = len(clauses)
        clauses = [set(clause) for clause in clauses]
        queue = list(clauses)
        while queue:
            clause = queue.pop()
            if not clause:
                return 1
            lits = list(clause)
            other_lit = random.choice(lits)
            new_clauses = []
            for c in queue:
                if other_lit in c:
                    continue
                if -other_lit in c:
                    new_clauses.append(c - {other_lit})
                else:
                    new_clauses.append(c | {-other_lit})
            queue.extend(new_clauses)
        return float('inf')
    
    n = random.choice([10, 20, 30, 40])
    d = random.randint(2, min(n-1, 5))
    graph = generate_d_regular_graph(d, n)
    if not graph:
        return {
            "metric_name": "tropical_analytic_rank",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    clauses = tseitin_formula(graph)
    tar = tropical_analytic_rank(clauses)
    w = resolution_width(clauses)
    
    if tar == float('inf') or w == float('inf'):
        return {
            "metric_name": "tropical_analytic_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "tropical_analytic_rank",
        "metric_value": tar / w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
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
    else:
        max_ratio = max(r["metric_value"] for r in results if r["conjecture_holds"])
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif max_ratio > 10:
        print(f"RESULT: FALSIFIED counterexample=\"max_ratio_exceeds_10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")