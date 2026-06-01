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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def minimal_symplectic_volume(n):
    # Generate a random symmetric matrix
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            A[j][i] = A[i][j]
    
    # Compute the determinant using Gaussian elimination
    det = Fraction(1)
    for row in gaussian_elimination(A):
        for val in row:
            det *= Fraction(val)
    
    return abs(det)

def dpll_search_tree_diameter(n):
    # Simplified DPLL algorithm to estimate diameter
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll([c for c in clauses if literal not in c and not all(l in assignment for l in c)], new_assignment)
        pure_literal = next((l for l in range(-n, 0) if all(l not in c or (l in assignment and assignment[l]) for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll([c for c in clauses if pure_literal not in c and not all(l in assignment for l in c)], new_assignment)
        literal = next((l for l in range(1, n+1)), None)
        return max(dpll(clauses + [[-literal]], assignment), dpll(clauses + [[literal]], assignment))
    
    clauses = []
    for i in range(n):
        clauses.append([i+1])
        clauses.append([-i-1])
    return dpll(clauses, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    msvs = []
    diameters = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = [random.randint(-n, n) for _ in range(n)]
            msvs.append(minimal_symplectic_volume(n))
            diameters.append(dpll_search_tree_diameter(n))
    
    if len(msvs) < 30 or len(diameters) < 30:
        return {
            "metric_name": "msv_vs_diameter",
            "metric_value": None,
            "instances_tested": len(msvs),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_msv = sum(msvs) / len(msvs)
    mean_diameter = sum(diameters) / len(diameters)
    covariance = sum((msv - mean_msv) * (diameter - mean_diameter) for msv, diameter in zip(msvs, diameters)) / len(msvs)
    variance_msv = sum((msv - mean_msv) ** 2 for msv in msvs) / len(msvs)
    variance_diameter = sum((diameter - mean_diameter) ** 2 for diameter in diameters) / len(diameters)
    
    correlation_coefficient = covariance / (math.sqrt(variance_msv) * math.sqrt(variance_diameter))
    
    return {
        "metric_name": "msv_vs_diameter",
        "metric_value": correlation_coefficient,
        "instances_tested": len(msvs),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"correlation={correlation_coefficient}"
    }

if __name__ == "__main__":
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
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples_found")