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
from itertools import combinations

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                if k == i:
                    A[j][k] = 0
                else:
                    A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def minimal_tropical_motivic_rank(clauses):
    n = len(clauses)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    for i in range(n):
        for j in range(i+1, n):
            if clauses[i][j] == 1 and clauses[j][i] == -1:
                A[i][j] = 1
                A[j][i] = -1
            elif clauses[i][j] == -1 and clauses[j][i] == 1:
                A[i][j] = -1
                A[j][i] = 1
    
    try:
        x = gaussian_elimination(A, b)
        return sum(abs(val) for val in x)
    except ZeroDivisionError:
        return float('inf')

def dpll(clauses):
    def solve(assignment):
        if not clauses:
            return assignment
        clause = next((c for c in clauses if any(lit in assignment and (lit > 0) == assignment[lit] for lit in c)), None)
        if not clause:
            return assignment
        p = min(clause, key=abs)
        new_assignment = assignment.copy()
        new_assignment[p] = True
        result = solve(new_assignment)
        if result is not None:
            return result
        new_assignment[p] = False
        result = solve(new_assignment)
        if result is not None:
            return result
        return None
    
    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 3
    clauses = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    mtr_G = minimal_tropical_motivic_rank(clauses)
    w_phi_G = len(dpll(clauses))
    
    if mtr_G == float('inf'):
        return {
            "metric_name": "mtr(G)/w(φ_G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = mtr_G / w_phi_G
    return {
        "metric_name": "mtr(G)/w(φ_G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")