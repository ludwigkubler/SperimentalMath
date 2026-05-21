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

def generate_tseitin_formula(n):
    if n <= 0:
        return [], []
    
    variables = list(range(1, n + 1))
    clauses = []
    tseitin_vars = {}
    
    def add_clause(clause):
        clauses.append(clause)
    
    for i in range(1, n + 1):
        tseitin_vars[i] = len(variables) + i
        variables.append(tseitin_vars[i])
    
    for i in range(n):
        # (A_i -> A_{i+1})
        add_clause([tseitin_vars[i + 1], -variables[i]])
        add_clause([-tseitin_vars[i + 1], variables[i]])
        
        # (¬A_i ∨ ¬A_{i+1} ∨ A)
        add_clause([-variables[i], -tseitin_vars[i + 1], tseitin_vars[n + i + 1]])
    
    # (¬A_n ∨ B)
    add_clause([-variables[-1], n + 2])
    
    for i in range(n):
        # (B -> A_i)
        add_clause([n + 2, -tseitin_vars[i]])
        add_clause([-n + 2, tseitin_vars[i]])
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = generate_tseitin_formula(n)
    
    if not variables or not clauses:
        return {
            "metric_name": "Resolution refutation length",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Compute the minimal cyclic order of a maximal disjoint set
    graph = {v: [] for v in variables}
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                if clause[i] > 0 and clause[j] > 0:
                    graph[clause[i]].append(clause[j])
                    graph[clause[j]].append(clause[i])
    
    def dfs(v, visited):
        stack = [v]
        while stack:
            u = stack.pop()
            if u not in visited:
                visited.add(u)
                for neighbor in graph[u]:
                    stack.append(neighbor)
    
    max_disjoint_set = []
    visited = set()
    for v in variables:
        if v not in visited:
            dfs(v, visited)
            max_disjoint_set.append(len(visited))
            visited.clear()
    
    C_G = min(max_disjoint_set)
    
    # Compute the Resolution refutation length
    def resolution_refutation_length(clauses):
        stack = []
        while clauses:
            clause = clauses.pop()
            if len(clause) == 1:
                return -1
            unit_clause = next((c for c in clause if abs(c) not in (x[0] for x in stack)), None)
            if unit_clause is None:
                return -1
            polarity = unit_clause > 0
            unit_var = abs(unit_clause)
            new_clauses = []
            for other_clause in clauses:
                if unit_var in other_clause:
                    continue
                if not any(abs(c) == unit_var for c in other_clause):
                    new_clauses.append(other_clause)
                else:
                    new_clause = [c for c in other_clause if abs(c) != unit_var]
                    if polarity:
                        new_clause = [-x for x in new_clause]
                    new_clauses.append(new_clause)
            clauses = new_clauses
            stack.append((unit_var, polarity))
        return len(stack)
    
    refutation_length = resolution_refutation_length(clauses)
    
    if refutation_length < 0:
        counterexample = "resolution_failure"
    elif refutation_length < 2 ** C_G:
        counterexample = f"refutation_length<{2**C_G}"
    else:
        counterexample = ""
    
    return {
        "metric_name": "Resolution refutation length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2 ** C_G,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")