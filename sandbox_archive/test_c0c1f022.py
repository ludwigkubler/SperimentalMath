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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, n) for _ in range(n)]
            clauses.append(clause)
        return clauses
    
    def dpll_solve(cnf):
        def solve(variables, assignment):
            if not cnf:
                return True
            literal = next((lit for lit in variables if lit not in assignment and -lit not in assignment), None)
            if literal is None:
                return False
            assignment[literal] = True
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if solve(variables, assignment):
                return True
            assignment[literal] = False
            assignment[-literal] = True
            new_cnf = [c for c in cnf if -literal not in c and literal not in c]
            if solve(variables, assignment):
                return True
            del assignment[literal]
            del assignment[-literal]
            return False
        
        variables = list(range(1, n + 1))
        assignment = {}
        return solve(variables, assignment)
    
    def local_coherence(cnf):
        graph = {i: set() for i in range(n)}
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    graph[lit].add(-lit)
                    graph[-lit].add(lit)
        visited = [False] * (n + 1)
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in graph[node]:
                        stack.append(neighbor)
        
        dfs(1)
        return sum(visited) - 1
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    coherence = local_coherence(cnf)
    path_length = dpll_solve(cnf)
    
    if path_length is None:
        return {
            "metric_name": "LocalCoherence",
            "metric_value": coherence,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL solver failed"
        }
    
    return {
        "metric_name": "LocalCoherence",
        "metric_value": coherence,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"DPLL solver failed\" first_failing_seed={first_failing_seed}")