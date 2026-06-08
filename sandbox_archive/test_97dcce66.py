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
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] + factor * A[i][k] for k in range(i, n)]
            b[j] += factor * b[i]

    # Back-substitute
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def dpll(clauses, assignment={}):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            return False

    literal = next(l for l in range(1, max(max(abs(c) for c in clause) for clause in clauses)) + 1 if l not in assignment)
    new_assignment_true = assignment.copy()
    new_assignment_true[literal] = True
    if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment_true):
        return True

    new_assignment_false = assignment.copy()
    new_assignment_false[literal] = False
    if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment_false):
        return True

    return False

def generate_d_regular_graph(n, d):
    graph = [[] for _ in range(n)]
    degree_count = [0] * n
    edges_added = 0
    
    while edges_added < (n * d) // 2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and v not in graph[u]:
            graph[u].append(v)
            graph[v].append(u)
            degree_count[u] += 1
            degree_count[v] += 1
            edges_added += 1
    
    return graph

def tseitin_formula(graph, n):
    literals = list(range(1, n+1))
    clauses = []
    
    for i in range(n):
        for j in range(i+1, n):
            if (i, j) not in graph and (j, i) not in graph:
                clauses.append([-literals[i], -literals[j]])
                clauses.append([literals[i], literals[j]])
                clauses.append([-literals[i], literals[j]])
                clauses.append([literals[i], -literals[j]])
            else:
                clauses.append([literals[i], literals[j]])
    
    return clauses

def minimal_tropical_motivic_rank(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    b = [0] * n
    
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                A[i][literal - 1] += 1
            else:
                A[i][-1] -= 1
    
    x = gaussian_elimination(A, b)
    return max(abs(x[i]) for i in range(n))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.randint(2, min(n-1, 3))
    
    graph = generate_d_regular_graph(n, d)
    clauses = tseitin_formula(graph, n)
    
    mtr_G = minimal_tropical_motivic_rank(clauses)
    w_phi_G = Fraction(dpll(clauses), 1) if dpll(clauses) else float('inf')
    
    return {
        "metric_name": "mtr(G)/w(φ_G)",
        "metric_value": mtr_G / w_phi_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mtr_G / w_phi_G >= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")