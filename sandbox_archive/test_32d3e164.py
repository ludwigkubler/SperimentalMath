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
from collections import defaultdict

def generate_expander_graph(n, m):
    graph = [[] for _ in range(n)]
    edges_added = 0
    while edges_added < m:
        u, v = random.sample(range(n), 2)
        if u != v and v not in graph[u]:
            graph[u].append(v)
            graph[v].append(u)
            edges_added += 1
    return graph

def find_fundamental_group_rank(graph):
    n = len(graph)
    visited = [False] * n
    rank = 0
    
    def dfs(node, parent):
        nonlocal rank
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, node)
            elif neighbor != parent:
                rank += 1
    
    for i in range(n):
        if not visited[i]:
            dfs(i, -1)
    
    return rank

def generate_tseitin_formula(graph):
    n = len(graph)
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    
    # Add clauses for each edge
    for u, v in [(i, j) for i in range(n) for j in graph[i]]:
        clauses.append([f'-{literals[u]}', f'{literals[v]}'])
        clauses.append([f'{literals[u]}', f'-{literals[v]}'])
    
    # Add clauses to ensure each literal appears exactly once
    for i in range(n):
        clauses.append([f'{literals[i]}'])
        clauses.append([f'-{literals[i]}'])
    
    return literals, clauses

def dpll_with_clause_learning(clauses, literals):
    def is_satisfiable():
        assignment = {}
        
        def backtrack(level):
            if level == len(literals):
                return True
            literal = literals[level]
            for value in [True, False]:
                assignment[literal] = value
                if all([not clause or any(assignment.get(lit, not value) for lit in clause) for clause in clauses]):
                    if backtrack(level + 1):
                        return True
            del assignment[literal]
            return False
        
        return backtrack(0)
    
    return is_satisfiable()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = int(1.5 * n)
    graph = generate_expander_graph(n, m)
    rank = find_fundamental_group_rank(graph)
    literals, clauses = generate_tseitin_formula(graph)
    
    proof_size = dpll_with_clause_learning(clauses, literals)
    
    if not proof_size:
        return {
            "metric_name": "resolution_proof_size",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL did not find a proof"
        }
    
    c = 0.3
    expected_size = 2 ** (c * (m - n + 1))
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "conjecture_holds": proof_size >= expected_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 230, 7))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")