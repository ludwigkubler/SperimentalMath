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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    return [row for row in A if any(row)]

def tseitin_formula(G):
    n = len(G)
    literals = {i: f'x{i}' for i in range(n)}
    clauses = []
    
    # Clause for each vertex
    for i in range(n):
        clause = [literals[i]]
        for j in range(n):
            if G[i][j]:
                clause.append(f'-{literals[j]}')
        clauses.append(clause)
    
    # Clause for each edge
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                literals_ij = f'x{i}{j}'
                literals_ji = f'x{j}{i}'
                clause = [f'-{literals_ij}', f'-{literals_ji}', literals[i], literals[j]]
                clauses.append(clause)
    
    # Clause for each edge
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                literals_ij = f'x{i}{j}'
                literals_ji = f'x{j}{i}'
                clause = [f'-{literals_ij}', f'-{literals_ji}', literals[i], literals[j]]
                clauses.append(clause)
    
    return clauses

def resolution(refutation):
    while True:
        new_clauses = []
        for i in range(len(refutation)):
            for j in range(i+1, len(refutation)):
                clause_i = refutation[i]
                clause_j = refutation[j]
                for lit_i in clause_i:
                    if '-' in lit_i:
                        neg_lit_i = lit_i[1:]
                    else:
                        neg_lit_i = f'-{lit_i}'
                    
                    if neg_lit_i in clause_j:
                        new_clause = [l for l in clause_i + clause_j if l != lit_i and l != neg_lit_i]
                        new_clauses.append(new_clause)
        
        refutation.extend(new_clauses)
        
        # Check for unit clauses
        unit_clauses = [c[0] for c in refutation if len(c) == 1]
        if not unit_clauses:
            break
        
        for lit in unit_clauses:
            refutation = [c for c in refutation if lit not in c and '-' + lit not in c]
    
    return refutation

def local_index(G):
    n = len(G)
    clauses = tseitin_formula(G)
    refutation = []
    
    # Add all clauses to the refutation
    for clause in clauses:
        refutation.append(clause)
    
    # Perform resolution
    refutation = resolution(refutation)
    
    return len(gaussian_elimination(refutation))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    ν = local_index(G)
    Tseitin_refutation = resolution(tseitin_formula(G))
    
    if ν == 0:
        expected_length = 2
    else:
        expected_length = 2 ** ν
    
    if len(Tseitin_refutation) < expected_length:
        conjecture_holds = False
        counterexample = f"Refutation length {len(Tseitin_refutation)} is less than expected {expected_length} for ν(G)={ν}"
    elif len(Tseitin_refutation) > expected_length:
        conjecture_holds = False
        counterexample = f"Refutation length {len(Tseitin_refutation)} is greater than expected {expected_length} for ν(G)={ν}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": len(Tseitin_refutation),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")