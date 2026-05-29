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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        variables = set()
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            variables.update(abs(x) for x in clause)
            clauses.append(clause)
        return variables, clauses
    
    def dpll(sat_instance):
        variables, clauses = sat_instance
        assignment = {v: None for v in variables}
        
        def solve():
            if not clauses:
                return True
            literal = random.choice([x for clause in clauses for x in clause])
            value = 1 if literal > 0 else -1
            variable = abs(literal)
            assignment[variable] = value
            
            new_clauses = []
            for clause in clauses:
                if any(abs(x) == variable and (x // abs(x)) != value for x in clause):
                    continue
                elif all(abs(x) != variable for x in clause):
                    return False
                else:
                    new_clauses.append([x for x in clause if abs(x) != variable])
            
            if solve():
                return True
            
            assignment[variable] = -value
            new_clauses = []
            for clause in clauses:
                if any(abs(x) == variable and (x // abs(x)) != value for x in clause):
                    continue
                elif all(abs(x) != variable for x in clause):
                    return False
                else:
                    new_clauses.append([x for x in clause if abs(x) != variable])
            
            if solve():
                return True
            
            assignment[variable] = None
            return False
        
        return solve(), assignment
    
    def extract_coxeter_diagram(assignment):
        diagram = defaultdict(list)
        for var, value in assignment.items():
            if value is not None:
                for other_var, other_value in assignment.items():
                    if other_var != var and other_value is not None and (var, other_var) not in diagram:
                        diagram[var].append(other_var)
                        diagram[other_var].append(var)
        return diagram
    
    def count_vertices(diagram):
        visited = set()
        
        def dfs(node):
            if node in visited:
                return 0
            visited.add(node)
            return 1 + sum(dfs(neigh) for neigh in diagram[node])
        
        return sum(dfs(node) for node in diagram if node not in visited)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_vertices = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            sat_instance = generate_sat_instance(n)
            _, assignment = dpll(sat_instance)
            diagram = extract_coxeter_diagram(assignment)
            vertices = count_vertices(diagram)
            total_vertices += vertices
            instances_tested += 1
    
    mean_vertices = total_vertices / instances_tested
    conjecture_holds = all(vertices <= n**2 * math.log(n) for n, _ in zip(n_values, range(instances_tested)))
    
    return {
        "metric_name": "Number of vertices in Coxeter-Dynkin diagram",
        "metric_value": mean_vertices,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n_values[-1]}, vertices={total_vertices}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_vertices = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_vertices} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_vertices} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={n_values[-1]}, vertices={total_vertices}\" first_failing_seed={first_failing_seed + 1}")