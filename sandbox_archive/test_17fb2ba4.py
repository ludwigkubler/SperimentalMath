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

def generate_tseitin_formula(n: int, m: int) -> tuple:
    variables = list(range(1, n + 1))
    clauses = []
    
    def new_variable():
        return n + len(clauses) + 1
    
    for _ in range(m):
        a = random.choice(variables)
        b = random.choice(variables)
        op = random.choice(['AND', 'OR'])
        clause = (a, b, op)
        clauses.append(clause)
    
    # Add Tseitin axioms
    tseitin_axioms = []
    for i in range(m):
        v = new_variable()
        tseitin_axioms.extend([(v, a, 'EQ'), (v, b, 'EQ')])
        tseitin_axioms.append((v, i + 1, 'NEQ'))
    
    clauses.extend(tseitin_axioms)
    
    return variables, clauses

def generate_graph_from_formula(variables: list, clauses: list) -> dict:
    graph = {}
    for v in variables:
        graph[v] = set()
    for a, b, op in clauses:
        if op == 'AND':
            graph[a].add(b)
            graph[b].add(a)
        elif op == 'OR':
            graph[a].add(b)
            graph[b].add(a)
    return graph

def compute_local_zeta_function_rank(graph: dict) -> int:
    n = len(graph)
    zeta_matrix = [[0] * n for _ in range(n)]
    
    def dfs(node, visited):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph[node]:
            dfs(neighbor, visited)
            zeta_matrix[node][neighbor] += 1
    
    for i in range(n):
        dfs(i, set())
    
    rank = 0
    for row in zeta_matrix:
        if any(row):
            rank += 1
    
    return rank

def dpll(clauses: list) -> bool:
    def solve(assignment):
        if not clauses:
            return True
        clause = next(c for c in clauses if any(var in assignment and assignment[var] == val for var, val in c))
        pos_var = next((var for var, val in clause if var not in assignment), None)
        neg_var = next((var for var, val in clause if var in assignment and assignment[var] != val), None)
        
        if pos_var is not None:
            assignment[pos_var] = True
            if solve(assignment):
                return True
            del assignment[pos_var]
        
        if neg_var is not None:
            assignment[neg_var] = False
            if solve(assignment):
                return True
            del assignment[neg_var]
        
        return False
    
    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n, 2 * n)
        graph = generate_graph_from_formula(variables, clauses)
        zeta_rank = compute_local_zeta_function_rank(graph)
        
        if not clauses:
            continue
        
        assignment = {}
        for var in variables:
            assignment[var] = random.choice([True, False])
        
        width = 1
        while True:
            if dpll(clauses):
                break
            width += 1
    
        results.append({
            "n": n,
            "zeta_rank": zeta_rank,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((r["zeta_rank"] - mean_zeta) * (r["width"] - mean_width) for r in results) / len(results)
    mean_zeta = sum(r["zeta_rank"] for r in results) / len(results)
    mean_width = sum(r["width"] for r in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation > 0.8,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")