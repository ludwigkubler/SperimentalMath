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

def generate_d_regular_graph(n, d):
    if (d * n) % 2 != 0:
        raise ValueError("d * n must be even")
    
    G = [[0] * n for _ in range(n)]
    edges_added = 0
    
    while edges_added < (d * n) // 2:
        u, v = random.sample(range(n), 2)
        if G[u][v] == 0 and u != v:
            G[u][v] = 1
            G[v][u] = 1
            edges_added += 1
    
    return G

def compute_eigenvalues(G):
    n = len(G)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    def matrix_multiply(A, B):
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_add(A, B):
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    
    def scalar_multiply(s, A):
        return [[s * A[i][j] for j in range(n)] for i in range(n)]
    
    def matrix_trace(A):
        return sum(A[i][i] for i in range(n))
    
    def characteristic_polynomial(G):
        x = 1
        n = len(G)
        while x <= n:
            G_x = scalar_multiply(-x, I)
            G_x = matrix_add(G_x, G)
            det = determinant(G_x)
            yield det * math.pow(x, n - x)
            x += 1
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        
        det = 0
        for j in range(len(A)):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    eigenvalues = []
    for p in characteristic_polynomial(G):
        roots = find_roots(p, len(eigenvalues))
        eigenvalues.extend(roots)
    
    return eigenvalues

def find_roots(poly, degree):
    if degree == 1:
        return [-poly[0] / poly[1]]
    
    roots = []
    for i in range(degree):
        a = poly[i]
        b = sum(poly[j] * (-i) ** (j - i) for j in range(i + 1, degree))
        c = sum(poly[j] * (-i) ** (j - i) for j in range(i + 2, degree))
        
        discriminant = b**2 - 4*a*c
        if discriminant >= 0:
            root1 = (-b + math.sqrt(discriminant)) / (2*a)
            root2 = (-b - math.sqrt(discriminant)) / (2*a)
            roots.extend([root1, root2])
        else:
            real_part = -b / (2*a)
            imaginary_part = math.sqrt(-discriminant) / (2*a)
            roots.extend([real_part + imaginary_part * 1j, real_part - imaginary_part * 1j])
    
    return roots

def tseitin_formula(G):
    n = len(G)
    literals = [f"x{i}" for i in range(n)]
    clauses = []
    
    for i in range(n):
        clause = [literals[i]]
        for j in range(i + 1, n):
            if G[i][j] == 1:
                clause.append(f"~{literals[j]}")
        clauses.append(clause)
    
    return literals, clauses

def resolution_width(clauses):
    queue = clauses[:]
    resolvents = set()
    width = 0
    
    while queue:
        literal_count = max(len(c) for c in queue if isinstance(c, list))
        if literal_count > width:
            width = literal_count
        
        unit_clause = next((c for c in queue if len(c) == 1), None)
        if unit_clause is None:
            break
        
        literal = unit_clause[0]
        queue.remove(unit_clause)
        
        for clause in queue:
            if isinstance(clause, list):
                if literal in clause:
                    new_clause = [l for l in clause if l != literal and l != f"~{literal}"]
                    if not new_clause:
                        return math.inf
                    resolvents.add(tuple(sorted(new_clause)))
                    queue.append(new_clause)
                elif f"~{literal}" in clause:
                    new_clause = [l for l in clause if l != f"~{literal}" and l != literal]
                    if not new_clause:
                        return math.inf
                    resolvents.add(tuple(sorted(new_clause)))
                    queue.append(new_clause)
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 3
    
    G = generate_d_regular_graph(n, d)
    eigenvalues = compute_eigenvalues(G)
    m_order = max(abs(e) for e in eigenvalues)
    
    literals, clauses = tseitin_formula(G)
    w = resolution_width(clauses)
    
    if math.isnan(w):
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    correlation_coefficient = (m_order * w) / (m_order**2 + w**2)
    r_squared = correlation_coefficient ** 2
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8 and r_squared >= 0.9,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")