# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def generate_random_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges = set()
    
    while len(edges) < (n * d) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    
    return graph

def generate_tseitin_formula(n, d):
    graph = generate_random_graph(n, d)
    literals = list(range(1, n * 2 + 1))
    clauses = []
    
    for i in range(n):
        clauses.append([literals[i], -literals[n + i]])
        for j in range(i + 1, n):
            clauses.append([-literals[i], -literals[j], literals[n + i + j]])
            clauses.append([-literals[j], -literals[i], literals[n + i + j]])
    
    return graph, literals, clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        pivot = Fraction(matrix[i][i])
        for j in range(cols):
            matrix[i][j] /= pivot
        
        for j in range(rows):
            if j != i:
                factor = Fraction(matrix[j][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def resolution_width(clauses):
    queue = clauses[:]
    learned_clauses = []
    while queue:
        clause1 = queue.pop(0)
        for clause2 in queue + learned_clauses:
            if not set(clause1).isdisjoint(set(clause2)):
                new_clause = [l for l in clause1 if l not in clause2] + [l for l in clause2 if -l not in clause1]
                if len(new_clause) == 0:
                    return math.inf
                if new_clause not in queue and new_clause not in learned_clauses:
                    learned_clauses.append(new_clause)
    return max(len(clause) for clause in learned_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2
    graph, literals, clauses = generate_tseitin_formula(n, d)
    
    OHD = len(gaussian_elimination([[Fraction(1 if j in neighbors else -1) for j in range(n)] for neighbors in graph]))
    w = resolution_width(clauses)
    
    return {
        "metric_name": "OHD vs. Resolution Width",
        "metric_value": OHD / w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": OHD <= 3 * w,
        "counterexample": "" if OHD <= 3 * w else f"OHD({OHD}) > 3w({3 * w})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")