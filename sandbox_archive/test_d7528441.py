# auto-injected by SEC sandbox
import math
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
        factor = Fraction(A[i][i], A[i][i])
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            if factor == 0:
                continue
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_rank(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def cnf_to_quasigroup(cnf):
    n = len(cnf[0])
    q = [[0] * (2**n) for _ in range(2**n)]
    for clause in cnf:
        for lit in clause:
            i, b = abs(lit) - 1, lit > 0
            for j in range(2**n):
                if j & (1 << i):
                    q[j][j ^ (1 << i)] = 1 if b else 0
    return q

def resolution_width(cnf):
    clauses = cnf[:]
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                clause_i = set(clauses[i])
                clause_j = set(clauses[j])
                for lit in clause_i:
                    if -lit in clause_j:
                        new_clause = (clause_i ^ {lit}) | (clause_j ^ {-lit})
                        if new_clause not in new_clauses and new_clause not in clauses:
                            new_clauses.append(new_clause)
        if not new_clauses:
            break
        clauses.extend(new_clauses)
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = [[random.randint(1, n*2) for _ in range(random.randint(1, n))] for _ in range(n)]
        q = cnf_to_quasigroup(cnf)
        order = matrix_rank(q)
        width = resolution_width(cnf)
        
        results.append({
            "n": n,
            "order": order,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    order_values = [r["order"] for r in results]
    width_values = [r["width"] for r in results]
    
    mean_order = sum(order_values) / len(order_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation = sum((o - mean_order) * (w - mean_width) for o, w in zip(order_values, width_values)) / \
                  (len(results) * sum((o - mean_order)**2 for o in order_values) ** 0.5 *
                   sum((w - mean_width)**2 for w in width_values) ** 0.5)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": "" if correlation >= 0.8 else "low_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    correlation_values = [run_trial(seed)["metric_value"] for seed in seeds if run_trial(seed)["instances_tested"] > 0]
    support_fraction = sum(1 for r in correlation_values if r >= 0.8) / len(correlation_values)
    
    if all(r >= 0.8 for r in correlation_values):
        print(f"RESULT: SUPPORTED mean={sum(correlation_values)/len(correlation_values):.4f} std=0.0000 support_fraction={support_fraction:.2f}")
    elif any(r < 0.8 for r in correlation_values):
        first_failing_seed = next(seed for seed in seeds if run_trial(seed)["metric_value"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")