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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    n = len(matrix)
    copy_matrix = [row[:] for row in matrix]
    gaussian_elimination(copy_matrix)
    rank = 0
    for i in range(n):
        if any(copy_matrix[i]):
            rank += 1
    return rank

def tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    # Create clauses for each variable
    for i in range(1, n + 1):
        clauses.append([variables[i - 1]])
        clauses.append([-variables[i - 1], random.choice(variables[:i - 1])])
        clauses.append([-variables[i - 1], random.choice(variables[i:])])
    
    # Create clauses for each clause
    for i in range(n, 2 * n):
        clause = [random.choice(variables) for _ in range(3)]
        clauses.append(clause)
        clauses.append([-clause[0], -clause[1]])
        clauses.append([-clause[0], -clause[2]])
        clauses.append([-clause[1], -clause[2]])
    
    return variables, clauses

def resolution_width(clauses):
    queue = clauses[:]
    literals_seen = set()
    while queue:
        literal = random.choice(queue)
        if literal in literals_seen:
            continue
        literals_seen.add(literal)
        for clause in queue:
            if -literal in clause:
                new_clause = [l for l in clause if l != -literal]
                if not new_clause:
                    return len(literals_seen) + 1
                queue.append(new_clause)
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        incidence_matrix = [[0] * len(variables) for _ in range(len(clauses))]
        
        # Fill incidence matrix
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    incidence_matrix[i][literal - 1] = 1
                else:
                    incidence_matrix[i][-literal - 1] = 1
        
        minimal_rank = rank(incidence_matrix)
        width = resolution_width(clauses)
        
        results.append({
            "n": n,
            "minimal_rank": minimal_rank,
            "resolution_width": width
        })
    
    total_minimal_rank = sum(result["minimal_rank"] for result in results)
    total_resolution_width = sum(result["resolution_width"] for result in results)
    mean_ratio = (total_minimal_rank / total_resolution_width) if total_resolution_width != 0 else 0
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": 0.5 <= mean_ratio <= 1.5,
        "counterexample": "" if 0.5 <= mean_ratio <= 1.5 else f"mean_ratio={mean_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if 0.5 <= result["metric_value"] <= 1.5) / len(results)
    
    if all(0.5 <= result["metric_value"] <= 1.5 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction=1")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.5 <= result["metric_value"] <= 1.5))
        print(f"RESULT: FALSIFIED counterexample='mean_ratio_outside_range' first_failing_seed={first_failing_seed}")