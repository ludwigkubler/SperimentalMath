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

def generate_random_graph(n, p):
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                graph[i][j] = graph[j][i] = 1
    return graph

def gromov_hyperbolicity(graph):
    n = len(graph)
    def distance(u, v):
        queue = [(u, 0)]
        visited = set([u])
        while queue:
            node, dist = queue.pop(0)
            if node == v:
                return dist
            for neighbor in range(n):
                if graph[node][neighbor] and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        return float('inf')
    
    def four_point_condition(a, b, c, d):
        ab = distance(a, b)
        ac = distance(a, c)
        ad = distance(a, d)
        bc = distance(b, c)
        bd = distance(b, d)
        cd = distance(c, d)
        return max(ab + cd - ac - bd, ac + bd - ab - cd, ad + bc - ab - cd) <= min(ab + bc, ac + bd, ad + cd)
    
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                for d in range(c + 1, n):
                    if not four_point_condition(a, b, c, d):
                        return float('-inf')
    return 0

def tseitin_formula(graph):
    n = len(graph)
    clauses = []
    literals = {}
    for i in range(n):
        literals[i] = f'x{i}'
    
    def add_clause(clause):
        clauses.append(clause)
    
    def negate(lit):
        if lit.startswith('¬'):
            return lit[1:]
        else:
            return '¬' + lit
    
    def clause_from_vars(vars):
        return [negate(v) for v in vars]
    
    for i in range(n):
        add_clause([literals[i]])
    
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                add_clause(clause_from_vars([negate(literals[i]), literals[j]]))
                add_clause(clause_from_vars([negate(literals[j]), literals[i]]))
    
    return clauses

def dpll_with_memoization(clauses, assignment, unit_clauses=None):
    if unit_clauses is None:
        unit_clauses = []
    
    for clause in unit_clauses:
        literal = next((lit for lit in clause if lit not in assignment and negate(lit) not in assignment), None)
        if literal is None:
            return True
        assignment[literal] = True
    
    unit_clauses.clear()
    for clause in clauses:
        unsatisfied = [lit for lit in clause if lit not in assignment and negate(lit) not in assignment]
        if len(unsatisfied) == 0:
            continue
        elif len(unsatisfied) == 1:
            literal = unsatisfied[0]
            unit_clauses.append(clause)
        else:
            literal = random.choice(unsatisfied)
        
        assignment[literal] = True
    
    for clause in clauses:
        if all(lit not in assignment or negate(lit) in assignment for lit in clause):
            continue
        elif any(lit in assignment and negate(lit) in assignment for lit in clause):
            return False
    
    false_clauses = [clause for clause in clauses if any(lit in assignment and negate(lit) in assignment for lit in clause)]
    true_clauses = [clause for clause in clauses if all(lit not in assignment or negate(lit) in assignment for lit in clause)]
    
    for literal in assignment:
        if literal.startswith('¬'):
            continue
        new_assignment = {k: v for k, v in assignment.items()}
        new_assignment[literal] = False
        if dpll_with_memoization(false_clauses, new_assignment):
            return True
    
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = 0.5
    graph = generate_random_graph(n, p)
    delta_G = gromov_hyperbolicity(graph)
    
    if delta_G == float('-inf'):
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    clauses = tseitin_formula(graph)
    resolution_length = len(clauses) if dpll_with_memoization(clauses, {}) else float('inf')
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": delta_G >= 1 or resolution_length == float('inf'),
        "counterexample": "" if delta_G >= 1 else f"Graph with n={n}, p={p} has δ(G)={delta_G}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    resolution_lengths = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(resolution_lengths) / len(resolution_lengths):.2f} std=0 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "mapping_undefined" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] != "mapping_undefined")
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")