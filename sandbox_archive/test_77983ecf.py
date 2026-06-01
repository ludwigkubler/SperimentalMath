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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Search for a non-zero pivot in the column
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    break
            else:
                raise ValueError("Singular matrix")
        for j in range(n):
            if j == i:
                continue
            factor_k = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor_k * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def m_order(phi):
    # Convert CNF to quadratic form Q
    n = len(phi)
    Q = [[0] * n for _ in range(n)]
    for clause in phi:
        for literal in clause:
            var_index = abs(literal) - 1
            if literal > 0:
                Q[var_index][var_index] += 1
            else:
                Q[var_index][var_index] -= 1
    return abs(determinant(gaussian_elimination(Q)))

def dpll(phi, assignment=[]):
    if not phi:
        return True
    if any(all(literal in assignment for literal in clause) or all(-literal in assignment for literal in clause) for clause in phi):
        return False
    
    var = next(var for var in range(1, len(phi) + 1) if var not in [abs(lit) for lit in assignment])
    assignment.append(var)
    if dpll(phi, assignment):
        return True
    assignment.pop()
    assignment.append(-var)
    return dpll(phi, assignment)

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in {5, 10, 15, 20, 30, 40}:
        phi = generate_cnf(n)
        m_order_val = m_order(phi)
        dpll_tree = dpll(phi)
        if not dpll_tree:
            return {
                "metric_name": "m_order",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL search tree is empty"
            }
        results.append((m_order_val, dpll_tree))
    
    m_order_vals = [m for m, _ in results]
    dpll_trees = [d for _, d in results]
    correlation_coefficient = sum((m - sum(m_order_vals) / len(m_order_vals)) * (d - sum(dpll_trees) / len(dpll_trees)) for m, d in results)
    correlation_coefficient /= math.sqrt(sum((m - sum(m_order_vals) / len(m_order_vals)) ** 2 for m in m_order_vals)) * math.sqrt(sum((d - sum(dpll_trees) / len(dpll_trees)) ** 2 for d in dpll_trees))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")