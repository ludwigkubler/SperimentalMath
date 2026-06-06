# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations, product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def resolution_width(cnf):
    clauses = [set(clause) for clause in cnf]
    variables = set()
    for clause in clauses:
        variables.update(clause)
    
    n = len(variables)
    max_width = 0
    for assignment in product([True, False], repeat=n):
        unsatisfied_clauses = []
        for clause in clauses:
            if not any(lit in assignment for lit in clause) and not any(not lit in assignment for lit in clause):
                unsatisfied_clauses.append(clause)
        
        resolution_tree = []
        while unsatisfied_clauses:
            new_clause = None
            for i in range(len(unsatisfied_clauses)):
                for j in range(i+1, len(unsatisfied_clauses)):
                    if any(lit in unsatisfied_clauses[i] and not lit in unsatisfied_clauses[j] for lit in variables):
                        new_clause = [lit for lit in unsatisfied_clauses[i] if lit not in unsatisfied_clauses[j]]
                        break
                if new_clause:
                    break
            if new_clause is None:
                break
            resolution_tree.append(new_clause)
            unsatisfied_clauses.remove(new_clause)
        
        max_width = max(max_width, len(resolution_tree))
    
    return max_width

def geometric_fluctuation(cnf):
    n = len(cnf[0])
    num_satisfying_assignments = sum(1 for assignment in product([True, False], repeat=n) if all(any(lit in assignment for lit in clause) or any(not lit in assignment for lit in clause) for clause in cnf))
    total_variation = Fraction(num_satisfying_assignments - 2**n + 1, 2**n)
    return total_variation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    correlation_sum = 0.0
    
    for n in n_values:
        cnf = [[random.choice([True, False]) for _ in range(n)] for _ in range(2*n)]
        
        resolution_w = resolution_width(cnf)
        gf = geometric_fluctuation(cnf)
        
        if resolution_w is None or gf is None:
            return {
                "metric_name": "Resolution Width vs Geometric Fluctuation",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        correlation_sum += resolution_w * gf
        instances_tested += 1
    
    mean_correlation = correlation_sum / instances_tested
    return {
        "metric_name": "Resolution Width vs Geometric Fluctuation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": mean_correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")