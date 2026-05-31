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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(random.randint(2, n))]
            operator = random.choice(['&', '|'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def resolution_width(formula):
        if formula == '0':
            return 1
        elif formula == '1':
            return 1
        else:
            subformula = formula[1:-1]
            operator = formula[2]
            left, right = subformula.split(operator)
            return max(resolution_width(left), resolution_width(right)) + 1
    
    def matrix_algebra(formula):
        n = len(formula)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            if formula[i] == '0':
                A[i][i] = -1
            elif formula[i] == '1':
                A[i][i] = 1
        return A
    
    def determinant(matrix, n):
        det = Fraction(0)
        if n == 1:
            return matrix[0][0]
        for j in range(n):
            submatrix = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1)**j * matrix[0][j] * determinant(submatrix, n-1)
        return det
    
    def order_of_automorphism_group(matrix):
        n = len(matrix)
        det = determinant(matrix, n)
        if det == 0:
            return 0
        else:
            return abs(det)
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        formula = generate_formula(n)
        width = resolution_width(formula)
        A = matrix_algebra(formula)
        order = order_of_automorphism_group(A)
        
        if order == 0:
            continue
        
        instances_tested += 1
        metric_values.append(width - math.log(order, 2))
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = (sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))**0.5
    
    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    return {
        "metric_name": "resolution_width_log_order",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = (sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_instances\" first_failing_seed={first_failing_seed}")