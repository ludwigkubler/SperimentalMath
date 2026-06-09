# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        
        # Generate clauses for each variable
        for var in variables:
            clause = [var]
            neg_clause = [-var]
            clauses.append(clause)
            clauses.append(neg_clause)
            
            # Generate clauses for each pair of literals
            for other_var in variables:
                if var != other_var:
                    clause = [var, -other_var]
                    neg_clause = [-var, other_var]
                    clauses.append(clause)
                    clauses.append(neg_clause)
        
        return clauses
    
    def dpll(clauses):
        assignment = {}
        stack = []
        
        def backtrack():
            if not stack:
                return True
            literal = stack.pop()
            var = abs(literal)
            if literal in assignment:
                continue
            
            # Try assigning True to the variable
            assignment[var] = 1
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if backtrack():
                return True
            del assignment[var]
            
            # Try assigning False to the variable
            assignment[var] = -1
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if backtrack():
                return True
            del assignment[var]
            
            stack.append(literal)
            return False
        
        for clause in clauses:
            if len(clause) == 0:
                return False
            stack.append(clause[0])
        
        return backtrack()
    
    def compute_persistent_homology(clauses):
        graph = defaultdict(set)
        
        for literal, other_literal in combinations(range(-40, 41), 2):
            if literal != -other_literal and (literal, other_literal) not in clauses:
                graph[literal].add(other_literal)
                graph[other_literal].add(literal)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        
        visited = set()
        connected_components = 0
        
        for literal in range(-40, 41):
            if literal not in visited:
                dfs(literal, visited)
                connected_components += 1
        
        return connected_components
    
    def resolution_width(clauses):
        queue = clauses[:]
        width = 0
        
        while queue:
            new_clause = []
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause.extend([l for l in clause1 if l not in clause2] + [l for l in clause2 if l not in clause1])
                        new_clause = list(set(new_clause))
            
            if len(new_clause) > width:
                width = len(new_clause)
            
            queue.append(new_clause)
        
        return width
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_tseitin_formula(n)
    
    persistent_homology_value = compute_persistent_homology(clauses)
    resolution_width_value = resolution_width(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": persistent_homology_value >= resolution_width_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")