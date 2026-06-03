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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            clauses.append([-variables[i-1], f'y{i}'])
            clauses.append([f'y{i}', -f'y{i}'])
        for i in range(n):
            for j in range(i+1, n):
                clauses.append([f'x{i}', f'x{j}', -f'y{i+j}'])
                clauses.append([-f'x{i}', f'x{j}', f'y{i+j}'])
                clauses.append([f'x{i}', -f'x{j}', f'y{i+j}'])
                clauses.append([-f'x{i}', -f'x{j}', -f'y{i+j}'])
        return variables, clauses
    
    def resolution_width(clauses):
        queue = set()
        for clause in clauses:
            queue.add(tuple(sorted(clause)))
        while True:
            new_clause = None
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                        if not new_clause:
                            return len(queue)
                        if new_clause not in queue:
                            queue.add(new_clause)
            if new_clause is None:
                break
        return len(queue)
    
    def local_indeterminacy(n):
        variables, clauses = tseitin_formula(n)
        A = [[0] * n for _ in range(n)]
        b = [0] * n
        for clause in clauses:
            for var in clause:
                if var.startswith('x'):
                    i = int(var[1:]) - 1
                    A[i][i] += 1
                elif var.startswith('-x'):
                    i = int(var[2:]) - 1
                    A[i][i] -= 1
        b = gaussian_elimination(A, b)
        return sum(abs(x) for x in b)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        i_phi = local_indeterminacy(n)
        w_phi = resolution_width(clauses)
        results.append((i_phi, w_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    i_phi_values = [i for i, w in results]
    w_phi_values = [w for i, w in results]
    mean_i_phi = sum(i_phi_values) / len(i_phi_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    correlation_coefficient = sum((i - mean_i_phi) * (w - mean_w_phi) for i, w in results) / (len(results) * math.sqrt(sum((i - mean_i_phi)**2 for i in i_phi_values)) * math.sqrt(sum((w - mean_w_phi)**2 for w in w_phi_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")