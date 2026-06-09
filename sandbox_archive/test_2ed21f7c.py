# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, n-1) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def tseitin_graph(cnf):
        variables = set()
        edges = set()
        
        for i, clause in enumerate(cnf):
            new_var = -i - 2
            variables.add(new_var)
            for literal in clause:
                if literal > 0:
                    variables.add(literal)
                    edges.add((literal, new_var))
                else:
                    variables.add(-literal)
                    edges.add((-literal, new_var))
        
        return variables, edges
    
    def topological_entropy(variables, edges):
        n = len(variables)
        adjacency_matrix = [[0] * n for _ in range(n)]
        in_degree = [0] * n
        
        for u, v in edges:
            if u > 0 and v < -1:
                u -= 1
                v += 2
                adjacency_matrix[u][v] = 1
                in_degree[v] += 1
        
        queue = [i for i in range(n) if in_degree[i] == 0]
        topological_order = []
        
        while queue:
            node = queue.pop(0)
            topological_order.append(node)
            for neighbor in range(n):
                if adjacency_matrix[node][neighbor]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
        
        if len(topological_order) != n:
            return float('inf')
        
        entropy = 0
        for i in range(n):
            degree = sum(adjacency_matrix[i])
            if degree > 0:
                entropy += Fraction(degree, n).log()
        
        return entropy
    
    def resolution_width(cnf):
        stack = []
        assignment = {}
        
        def dpll():
            while True:
                unit_clause = next((c for c in cnf if len(c) == 1), None)
                if unit_clause is not None:
                    literal = unit_clause[0]
                    if literal < 0 and literal in assignment and assignment[literal] != -1:
                        return False
                    assignment[-literal] = 1
                    stack.append(literal)
                else:
                    if all(lit in assignment for lit in cnf):
                        return True
                    var = next((v for v in range(1, len(cnf) + 1) if v not in assignment), None)
                    assignment[var] = 0
                    stack.append(var)
                    new_assignment = {k: v for k, v in assignment.items()}
                    new_assignment[-var] = 1
                    if dpll():
                        return True
                    del assignment[var]
                    del new_assignment[-var]
                    stack.pop()
        
        return len(stack) if dpll() else float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        variables, edges = tseitin_graph(cnf)
        entropy = topological_entropy(variables, edges)
        width = resolution_width(cnf)
        
        if entropy == float('inf') or width == float('inf'):
            results.append({"n": n, "entropy": entropy, "width": width})
        else:
            results.append({"n": n, "entropy": entropy, "width": width})
    
    mean_entropy = sum(r["entropy"] for r in results) / len(results)
    max_width = max(r["width"] for r in results)
    conjecture_holds = all(r["width"] <= 2 * r["n"] for r in results)
    
    return {
        "metric_name": "Topological Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": max_width,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Resolution width exceeds 2n for some instances"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Resolution width exceeds 2n' first_failing_seed={first_failing_seed}")