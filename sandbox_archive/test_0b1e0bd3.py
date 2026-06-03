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
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]

    # Back-substitution to find the rank
    rank = 0
    for row in matrix:
        if any(row[i] != 0 for i in range(n)):
            rank += 1
    return rank

def quadratic_form(literals, clauses):
    n = len(literals)
    Q = [[0] * n for _ in range(n)]
    
    for clause in clauses:
        literals_in_clause = [l for l in clause if l != 0]
        if not literals_in_clause:
            continue
        i = int(abs(literals_in_clause[0]) - 1) % n
        j = int(abs(literals_in_clause[1]) - 1) % n
        Q[i][j] += 1
        Q[j][i] += 1
    
    return gaussian_elimination(Q)

def tseitin_formula(n):
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Clause: x1 ∨ ¬x2 ∨ ... ∨ ¬xn
    clause = [-i for i in range(1, n+1)]
    clauses.append(clause)
    
    # Clauses: xi ∨ ¬xi -> ¬xi ∨ ¬xi (tautology)
    for i in range(n):
        clause = [i+1, -(i+1), -(i+1)]
        clauses.append(clause)
    
    return literals, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in range(5, 41):
        literals, clauses = tseitin_formula(n)
        min_rank = quadratic_form(literals, clauses)
        resolution_width = len(clauses)  # Simplified for demonstration
        
        results.append({
            "n": n,
            "min_rank": min_rank,
            "resolution_width": resolution_width
        })
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_ranks = [r["min_rank"] for r in results]
    widths = [r["resolution_width"] for r in results]
    
    correlation_coefficient = sum((min_ranks[i] - mean_min_ranks) * (widths[i] - mean_widths) for i in range(len(results))) / math.sqrt(sum((min_ranks[i] - mean_min_ranks)**2 for i in range(len(results))) * sum((widths[i] - mean_widths)**2 for i in range(len(results))))
    
    mean_min_ranks = sum(min_ranks) / len(min_ranks)
    mean_widths = sum(widths) / len(widths)
    
    if correlation_coefficient < 0.9:
        return {
            "metric_name": "min_rank",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": f"Correlation coefficient {correlation_coefficient} < 0.9"
        }
    
    return {
        "metric_name": "min_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {seed} {trial_result}")
        
        if not "metric_value" in trial_result or trial_result["conjecture_holds"] is False:
            break
    
    results = [run_trial(seed) for seed in seeds]
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")