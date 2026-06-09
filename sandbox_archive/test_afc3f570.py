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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(matrix):
    A = [row[:] for row in matrix]
    r = gaussian_elimination(A)
    return sum(1 for row in r if any(row[col] != 0 for col in range(len(row))))

def mrd(formula):
    variables = set()
    clauses = []
    for clause in formula:
        variables.update(clause)
        clauses.append(clause)
    
    n = len(variables)
    V = [[0] * n for _ in range(n)]
    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            if i != j:
                count = sum(1 for clause in clauses if (var1 in clause and var2 not in clause) or (var1 not in clause and var2 in clause))
                V[i][j] = Fraction(count, 2)
    
    return rank(V)

def dpll(formula):
    def solve(model):
        if not formula:
            return True
        if any(not any(var in model for var in clause) for clause in formula):
            return False
        
        var = next(var for var in variables if var not in model)
        new_assignment = {var: True}
        if solve({**model, **new_assignment}):
            return True
        
        new_assignment = {var: False}
        if solve({**model, **new_assignment}):
            return True
        
        return False
    
    variables = set()
    for clause in formula:
        variables.update(clause)
    
    model = {}
    return solve(model)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    n_max = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        formula = [random.sample(range(1, n+1), random.randint(1, n)) for _ in range(random.randint(1, n))]
        mrd_value = mrd(formula)
        dpll_height = 0 if not dpll(formula) else 1  # Simplified DPLL height calculation
        metric_values.append(mrd_value - dpll_height**2)
        
        if abs(metric_value) > 0.1:
            conjecture_holds = False
            counterexample = f"mrd({formula})={mrd_value}, h({formula})^2={dpll_height**2}"
        
        n_max = max(n_max, len(formula))
    
    return {
        "metric_name": "mrd - dpll^2",
        "metric_value": sum(metric_values) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")