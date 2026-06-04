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
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below the pivot
        factor = Fraction(A[i][i])
        for j in range(i+1, n):
            A[j][i] /= factor
    
    return A

def hodge_complexity(phi):
    # Convert phi to a matrix representation (simplified example)
    n = len(phi)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if phi[i][j]:
                A[i][j] = 1
    
    rank = 0
    for row in gaussian_elimination(A):
        if any(row):
            rank += 1
    
    return rank

def dpll_proof_tree_height(phi):
    # Simplified DPLL algorithm to estimate proof tree height (simplified example)
    n = len(phi)
    clauses = phi[:]
    stack = []
    
    def backtrack():
        while True:
            if not stack:
                return len(clauses)  # Return the current depth
            
            clause = next((c for c in clauses if any(lit in c for lit in stack)), None)
            if not clause:
                stack.pop()
                continue
            
            literal = next(lit for lit in clause if lit in stack)
            if literal > 0:
                stack.append(-literal)
            else:
                stack.append(-literal)
    
    return backtrack()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    hdc_values = []
    h_values = []
    
    for n in n_values:
        phi = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
        
        hdc_value = hodge_complexity(phi)
        h_value = dpll_proof_tree_height(phi)
        
        hdc_values.append(hdc_value)
        h_values.append(h_value)
    
    mean_hdc = sum(hdc_values) / len(hdc_values)
    mean_h = sum(h_values) / len(h_values)
    std_dev = (sum((x - mean_hdc)**2 for x in hdc_values) / len(hdc_values))**0.5
    
    correlation_coefficient = sum((hdc_values[i] - mean_hdc) * (h_values[i] - mean_h) for i in range(len(hdc_values))) / (len(hdc_values) * std_dev * std_dev)
    
    if correlation_coefficient >= 0.8:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(hdc_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical support")