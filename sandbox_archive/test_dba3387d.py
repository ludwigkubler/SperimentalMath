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
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot row
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(A[i][i], A[i][i])
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            if factor == 0:
                continue
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return rank(A)

def rank(A):
    m, n = len(A), len(A[0])
    r = 0
    for i in range(m):
        if all(A[i][j] == 0 for j in range(n)):
            continue
        r += 1
    return r

def dpll(formula, assignment={}):
    if not formula:
        return True
    var = next(iter(formula))
    pos_clauses = [c for c in formula if var in c]
    neg_clauses = [c for c in formula if -var in c]
    
    # Try assigning True to var
    new_assignment = assignment.copy()
    new_assignment[var] = True
    if dpll(pos_clauses, new_assignment):
        return True
    
    # Try assigning False to var
    new_assignment[var] = False
    if dpll(neg_clauses, new_assignment):
        return True
    
    return False

def mrd(formula):
    n = len(formula)
    V = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            clause = formula[i] & formula[j]
            if not clause:
                continue
            V[i][j] = 1
            V[j][i] = 1
    
    return rank(V)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = {frozenset(random.sample(range(-n, -1), k)) for k in range(1, n)}
            mrd_value = mrd(formula)
            h_value = dpll(formula)
            
            if h_value == 0:
                continue
            
            results.append((mrd_value, h_value))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mrd_values, h_values = zip(*results)
    mean_mrd = sum(mrd_values) / len(mrd_values)
    mean_h_squared = sum(h**2 for h in h_values) / len(h_values)
    correlation_coefficient = sum((m - mean_mrd) * (h**2 - mean_h_squared) for m, h in zip(mrd_values, h_values)) / (len(results) * sum((m - mean_mrd)**2 for m in mrd_values))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(formula) for formula, _ in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.1 and mean_abs_diff <= 0.1,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=NA")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")