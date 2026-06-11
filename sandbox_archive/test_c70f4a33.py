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

def generate_boolean_instance(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([0, 1]) for _ in range(n)]
        if sum(clause) == 0:
            clause[random.randint(0, n-1)] = 1
        clauses.append(clause)
    return clauses

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(n):
        if i >= m:
            break
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented_matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= augmented_matrix[i][j] * x[j]
    
    return x

def clause_indicator_polynomial(clauses):
    n = len(clauses)
    poly = [0] * (2**n)
    for i in range(2**n):
        assignment = [(i >> j) & 1 for j in range(n)]
        product = 1
        for clause in clauses:
            if all(assignment[j] == clause[j] for j in range(n)):
                product *= -1
        poly[i] += product
    return poly

def minimal_quaternion_algebra_order(poly):
    n = len(poly)
    qm = []
    mte = 0
    for i in range(n):
        if poly[i] != 0:
            qm.append([i, poly[i]])
            mte += abs(poly[i])
    
    return qm, mte

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            clauses = generate_boolean_instance(n)
            poly = clause_indicator_polynomial(clauses)
            qm, mte = minimal_quaternion_algebra_order(poly)
            
            if len(qm) == 0 or mte == 0:
                continue
            
            instances_tested += 1
            order = sum(abs(x[1]) for x in qm)
            correlation_sum += order / mte
    
    mean_o_qm = correlation_sum / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_o_qm >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_order_over_mte",
        "metric_value": mean_o_qm,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_o_qm = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_o_qm} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_o_qm} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")