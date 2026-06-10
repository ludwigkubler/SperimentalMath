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
    if n < 1:
        return [], []
    
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Base case: x1 ∨ -x2
    clauses.append(f'{literals[0]} -{literals[1]}')
    
    # Recursive case: xi ∨ -xi-1
    for i in range(1, n):
        clauses.append(f'{literals[i]} -{literals[i-1]}')
    
    # Final clause: x1 ∧ ... ∧ xn
    final_clause = ' '.join(literals)
    clauses.append(final_clause)
    
    return literals, clauses

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] + factor * A[i][k] for k in range(i, n)]
            b[j] += factor * b[i]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def min_diophantine_degree(clauses):
    n = len(clauses)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    for i in range(n):
        for j in range(i, n):
            if i == j:
                A[i][j] = 1
            else:
                A[i][j] = -1
            b[j] += 1
    
    x = gaussian_elimination(A, b)
    return max(abs(x[i]) for i in range(n))

def frege_proof_length(clauses):
    n = len(clauses)
    length = 0
    for clause in clauses:
        length += len(clause.split())
    return length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        literals, clauses = generate_tseitin_formula(n)
        
        dd = min_diophantine_degree(clauses)
        f = frege_proof_length(clauses)
        
        results.append((dd, f))
    
    if not results:
        return {
            "metric_name": "min_diophantine_degree",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    dd_values, f_values = zip(*results)
    mean_dd = sum(dd_values) / len(dd_values)
    mean_f = sum(f_values) / len(f_values)
    
    correlation_coefficient = sum((dd - mean_dd) * (f - mean_f) for dd, f in results) / \
                              math.sqrt(sum((dd - mean_dd)**2 for dd in dd_values)) / \
                              math.sqrt(sum((f - mean_f)**2 for f in f_values))
    
    conjecture_holds = correlation_coefficient >= 0.8 and max(dd_values) <= 2 * mean_dd
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> max_dd=<{}>".format(correlation_coefficient, max(dd_values))
    
    return {
        "metric_name": "min_diophantine_degree",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")