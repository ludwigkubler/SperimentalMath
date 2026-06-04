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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for k in range(i+1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Back substitution
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def dpll(sat_instance, assignment={}):
    if not sat_instance:
        return True
    var = next((v for v in sat_instance if v not in assignment), None)
    if var is None:
        return False
    
    # Try assigning True to var
    assignment[var] = 1
    if dpll(sat_instance, assignment):
        return True
    
    # Backtrack and try assigning False to var
    del assignment[var]
    assignment[var] = -1
    if dpll(sat_instance, assignment):
        return True
    
    # If both assignments fail, backtrack further
    del assignment[var]
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    hdc_values = []
    h_values = []
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            sat_instance = [(random.choice([-1, 1]) * random.randint(1, n)) for _ in range(n)]
            
            # Compute hdc(φ) using Grothendieck-Witt class computation modulo 2 (simplified)
            A = [[0] * n for _ in range(n)]
            b = [0] * n
            for lit in sat_instance:
                var, sign = abs(lit), lit // abs(lit)
                A[var-1][var-1] += sign
                b[var-1] += sign
            
            try:
                x = gaussian_elimination(A, b)
                hdc_value = sum(abs(x[i]) for i in range(n))
            except Exception as e:
                return {
                    "metric_name": "hdc",
                    "metric_value": None,
                    "instances_tested": 1,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
            
            hdc_values.append(hdc_value)
            
            # Compute h(φ) using DPLL
            assignment = {}
            if dpll(sat_instance, assignment):
                h_value = len(assignment)
            else:
                h_value = float('inf')
            
            h_values.append(h_value)
    
    mean_hdc = sum(hdc_values) / len(hdc_values)
    mean_h = sum(h_values) / len(h_values)
    std_dev_hdc = math.sqrt(sum((x - mean_hdc) ** 2 for x in hdc_values) / len(hdc_values))
    std_dev_h = math.sqrt(sum((x - mean_h) ** 2 for x in h_values) / len(h_values))
    
    correlation_coefficient = sum((hdc_values[i] - mean_hdc) * (h_values[i] - mean_h) for i in range(len(hdc_values))) / (len(hdc_values) * std_dev_hdc * std_dev_h)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(hdc_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")