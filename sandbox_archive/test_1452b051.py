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
    
    def tseitin_formula(variables, clauses):
        tseitin_vars = {}
        tseitin_clauses = []
        
        for var in variables:
            tseitin_var = f"t{var}"
            tseitin_vars[var] = tseitin_var
            tseitin_clauses.append((tseitin_var,))
        
        for clause in clauses:
            tseitin_clause = []
            for literal in clause:
                if literal.startswith('not '):
                    var = literal[4:]
                    tseitin_clause.append(f"not {tseitin_vars[var]}")
                else:
                    tseitin_clause.append(tseitin_vars[literal])
            tseitin_clauses.append(tuple(tseitin_clause))
        
        tseitin_formula_str = " and ".join(" or ".join(clause) for clause in tseitin_clauses)
        return tseitin_vars, tseitin_formula_str
    
    def resolution_prove(formula):
        clauses = formula.split(" and ")
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = set(clauses[i].split(" or "))
                    clause_j = set(clauses[j].split(" or "))
                    if any(not (not p) in clause_j for p in clause_i):
                        new_clause = " or ".join(p for p in clause_j if p not in clause_i)
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(clauses)
            clauses.append(new_clause)
    
    def local_chromatic_number(graph):
        n = len(graph)
        colors = [-1] * n
        
        def dfs(node, color):
            stack = [node]
            while stack:
                node = stack.pop()
                if colors[node] == -1:
                    colors[node] = color
                    for neighbor in graph[node]:
                        if colors[neighbor] == -1:
                            stack.append(neighbor)
        
        for i in range(n):
            if colors[i] == -1:
                dfs(i, 0)
        
        return max(colors) + 1
    
    def generate_instance(n, m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = random.sample(variables | {f"not {var}" for var in variables}, random.randint(1, n))
            clauses.append(clause)
        return variables, clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = random.randint(n, 2 * n)
        variables, clauses = generate_instance(n, m)
        tseitin_vars, tseitin_formula_str = tseitin_formula(variables, clauses)
        graph = {i: set() for i in range(len(variables))}
        for clause in clauses:
            for literal in clause:
                if literal.startswith('not '):
                    var = literal[4:]
                    graph[tseitin_vars[var]].add(tseitin_vars[literal])
                else:
                    graph[tseitin_vars[literal]].add(tseitin_vars[var])
        
        local_chromatic = local_chromatic_number(graph)
        resolution_width = resolution_prove(tseitin_formula_str)
        metric_value = abs(local_chromatic - resolution_width)
        
        total_metric_value += metric_value
        instances_tested += 1
        n_max = max(n_max, n)
        
        if metric_value > k:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, local_chromatic={local_chromatic}, resolution_width={resolution_width}"
    
    return {
        "metric_name": "Absolute difference between local chromatic number and resolution proof width",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")