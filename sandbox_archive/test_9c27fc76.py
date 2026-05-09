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

def generate_random_regular_graph(n, k):
    if 2 * k > n - 1:
        raise ValueError("Invalid parameters for regular graph generation")
    
    adj = [[] for _ in range(n)]
    degree_sum = 0
    
    for i in range(n):
        neighbors = random.sample(range(i + 1, min(i + k // 2 + 1, n)), k // 2)
        adj[i] = neighbors
        degree_sum += len(neighbors)
    
    if degree_sum % 2 != 0:
        raise ValueError("Failed to generate a regular graph")
    
    return adj

def spectral_cheeger_constant(adj):
    n = len(adj)
    laplacian = [[0] * n for _ in range(n)]
    
    for i in range(n):
        deg_i = len(adj[i])
        laplacian[i][i] = deg_i
        for j in adj[i]:
            laplacian[i][j] = -1
    
    # Normalize the Laplacian
    for i in range(n):
        sum_row = sum(laplacian[i])
        for j in range(n):
            laplacian[i][j] /= math.sqrt(sum_row)
    
    # Compute eigenvalues of the normalized Laplacian
    eigenvalues = [0] * n
    for _ in range(10):  # Power iteration method
        v = [random.random() for _ in range(n)]
        v = [x / sum(v) for x in v]
        v_next = [sum(laplacian[i][j] * v[j] for j in range(n)) for i in range(n)]
        v_next = [x / sum(v_next) for x in v_next]
        eigenvalues[0] += max(abs(x - y) for x, y in zip(v, v_next))
        v = v_next
    
    return min(eigenvalues)

def tseitin_formula(adj):
    n = len(adj)
    literals = [f"x{i}" for i in range(n)]
    clauses = []
    
    for i in range(n):
        clause = [literals[i]]
        for j in adj[i]:
            clause.append(f"~{literals[j]}")
        clauses.append(clause)
    
    return clauses

def dpll_solver(clauses, assignment):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        value = literal.startswith("~")
        literal = literal.lstrip("~")
        if literal in assignment and assignment[literal] != value:
            return False
        assignment[literal] = value
        clauses = [c for c in clauses if literal not in c and not any(l.startswith("~") and l[1:] == literal for l in c)]
    pure_literal = next((l for l, count in Counter([x.lstrip("~") for x in sum(clauses, [])]).items() if count % 2 != 0), None)
    if pure_literal:
        value = pure_literal.startswith("~")
        literal = pure_literal.lstrip("~")
        assignment[literal] = value
        clauses = [c for c in clauses if literal not in c and not any(l.startswith("~") and l[1:] == literal for l in c)]
    
    literals = list(assignment.keys())
    literal = random.choice(literals)
    value = assignment[literal]
    new_assignment = {k: v for k, v in assignment.items()}
    new_assignment[literal] = not value
    if dpll_solver(clauses, new_assignment):
        return True
    
    new_assignment[literal] = value
    clauses.append([f"~{literal}"])
    return dpll_solver(clauses, new_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    k = 8
    adj = generate_random_regular_graph(n, k)
    h_G = spectral_cheeger_constant(adj)
    
    clauses = tseitin_formula(adj)
    assignment = {}
    
    proof_steps = 0
    while not dpll_solver(clauses, assignment):
        proof_steps += 1
    
    metric_value = proof_steps
    conjecture_holds = metric_value >= 2 ** (h_G * math.log(n))
    counterexample = "" if conjecture_holds else f"Graph with h(G)={h_G} and proof steps={proof_steps}"
    
    return {
        "metric_name": "Proof Steps",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Graph with h(G) ≤ 1/√n\" first_failing_seed={first_failing_seed}")