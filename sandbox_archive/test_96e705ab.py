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
        cnf = []
        for i in range(1, n+1):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def is_satisfiable(cnf):
        stack = []
        assignment = {}
        
        def dpll():
            if not cnf:
                return True
            literal = find_unassigned_variable(cnf)
            if literal is None:
                return False
            
            for value in [True, False]:
                new_assignment[literal] = value
                new_cnf = propagate(cnf, literal, value)
                if dpll():
                    return True
                del new_assignment[literal]
            
            return False
        
        def find_unassigned_variable(cnf):
            for clause in cnf:
                for literal in clause:
                    if literal not in new_assignment and -literal not in new_assignment:
                        return literal
            return None
        
        def propagate(cnf, literal, value):
            new_cnf = []
            for clause in cnf:
                if literal in clause:
                    continue
                if -literal in clause:
                    clause.remove(-literal)
                    if not clause:
                        return []
                    new_cnf.append(clause)
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        return dpll()
    
    def calculate_orbits(cnf):
        graph = {}
        for clause in cnf:
            for literal1 in clause:
                for literal2 in clause:
                    if literal1 != literal2:
                        if literal1 not in graph:
                            graph[literal1] = set()
                        if literal2 not in graph:
                            graph[literal2] = set()
                        graph[literal1].add(literal2)
                        graph[literal2].add(literal1)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        
        orbits = 0
        visited = set()
        for literal in graph:
            if literal not in visited:
                dfs(literal, visited)
                orbits += 1
        
        return orbits
    
    def calculate_resolution_width(cnf):
        clauses = [set(clause) for clause in cnf]
        queue = clauses.copy()
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                new_clause = set()
                for literal in clause1:
                    if -literal not in clause2:
                        new_clause.add(literal)
                for literal in clause2:
                    if -literal not in clause1:
                        new_clause.add(literal)
                if len(new_clause) == 0:
                    return 0
                queue.append(new_clause)
        return max(len(clause) for clause in clauses)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    orbits = calculate_orbits(cnf)
    width = calculate_resolution_width(cnf)
    
    return {
        "metric_name": "Orbit Width Ratio",
        "metric_value": Fraction(orbits, width) if width != 0 else None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": orbits == width,
        "counterexample": "" if orbits == width else f"Orbits: {orbits}, Width: {width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_count = sum(1 for r in results if r["conjecture_holds"])
    
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")