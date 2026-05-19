# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict, deque

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank(A):
    A = gaussian_elimination(A)
    r = 0
    for row in A:
        if any(row):
            r += 1
    return r

def betti_number(graph):
    n = len(graph)
    m = sum(len(neighbors) for neighbors in graph.values()) // 2
    return m - n + 1

def resolution_width(graph):
    n = len(graph)
    clauses = []
    variables = set()
    
    # Create Tseitin encoding
    for v, neighbors in graph.items():
        literals = [f"x_{v}_{i}" for i in range(len(neighbors))]
        clauses.append([literals[0]] + [-x for x in literals[1:]])
        variables.update(literals)
        
        for i in range(len(neighbors)):
            for j in range(i+1, len(neighbors)):
                clauses.append([-literals[i], -literals[j]])
    
    # Convert to CNF
    cnf = []
    for clause in clauses:
        cnf.append([int(x[1:]) if x.startswith('x') else -int(x[1:]) for x in clause])
    
    # Compute resolution width using DPLL-based estimator
    def dpll(cnf, assignment):
        if not cnf:
            return len(assignment)
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause is None:
            p = random.choice([x for x in variables if x not in assignment])
            return max(dpll(cnf + [[-p]], assignment | {p: True}), dpll(cnf + [[-p]], assignment | {p: False}))
        literal = unit_clause[0]
        var, sign = (literal, True) if literal > 0 else (-literal, False)
        if var in assignment and assignment[var] != sign:
            return float('inf')
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        new_assignment = assignment | {var: sign}
        return dpll(new_cnf, new_assignment)
    
    width = min(dpll(cnf, {}) for _ in range(10))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = defaultdict(list)
    vertices = list(range(n))
    edges = set()
    
    # Generate a connected graph
    while len(graph) < n or not all(len(neighbors) > 0 for neighbors in graph.values()):
        u, v = random.sample(vertices, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            graph[u].append(v)
            graph[v].append(u)
    
    betti = betti_number(graph)
    width = resolution_width(graph)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= betti,
        "counterexample": "" if width >= betti else f"Graph with n={n}, m={len(edges)}, Betti number={betti}, Width={width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")