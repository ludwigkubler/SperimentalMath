# auto-injected by SEC sandbox
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
import math
from fractions import Fraction
import itertools

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for k in range(i+1, n):
            factor_k = Fraction(A[k][i], A[i][i])
            for j in range(n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] -= factor_k * A[i][j]
    return A

def determinant(A):
    n = len(A)
    det = Fraction(1, 1)
    for i in range(n):
        det *= A[i][i]
    return det

def m_order(phi):
    # Convert CNF to quadratic form matrix Q
    n = len(phi)
    Q = [[0] * n for _ in range(n)]
    for clause in phi:
        for var1 in clause:
            for var2 in clause:
                if var1 != var2:
                    Q[abs(var1)-1][abs(var2)-1] += 1
    return abs(determinant(gaussian_elimination(Q)))

def dpll_search_tree(phi):
    def dpll(clause_set, assignment):
        if not clause_set:
            return True
        unit_clause = next((c for c in clause_set if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[var] = True
            if dpll(clause_set - {unit_clause}, new_assignment):
                return True
            new_assignment[var] = False
            if dpll(clause_set - {unit_clause, frozenset([-var])}, new_assignment):
                return True
            return False
        pure_literal = next((v for v in range(1, n+1) if (v not in assignment and -v not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll(clause_set, new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll(clause_set, new_assignment):
                return True
            return False
        var = next((v for v in range(1, n+1) if v not in assignment and -v not in assignment), None)
        if dpll(clause_set, assignment | {var: True}):
            return True
        if dpll(clause_set, assignment | {var: False}):
            return True
        return False
    
    return len(dpll(phi, {}))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    phi = []
    for _ in range(10 * n):  # Generate a CNF with 10*n clauses and n variables
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if len(set(clause)) == 2:
            phi.append(frozenset(clause))
    
    m_order_val = m_order(phi)
    d_phi = dpll_search_tree(phi)
    
    return {
        "metric_name": "m_order_diameter_correlation",
        "metric_value": m_order_val * d_phi,
        "instances_tested": 10 * n,
        "n_max": n,
        "conjecture_holds": m_order_val * d_phi >= 0.7 * (n + 1) ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"m_order_diameter_correlation\" first_failing_seed={first_failing_seed}")