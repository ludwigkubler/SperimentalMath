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

def generate_tseitin_formula(n):
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for each literal
    for i in range(n):
        clauses.append([literals[i]])
    
    # Generate clauses for implications
    for i in range(1, n):
        clauses.append([-literals[i-1], literals[i]])
    
    # Generate the final clause
    clauses.append([-literals[n-2], -literals[n-1]])
    
    return clauses, literals

def gaussian_elimination(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    rank = 0
    
    for i in range(rows):
        if matrix[i][i] == 0:
            swap_found = False
            for j in range(i+1, rows):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        
        pivot = Fraction(matrix[i][i])
        for j in range(cols):
            matrix[i][j] /= pivot
        
        for j in range(rows):
            if j != i and matrix[j][i] != 0:
                factor = -matrix[j][i]
                for k in range(cols):
                    matrix[j][k] += factor * matrix[i][k]
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses, literals = generate_tseitin_formula(n)
        
        # Convert clauses to a matrix
        matrix = [[0] * (n + 1) for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                if lit.startswith('x'):
                    var_index = int(lit[1:]) - 1
                    matrix[var_index][var_index] += 1
        
        rank = gaussian_elimination(matrix)
        
        # Use a DPLL solver to find the resolution refutation size
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                lit = unit_clause[0]
                if lit < 0 and -lit in assignment:
                    return False
                assignment[lit] = True
                new_clauses = [c for c in clauses if not set(c).issubset(assignment)]
                return dpll(new_clauses, assignment)
            pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal is not None:
                assignment[pure_literal] = True
                new_clauses = [c for c in clauses if not set(c).issubset(assignment)]
                return dpll(new_clauses, assignment)
            literal = next((l for l in range(1, n+1) if l not in assignment), None)
            assignment[literal] = True
            new_clauses = [c for c in clauses if not set(c).issubset(assignment)]
            if dpll(new_clauses, assignment):
                return True
            assignment[literal] = False
            assignment[-literal] = True
            new_clauses = [c for c in clauses if not set(c).issubset(assignment)]
            return dpll(new_clauses, assignment)
        
        resolution_refutation_size = 0
        while not dpll(clauses, {}):
            resolution_refutation_size += 1
        
        results.append({
            "n": n,
            "rank": rank,
            "resolution_refutation_size": resolution_refutation_size
        })
    
    metric_value = sum(result["resolution_refutation_size"] for result in results)
    instances_tested = len(results)
    conjecture_holds = all(result["resolution_refutation_size"] >= 2**result["rank"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Resolution Refutation Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")