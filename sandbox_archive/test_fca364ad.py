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
from fractions import Fraction
import math

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    
    for i in range(cols):
        max_row = rank
        for j in range(rank, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        if matrix[max_row][i] == 0:
            continue
        
        matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
        
        for j in range(rows):
            if j != rank:
                factor = -matrix[j][i] / matrix[rank][i]
                for k in range(cols):
                    matrix[j][k] += factor * matrix[rank][k]
        
        rank += 1
    
    return rank

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # XOR clauses
    for i in range(1, n+1):
        clause = [f'-{variables[i-1]}']
        for j in range(i+1, n+1):
            clause.append(f'{variables[j-1]}')
        clauses.append(clause)
    
    # OR clauses
    for i in range(n):
        clause = []
        for j in range(1, n+1):
            if (j - 1) & (1 << i):
                clause.append(f'{variables[j-1]}')
            else:
                clause.append(f'-{variables[j-1]}')
        clauses.append(clause)
    
    # Negation of the XOR of all variables
    neg_clause = [f'-{variables[i-1]}' for i in range(1, n+1)]
    clauses.append(neg_clause)
    
    return clauses

def resolution_prove(clauses):
    clauses_set = set(tuple(sorted(c)) for c in clauses)
    new_clauses = []
    
    while True:
        found_resolvent = False
        for i in range(len(new_clauses)):
            for j in range(i+1, len(new_clauses)):
                clause_i = new_clauses[i]
                clause_j = new_clauses[j]
                
                common_vars = set(clause_i) & set(clause_j)
                if not common_vars:
                    continue
                
                resolvent = []
                for var in clause_i:
                    if var.startswith('-') and var[1:] in clause_j:
                        continue
                    resolvent.append(var)
                for var in clause_j:
                    if var.startswith('-') and var[1:] in clause_i:
                        continue
                    resolvent.append(var)
                
                resolvent = sorted(set(resolvent))
                if tuple(resolvent) not in clauses_set:
                    new_clauses.append(resolvent)
                    found_resolvent = True
        
        if not found_resolvent:
            break
    
    return len(new_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        incidence_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Build incidence matrix
        for clause in formula:
            for var in clause:
                if var.startswith('-'):
                    var_index = int(var[1:]) - 1
                    incidence_matrix[var_index][n] += 1
                else:
                    var_index = int(var) - 1
                    incidence_matrix[n][var_index] += 1
        
        rank = gaussian_elimination(incidence_matrix)
        
        proof_length = resolution_prove(formula)
        
        results.append({
            "metric_name": "rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": rank <= n ** (2/3) * math.log(n, 2) ** 2 and proof_length >= rank,
            "counterexample": ""
        })
    
    total_rank = sum(result["metric_value"] for result in results)
    avg_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - avg_rank) ** 2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean": avg_rank,
        "std": std_rank,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(result["mean"] for result in results)
    avg_rank = total_rank / len(results)
    std_rank = math.sqrt(sum((result["mean"] - avg_rank) ** 2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank:.4f} std={std_rank:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")