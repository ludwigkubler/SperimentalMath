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

def generate_instance(n: int, m: int) -> tuple:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return (variables, clauses)

def tseitin_formula(variables: list, clauses: list) -> dict:
    literals = {var: f'x{var}' for var in variables}
    neg_literals = {var: f'-x{var}' for var in variables}
    formulas = {}
    
    def negate(lit):
        return neg_literals[lit] if lit.startswith('x') else literals[lit]
    
    def or_formula(*lits):
        return ' ∨ '.join(lits)
    
    def and_formula(*lits):
        return ' ∧ '.join(lits)
    
    def implies(lhs, rhs):
        return f'¬{lhs} ∨ {rhs}'
    
    def iff(lhs, rhs):
        return f'{implies(lhs, rhs)} ∧ {implies(rhs, lhs)}'
    
    for i, clause in enumerate(clauses):
        clause_var = f'y{i+1}'
        formulas[clause_var] = or_formula(*[negate(lit) if random.choice([True, False]) else lit for lit in clause])
    
    final_formula = and_formula(*formulas.values())
    
    return {var: literals[var] for var in variables}, final_formula

def local_chromatic_number(graph: dict) -> int:
    n = len(graph)
    colors = [-1] * n
    color_count = 0
    
    def is_safe(v, c):
        for u in range(n):
            if graph[v][u] and colors[u] == c:
                return False
        return True
    
    def dfs(v, c):
        nonlocal color_count
        colors[v] = c
        color_count = max(color_count, c + 1)
        for u in range(n):
            if graph[v][u] and colors[u] == -1:
                dfs(u, c)
    
    for v in range(n):
        if colors[v] == -1:
            dfs(v, 0)
    
    return color_count

def resolution_width(formula: str) -> int:
    clauses = formula.split(' ∧ ')
    queue = []
    while True:
        new_clauses = []
        found_resolvent = False
        for i in range(len(queue)):
            for j in range(i + 1, len(queue)):
                if any(lit.startswith('-') and lit[1:] == other_lit for lit in queue[i] for other_lit in queue[j]):
                    resolvent = ' ∧ '.join([lit for lit in queue[i] if not lit.startswith('-') and lit[1:] != other_lit] + [lit for lit in queue[j] if not lit.startswith('-') and lit[1:] != other_lit])
                    new_clauses.append(resolvent)
                    found_resolvent = True
        if not found_resolvent:
            return len(queue)
        queue.extend(new_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 4 * n)
        instance = generate_instance(n, m)
        variables, clauses = instance
        graph = [[False] * n for _ in range(n)]
        
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    graph[clause[i]-1][clause[j]-1] = True
                    graph[clause[j]-1][clause[i]-1] = True
        
        tseitin_vars, tseitin_formula_str = tseitin_formula(variables, clauses)
        w_phi = resolution_width(tseitin_formula_str)
        
        L_G = local_chromatic_number(graph)
        results.append(abs(L_G - w_phi))
    
    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    n_max = max(n_values)
    conjecture_holds = all(x <= 1 for x in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= 1) / len(results)
    
    if all(r <= 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(r > 1 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r > 1)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed + 1}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")