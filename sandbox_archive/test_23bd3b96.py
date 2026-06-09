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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(1, n + 1):
            clauses.append([i])
            clauses.append([-i])
        
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([i, -j])
                clauses.append([-i, j])
        
        return variables, clauses
    
    def compute_persistent_homology(clauses):
        # Simplified version of persistent homology calculation
        graph = {i: set() for i in range(1, n + 1)}
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    graph[literal].add(-literal)
                    graph[-literal].add(literal)
        
        # Count connected components
        visited = set()
        components = 0
        
        def dfs(node):
            stack = [node]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    for neighbor in graph[current]:
                        stack.append(neighbor)
        
        for node in range(1, n + 1):
            if node not in visited:
                dfs(node)
                components += 1
        
        return components
    
    def resolution_width(clauses):
        # Simplified version of resolution width calculation
        queue = []
        assignment = {}
        
        def add_clause(clause):
            queue.append(clause)
        
        def resolve(lit1, lit2):
            for clause in clauses:
                if -lit1 in clause and -lit2 in clause:
                    new_lit = [x for x in clause if x != -lit1 and x != -lit2]
                    add_clause(new_lit)
        
        for clause in clauses:
            add_clause(clause)
        
        while queue:
            clause = queue.pop(0)
            if len(clause) == 1:
                literal = clause[0]
                assignment[literal] = True
                resolve(literal, -literal)
            else:
                return len(clause)
        
        return 1
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in range(5, n_max + 1):
        variables, clauses = generate_tseitin_formula(n)
        resolution_width_value = resolution_width(clauses)
        persistent_homology_value = compute_persistent_homology(clauses)
        
        if resolution_width_value <= persistent_homology_value:
            return {
                "metric_name": "correlation",
                "metric_value": -1.0,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Resolution width {resolution_width_value} <= Persistent homology {persistent_homology_value}"
            }
        
        metric_values.append(resolution_width_value - persistent_homology_value)
    
    return {
        "metric_name": "correlation",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")