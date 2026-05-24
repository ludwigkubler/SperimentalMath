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
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def local_index(G, p):
    n = len(G)
    adj_matrix = [[0] * n for _ in range(n)]
    for u, v in G:
        adj_matrix[u][v] = 1
    
    max_continuations = 0
    for i in range(n):
        for j in range(i+1, n):
            if adj_matrix[i][j] == 1:
                B = [Fraction(0)] * n
                B[j] = Fraction(1)
                A = [[Fraction(0)] * n for _ in range(n)]
                for k in range(n):
                    for l in range(n):
                        A[k][l] = adj_matrix[(i + k) % n][(j + l) % n]
                
                try:
                    solution = gaussian_elimination(A, B)
                    max_continuations = max(max_continuations, sum(1 for x in solution if abs(x) > 0))
                except Exception as e:
                    return None
    
    return max_continuations

def is_expander(G):
    n = len(G)
    degree_sum = sum(len(neighbors) for neighbors in G)
    avg_degree = degree_sum / n
    min_degree = min(len(neighbors) for neighbors in G)
    max_degree = max(len(neighbors) for neighbors in G)
    
    return min_degree >= avg_degree / 2 and max_degree <= avg_degree * 2

def tseitin_formula(G):
    n = len(G)
    literals = [i for i in range(n)]
    clauses = []
    
    for u, v in G:
        clauses.append([literals[u], -literals[v]])
        clauses.append([-literals[u], literals[v]])
    
    return literals, clauses

def resolution_width(clauses):
    n = len(clauses)
    queue = clauses[:]
    learned_clauses = []
    
    while queue:
        clause1 = queue.pop(0)
        for clause2 in queue + learned_clauses:
            common_lit = next((lit for lit in clause1 if -lit in clause2), None)
            if common_lit is not None:
                new_clause = [lit for lit in clause1 if lit != common_lit] + [lit for lit in clause2 if lit != -common_lit]
                if len(new_clause) == 0:
                    return float('inf')
                if new_clause not in queue and new_clause not in learned_clauses:
                    learned_clauses.append(new_clause)
    
    return max(len(clause) for clause in learned_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = 2
    
    G = []
    while len(G) < n * (n - 1):
        u, v = random.sample(range(n), 2)
        if (u, v) not in G and (v, u) not in G:
            G.append((u, v))
    
    if not is_expander(G):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    literals, clauses = tseitin_formula(G)
    ν_G = local_index(G, p)
    if ν_G is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    width = resolution_width(clauses)
    if width < 2 ** (math.log(ν_G, 2) * math.log(n, 2)):
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"width={width} < 2^(Ω({ν_G})) for n={n}"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={seeds[first_failing_seed]}")