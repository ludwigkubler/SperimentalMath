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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        pivot_row = i
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                pivot_row = j
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        for j in range(i+1, rows):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    non_zero_rows = [row for row in reduced_matrix if any(row)]
    return len(non_zero_rows)

def generate_random_cnf(n, m):
    literals = list(range(1, n+1)) + [-i for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, 3)
        clauses.append(clause)
    return clauses

def compute_clause_tree_width(clauses):
    variables = set()
    for clause in clauses:
        variables.update(clause)
    variable_count = len(variables)
    
    # Simplified heuristic to estimate clause tree width
    # This is a placeholder and should be replaced with actual computation
    return variable_count * 2

def compute_quotient_group_size(n):
    # Placeholder for computing the size of the quotient group
    # This is a placeholder and should be replaced with actual computation
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = random.randint(2*n, 4*n)
        cnf = generate_random_cnf(n, m)
        clause_tree_width = compute_clause_tree_width(cnf)
        quotient_group_size = compute_quotient_group_size(n)
        
        results.append({
            "n": n,
            "m": m,
            "clause_tree_width": clause_tree_width,
            "quotient_group_size": quotient_group_size
        })
    
    total_clauses = sum(result["m"] for result in results)
    total_clause_tree_width = sum(result["clause_tree_width"] for result in results)
    average_clause_tree_width = total_clause_tree_width / len(results)
    
    conjecture_holds = all(10 * n**2 * math.log(n) <= result["clause_tree_width"] <= 10 * n**3 for result in results)
    conjecture_holds &= any(result["quotient_group_size"] <= 10 * n**2 for result in results)
    
    return {
        "metric_name": "average_clause_tree_width",
        "metric_value": average_clause_tree_width,
        "instances_tested": total_clauses,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")