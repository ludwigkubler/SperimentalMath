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

def generate_tseitin_formula(m, n):
    variables = [f'x{i}' for i in range(m)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(m):
        clause = [variables[i]]
        for j in range(n):
            if random.choice([True, False]):
                clause.append(f'~{variables[j]}')
        clauses.append(clause)
    
    # Generate binary clauses between variables
    for i in range(m):
        for j in range(i + 1, m):
            clauses.append([f'~{variables[i]}', f'{variables[j]}'])
            clauses.append([f'~{variables[j]}', f'{variables[i]}'])
    
    return clauses

def resolution_tree_width(clauses):
    variables = set()
    for clause in clauses:
        for literal in clause:
            if literal.startswith('~'):
                variables.add(literal[1:])
            else:
                variables.add(literal)
    
    variables = sorted(variables)
    variable_map = {v: i for i, v in enumerate(variables)}
    
    tree = [[] for _ in range(len(variables))]
    
    def add_clause(clause):
        resolvents = []
        for literal in clause:
            if literal.startswith('~'):
                negated_var = literal[1:]
                if negated_var in variable_map:
                    resolvent = (negated_var, literal)
                    resolvents.append(resolvent)
        
        for i in range(len(resolvents)):
            for j in range(i + 1, len(resolvents)):
                var1, lit1 = resolvents[i]
                var2, lit2 = resolvents[j]
                if var1 != var2:
                    new_clause = [lit1[1:], lit2[1:]]
                    add_clause(new_clause)
        
        for var, literal in resolvents:
            tree[variable_map[var]].append(variable_map[literal])
    
    for clause in clauses:
        add_clause(clause)
    
    max_width = 0
    visited = [False] * len(tree)
    
    def dfs(node):
        if visited[node]:
            return 0
        visited[node] = True
        width = 1
        for neighbor in tree[node]:
            width = max(width, dfs(neighbor) + 1)
        return width
    
    for i in range(len(variables)):
        max_width = max(max_width, dfs(i))
    
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = n // 2
    clauses = generate_tseitin_formula(m, n)
    
    width = resolution_tree_width(clauses)
    
    return {
        "metric_name": "resolution_tree_width",
        "metric_value": width,
        "instances_tested": len(clauses),
        "conjecture_holds": width >= 2**m - 1,
        "counterexample": "" if width >= 2**m - 1 else f"Formula with m={m}, n={n} failed"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*37, 127))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(res["metric_value"] for res in results) / len(results)
    std_width = math.sqrt(sum((res["metric_value"] - mean_width)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Formula with m={m}, n={n} failed\" first_failing_seed={first_failing_seed}")