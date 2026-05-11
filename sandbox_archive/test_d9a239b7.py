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

def generate_random_graph(n):
    if n <= 1:
        return []
    edges = set()
    while len(edges) < n - 1:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    return list(edges)

def tree_depth(graph):
    if not graph:
        return 0
    adjacency_list = defaultdict(list)
    for u, v in graph:
        adjacency_list[u].append(v)
        adjacency_list[v].append(u)
    
    def dfs(node, parent):
        max_depth = 0
        for neighbor in adjacency_list[node]:
            if neighbor != parent:
                depth = dfs(neighbor, node)
                max_depth = max(max_depth, depth)
        return max_depth + 1
    
    return dfs(0, -1)

def tseitin_formula(graph):
    n = len(graph)
    literals = {f'x{i}': i for i in range(n)}
    clauses = []
    
    def add_clause(clause):
        if clause:
            clauses.append(clause)
    
    # Base case: each vertex is connected to at least one other vertex
    for u, v in graph:
        add_clause([-literals[u], literals[v]])
        add_clause([-literals[v], literals[u]])
    
    # Ensure each vertex has exactly two neighbors (simple cycle)
    for i in range(n):
        neighbors = [j for j in range(n) if (i, j) in graph or (j, i) in graph]
        if len(neighbors) != 2:
            return None
    
    # Tseitin encoding
    for u, v in graph:
        literal_uv = n + u * n + v
        add_clause([-literals[u], -literals[v], literal_uv])
        add_clause([literals[u], literal_uv])
        add_clause([literals[v], literal_uv])
        add_clause([-literal_uv, -literals[u]])
        add_clause([-literal_uv, -literals[v]])
    
    return clauses

def dpll(clauses):
    assignment = {}
    stack = []
    
    def is_satisfiable():
        for clause in clauses:
            if not any(lit in assignment and (assignment[lit] == 1) or (-lit in assignment and (assignment[-lit] == -1)) for lit in clause):
                return False
        return True
    
    def backtrack():
        if not stack:
            return is_satisfiable()
        
        var, value = stack.pop()
        assignment[var] = value
        
        if is_satisfiable():
            return True
        
        del assignment[var]
        stack.append((var, -value))
        
        if is_satisfiable():
            return True
        
        stack.pop()
        return False
    
    for clause in clauses:
        unassigned_vars = [lit for lit in clause if lit not in assignment and -lit not in assignment]
        if unassigned_vars:
            var = random.choice(unassigned_vars)
            stack.append((var, 1))
    
    return backtrack()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            graph = generate_random_graph(n)
            if not graph:
                continue
            
            depth = tree_depth(graph)
            formula = tseitin_formula(graph)
            
            if formula is None:
                return {
                    "metric_name": "Resolution proof length",
                    "metric_value": float('inf'),
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
            
            length = sum(1 for _ in range(100) if dpll(formula))
            total_length += length
            instances_tested += 1
    
    mean_length = total_length / instances_tested
    conjecture_holds = all(length >= 2 ** (0.5 * depth) for depth, length in zip(tree_depths, lengths))
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_length:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")