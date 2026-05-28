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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for r in range(i+1, rows):
            factor = -matrix[r][i] / matrix[i][i]
            for c in range(cols):
                if i == c:
                    matrix[r][c] = 0
                else:
                    matrix[r][c] += factor * matrix[i][c]
    
    # Back substitution to find the solution
    x = [0] * cols
    for r in range(rows-1, -1, -1):
        x[r] = matrix[r][-1] / matrix[r][r]
        for c in range(r+1, cols):
            matrix[r][-1] -= matrix[r][c] * x[c]
    
    return x

def min_rank(graph):
    n = len(graph)
    adjacency_matrix = [[0]*n for _ in range(n)]
    for u in graph:
        for v in graph[u]:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
    
    rank = 0
    for i in range(n):
        if all(adjacency_matrix[i][j] == 0 for j in range(i)):
            continue
        row = [adjacency_matrix[i][j] for j in range(n)]
        matrix = adjacency_matrix[:i] + [row] + adjacency_matrix[i+1:]
        try:
            gaussian_elimination(matrix)
            rank += 1
        except ZeroDivisionError:
            return rank
    return rank

def tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Each variable is true or false
    for var in variables:
        clauses.append([var])
        clauses.append(['~', var])
    
    # Implications between variables
    for i in range(n):
        for j in range(i+1, n):
            clauses.append([f'~{variables[i]}', f'~{variables[j]}', variables[i+j]])
            clauses.append([f'{variables[i]}', f'{variables[j]}', '~', variables[i+j]])
    
    # Final clause
    final_clause = []
    for i in range(n):
        final_clause.append(variables[i])
    clauses.append(final_clause)
    
    return variables, clauses

def resolution_proofs(clauses):
    def resolve(clause1, clause2):
        new_clauses = set()
        for lit1 in clause1:
            if lit1.startswith('~'):
                lit2 = lit1[1:]
                if lit2 in clause2:
                    continue
                else:
                    new_clause = [l for l in clause1 if l != lit1] + [l for l in clause2 if l != lit2]
                    new_clauses.add(tuple(sorted(new_clause)))
            else:
                lit2 = '~' + lit1
                if lit2 in clause2:
                    continue
                else:
                    new_clause = [l for l in clause1 if l != lit1] + [l for l in clause2 if l != lit2]
                    new_clauses.add(tuple(sorted(new_clause)))
        return new_clauses
    
    def is_tautology(clause):
        positive_lits = {lit for lit in clause if not lit.startswith('~')}
        negative_lits = {lit[1:] for lit in clause if lit.startswith('~')}
        return positive_lits & negative_lits
    
    clauses_set = set(map(tuple, clauses))
    while True:
        new_clauses = set()
        for clause1 in clauses_set:
            for clause2 in clauses_set:
                if clause1 != clause2 and not is_tautology(clause1) and not is_tautology(clause2):
                    resolved_clauses = resolve(clause1, clause2)
                    new_clauses.update(resolved_clauses)
        if not new_clauses:
            break
        clauses_set.update(new_clauses)
    
    return len(clauses_set)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        graph = {i: set() for i in range(n)}
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    u, v = int(clause[i][1:]) - 1, int(clause[j][1:]) - 1
                    graph[u].add(v)
                    graph[v].add(u)
        
        ν_G = min_rank(graph)
        L_F = resolution_proofs(clauses)
        
        results.append((ν_G, L_F))
    
    if len(results) < 30:
        return {
            "metric_name": "Resolution Proof Length",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    ν_G_values, L_F_values = zip(*results)
    mean_L_F = sum(L_F_values) / len(L_F_values)
    std_dev_L_F = math.sqrt(sum((x - mean_L_F)**2 for x in L_F_values) / len(L_F_values))
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": mean_L_F,
        "instances_tested": 30 * len(n_values),
        "conjecture_holds": all(L_F >= 2**(ν_G * math.log(2)) for ν_G, L_F in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
    
    if all(trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_L_F} std={std_dev_L_F} support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in enumerate([run_trial(seed) for seed in seeds], start=min(seeds)) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")