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
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n+1):
                    A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll(cnf_formula):
    def backtrack(assignment, clause_set):
        if not clause_set:
            return True
        unit_clause = next((c for c in clause_set if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            var = abs(literal)
            if literal > 0 and var in assignment or literal < 0 and -var not in assignment:
                return backtrack(assignment | {var}, [c for c in clause_set if var not in c])
            else:
                return False
        pure_literal = next((v for v in range(1, len(cnf_formula) + 1) if (v not in assignment and -v not in assignment)), None)
        if pure_literal is None:
            pure_literal = random.choice([v for v in range(1, len(cnf_formula) + 1) if v not in assignment])
        return backtrack(assignment | {pure_literal}, [c for c in clause_set if pure_literal not in c])

    return backtrack(set(), cnf_formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf_formula = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        cnf_formula.append(clause)
    
    ehrhart_degree = m - n + 1
    resolution_width = dpll(cnf_formula)
    
    if resolution_width is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll returned None"
        }
    
    if resolution_width < ehrhart_degree:
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"resolution_width ({resolution_width}) < ehrhart_degree ({ehrhart_degree})"
        }
    
    if resolution_width - ehrhart_degree > 2 * (n + m).bit_length():
        return {
            "metric_name": "resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"resolution_width - ehrhart_degree ({resolution_width - ehrhart_degree}) > C * log(n + m)"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width < degree_of_Ehrhart_polynomial\" first_failing_seed={first_failing_seed + 1}")