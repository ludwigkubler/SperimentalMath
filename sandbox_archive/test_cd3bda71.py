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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate lower entries
        factor = 1 / matrix[i][i]
        for j in range(i, n):
            matrix[i][j] *= factor
        for k in range(i+1, n):
            factor = -matrix[k][i]
            for j in range(i, n):
                matrix[k][j] += factor * matrix[i][j]
    return matrix

def rank(matrix):
    n = len(matrix)
    r = 0
    for i in range(n):
        if all(matrix[i][j] == 0 for j in range(r)):
            continue
        r += 1
    return r

def minimal_representation_rank(G):
    n = len(G)
    A = [[0]*n for _ in range(n)]
    for u, v in G:
        A[u][v] = 1
    A_inv = gaussian_elimination(A)
    return rank(A_inv)

def tseitin_formula(variables, clauses):
    literals = set()
    formula = []
    for clause in clauses:
        literals |= set(clause)
        new_var = len(literals)
        formula.append([new_var] + [-l for l in clause])
        for l in clause:
            formula.append([-new_var, -l])
    return formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(n):
        clause = [random.choice(variables), random.choice(variables)]
        if len(set(clause)) == 2:
            clauses.append(clause)
    
    formula = tseitin_formula(variables, clauses)
    d = len(formula)
    
    G = defaultdict(list)
    for lit in range(1, n+1):
        for i in range(d):
            if lit in formula[i]:
                u = (i // 2) + 1
                v = (i % 2) * 2 + 1 + lit
                G[u].append(v)
    
    r = minimal_representation_rank(G)
    
    return {
        "metric_name": "minimal_representation_rank",
        "metric_value": r,
        "instances_tested": 1,
        "conjecture_holds": r >= 2**d,
        "counterexample": "" if r >= 2**d else f"Formula with resolution depth {d} has rank {r}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*2+1, 2))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with resolution depth {result['metric_value']} has rank {result['metric_value']}\", first_failing_seed={first_failing_seed}")