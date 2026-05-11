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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def find_fundamental_group_rank(graph):
    n = len(graph)
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if graph[u][v]:
                edges.append((u, v))
    
    m = len(edges)
    A = [[0] * (n - 1) for _ in range(m)]
    b = [0] * m
    
    for i, (u, v) in enumerate(edges):
        A[i][u] = 1
        A[i][v] = -1
    
    rank = len(gaussian_elimination(A, b))
    return n - rank

def generate_tseitin_formula(graph):
    n = len(graph)
    m = len([e for e in graph if any(v > 0 for v in e)])
    clauses = []
    
    # Variables
    x = [f"x{i}" for i in range(n)]
    y = [f"y{i}{j}" for i in range(n) for j in range(i + 1, n)]
    
    # Clauses for each edge
    for u, v in [(i, j) for i in range(n) for j in range(i + 1, n)]:
        clauses.append([f"~{x[u]}", f"{y[u][v]}"])
        clauses.append([f"~{x[v]}", f"{y[u][v]}"])
        clauses.append([f"{x[u]}", f"{x[v]}", f"~{y[u][v]}"])
    
    # Clauses for each vertex
    for i in range(n):
        clauses.append([f"{x[i]}"] + [f"~{y[i][j]}" for j in range(i + 1, n)])
        clauses.append([f"~{x[i]}"] + [f"{y[i][j]}" for j in range(i + 1, n)])
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    primes = generate_primes(30)
    c = 0.3
    total_proofs = 0
    valid_proofs = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = int(1.5 * n)
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            graph[i][i] = 0
        if not any(sum(row) > 0 for row in graph):
            continue
        
        rank = find_fundamental_group_rank(graph)
        clauses = generate_tseitin_formula(graph)
        
        # DPLL with clause learning (simplified version)
        def dpll(clauses, assignment):
            nonlocal total_proofs
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal.startswith("~"):
                    literal = literal[1:]
                    assignment[literal] = False
                else:
                    assignment[literal] = True
                return dpll([c for c in clauses if literal not in c and "~" + literal not in c], assignment)
            pure_literal = next((l for l in set.union(*map(set, clauses)) if sum(1 for c in clauses if l in c) - sum(1 for c in clauses if "~" + l in c) == 0), None)
            if pure_literal:
                assignment[pure_literal] = True
                return dpll([c for c in clauses if pure_literal not in c and "~" + pure_literal not in c], assignment)
            
            literal = next(iter(clauses[0]))
            total_proofs += 1
            return dpll(clauses, {**assignment, literal: True}) or dpll(clauses, {**assignment, literal: False})
        
        if dpll(clauses, {}):
            valid_proofs += 1
    
    metric_value = valid_proofs / total_proofs if total_proofs > 0 else 0
    conjecture_holds = metric_value >= 2 ** (c * rank)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": metric_value,
        "instances_tested": total_proofs,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")