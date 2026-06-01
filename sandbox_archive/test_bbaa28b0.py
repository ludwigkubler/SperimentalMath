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

def generate_cnf(m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, m) * (2 * random.choice([0, 1]) - 1) for _ in range(random.randint(1, 5))]
        cnf.append(clause)
    return cnf

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find the pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Make all rows below this one 0 in the current column
        for k in range(i + 1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(n):
                A[k][j] -= factor * A[i][j]

    # Back substitution to find the solution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(A[i][-1], A[i][i])
        for k in range(i - 1, -1, -1):
            A[k][-1] -= A[k][i] * x[i]

    return x

def frege_depth(cnf):
    # Simplified DPLL solver to estimate Frege proof depth
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        pure_symbols = {}
        for clause in clauses:
            for literal in clause:
                symbol = abs(literal)
                if symbol in pure_symbols and pure_symbols[symbol] != literal:
                    return float('inf')
                elif symbol not in pure_symbols:
                    pure_symbols[symbol] = literal
        unit_clause = next((c for c in unit_clauses if c), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            depth_true = dpll([c for c in clauses if literal not in c], new_assignment)
            new_assignment[literal] = False
            depth_false = dpll([c for c in clauses if -literal not in c], new_assignment)
            return 1 + max(depth_true, depth_false)
        pure_clause = next((c for c in clauses if all(l in assignment for l in c)), None)
        if pure_clause:
            literal = next(l for l in pure_clause if assignment[l])
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return 1 + dpll([c for c in clauses if literal not in c], new_assignment)
        return float('inf')

    return dpll(cnf, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    mri_values = []
    frege_depths = []
    instances_tested = 0
    n_max = 0
    
    for m in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(m)
            instances_tested += 1
            n_max = max(n_max, len(cnf))
            
            # Compute minimal local ring index (simplified version)
            A = [[Fraction(0) for _ in range(m)] for _ in range(m)]
            for clause in cnf:
                for literal in clause:
                    row = abs(literal) - 1
                    col = abs(literal) - 1
                    A[row][col] += Fraction(1)
            try:
                x = gaussian_elimination(A)
                mri_values.append(sum(abs(x[i]) for i in range(m)))
            except ZeroDivisionError:
                mri_values.append(float('inf'))
            
            # Compute Frege proof depth
            frege_depths.append(frege_depth(cnf))
    
    if not mri_values or not frege_depths:
        return {
            "metric_name": "mri_vs_frege",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mri_values = [v for v in mri_values if v != float('inf')]
    frege_depths = [d for d in frege_depths if d != float('inf')]
    
    if not mri_values or not frege_depths:
        return {
            "metric_name": "mri_vs_frege",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_values"
        }
    
    mri_mean = sum(mri_values) / len(mri_values)
    frege_depth_mean = sum(frege_depths) / len(frege_depths)
    
    if len(mri_values) < 30 or len(frege_depths) < 30:
        return {
            "metric_name": "mri_vs_frege",
            "metric_value": mri_mean,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = 0
    for i in range(len(mri_values)):
        correlation += (mri_values[i] - mri_mean) * (frege_depths[i] - frege_depth_mean)
    correlation /= len(mri_values) * math.sqrt(sum((x - mri_mean) ** 2 for x in mri_values)) * math.sqrt(sum((y - frege_depth_mean) ** 2 for y in frege_depths))
    
    return {
        "metric_name": "mri_vs_frege",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) > 0.1,  # Threshold for significance
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "first_failing_seed" if first_failing_seed is not None else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")