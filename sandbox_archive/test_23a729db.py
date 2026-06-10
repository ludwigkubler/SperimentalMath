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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for r in range(i+1, m):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for r in range(i+1, m):
            factor = A[r][i] / A[i][i]
            for c in range(n):
                A[r][c] -= factor * A[i][c]

    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    
    det = 0
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for c in range(n):
            submatrix = [row[:c] + row[c+1:] for row in A[1:]]
            det += ((-1) ** c) * A[0][c] * determinant(submatrix)
    
    return det

def tseitin_formula(n):
    clauses = []
    literals = list(range(1, n+1)) + [-i for i in range(1, n+1)]
    random.shuffle(literals)
    
    # Create clauses
    for i in range(1, n+1):
        clause = [literals[i-1], literals[n+i-1]]
        clauses.append(clause)
    
    return clauses

def resolution_width(clauses):
    queue = set()
    for clause in clauses:
        if any(lit < 0 and -lit in queue for lit in clause):
            return len(queue)
        queue.update(clause)
    
    return len(queue)

def min_local_system_rank(clauses):
    n = len(clauses)
    matroid_matrix = [[0] * (2*n) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for lit in clause:
            if lit > 0:
                matroid_matrix[i][lit-1] = 1
            else:
                matroid_matrix[i][-lit-1] = 1
    
    rank = gaussian_elimination(matroid_matrix)
    return sum(1 for row in rank if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = tseitin_formula(n)
            m_lr = min_local_system_rank(clauses)
            w = resolution_width(clauses)
            
            metrics.append((m_lr, w))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metrics:
        return {
            "metric_name": "min_local_system_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_lr_values, w_values = zip(*metrics)
    correlation = sum((m - (sum(m_lr_values) / len(m_lr_values))) * (w - (sum(w_values) / len(w_values)))
                      for m, w in metrics) / len(metrics)
    
    return {
        "metric_name": "min_local_system_rank",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.8 * n_values[-1],
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")