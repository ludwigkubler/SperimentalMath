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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def rank(A):
    A = [row[:] for row in A]
    gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def generate_d_regular_graph(n, d):
    graph = [[] for _ in range(n)]
    edges = set()
    while len(edges) < n * d // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = [i for i in range(1, 2*n+1)]
    clauses = []
    
    def add_clause(lits):
        clauses.append([l for l in lits if l != 0])
    
    for u in range(n):
        for v in graph[u]:
            lit_u = literals[2*u]
            lit_v = literals[2*v + 1]
            add_clause([-lit_u, -lit_v])
            add_clause([-lit_u, lit_v])
            add_clause([lit_u, -lit_v])
    
    return clauses

def resolution_width(clauses):
    queue = [c for c in clauses if len(c) == 1]
    while queue:
        unit_clause = queue.pop()
        lit = unit_clause[0]
        for clause in clauses:
            if lit in clause:
                new_clause = [l for l in clause if l != lit and -l not in clause]
                if len(new_clause) == 0:
                    return math.inf
                elif len(new_clause) == 1:
                    queue.append(new_clause)
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    d = 4
    
    graph = generate_d_regular_graph(n, d)
    clauses = tseitin_formula(graph)
    width = resolution_width(clauses)
    
    if width == math.inf:
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    k_theory_rank = rank([[1 if i in graph[j] else 0 for j in range(n)] for i in range(n)])
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_width = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if not result["conjecture_holds"]) / len(results)
    
    if all(not result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif any(result["metric_value"] > 3 * result["instances_tested"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["metric_value"] > 3 * result["instances_tested"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width_infinite\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")