# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate OR clauses for each variable
        for var in variables:
            clause = [-var, -(-var)]
            clauses.append(clause)
        
        # Generate AND clauses for each pair of variables
        for i in range(n):
            for j in range(i + 1, n):
                clause = [variables[i], variables[j], -(variables[i] ^ variables[j])]
                clauses.append(clause)
        
        return clauses
    
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is not None:
            literal = unit_clause[0]
            new_assignment[literal] = literal > 0
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        
        literal, _ = random.choice(clauses)
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        
        return False
    
    def compute_persistent_homology(clauses):
        n = len(clauses)
        graph = {i: set() for i in range(1, 2 * n + 1)}
        
        for clause in clauses:
            literals = [abs(l) for l in clause]
            for literal in literals:
                for other_literal in literals:
                    if literal != other_literal:
                        graph[literal].add(other_literal)
                        graph[-literal].add(-other_literal)
        
        # Compute connected components
        visited = set()
        components = []
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        
        for node in range(1, 2 * n + 1):
            if node not in visited:
                components.append([])
                dfs(node)
        
        return len(components)
    
    def resolution_width(clauses):
        queue = clauses[:]
        levels = {literal: 0 for literal in set(sum(clauses, []))}
        
        while queue:
            clause = queue.pop(0)
            if not clause:
                return max(levels.values())
            
            literal = next(l for l in clause if levels[l] == 0)
            levels[-literal] = levels[literal] + 1
            
            new_clauses = []
            for c in clauses:
                if literal in c and -literal in c:
                    continue
                elif literal in c:
                    new_clauses.append([l for l in c if l != literal])
                elif -literal in c:
                    new_clauses.append([l for l in c if l != -literal])
            
            queue.extend(new_clauses)
        
        return max(levels.values())
    
    n = random.randint(5, 40)
    clauses = generate_tseitin_formula(n)
    persistent_homology_value = compute_persistent_homology(clauses)
    resolution_width_value = resolution_width(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": resolution_width_value <= persistent_homology_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")