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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['&', '|', '^'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def dpll_solver(formula):
        if formula == '0':
            return 1
        elif formula == '1':
            return 0
        else:
            subformulas = formula.split()
            operator = subformulas[1]
            left, right = subformulas[0], subformulas[2]
            if operator == '&':
                return dpll_solver(left) + dpll_solver(right)
            elif operator == '|':
                return max(dpll_solver(left), dpll_solver(right))
            elif operator == '^':
                return abs(dpll_solver(left) - dpll_solver(right))
    
    def p_adic_exponentiation_complexity(formula, p):
        if formula == '0' or formula == '1':
            return 0
        else:
            subformulas = formula.split()
            operator = subformulas[1]
            left, right = subformulas[0], subformulas[2]
            if operator == '&':
                return max(p_adic_exponentiation_complexity(left, p), p_adic_exponentiation_complexity(right, p))
            elif operator == '|':
                return max(p_adic_exponentiation_complexity(left, p), p_adic_exponentiation_complexity(right, p))
            elif operator == '^':
                return 1 + max(p_adic_exponentiation_complexity(left, p), p_adic_exponentiation_complexity(right, p))
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    results = []
    p = 3  # fixed prime number
    
    for _ in range(30):
        n = random.randint(5, 40)
        formula = generate_boolean_formula(n)
        d_F = dpll_solver(formula)
        E_p = p_adic_exponentiation_complexity(formula, p)
        results.append((d_F, E_p))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson's Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    d_F_values, E_p_values = zip(*results)
    correlation_coefficient = pearson_correlation_coefficient(d_F_values, E_p_values)
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient > 0.8 and all(corr >= -0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_linear_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_seeds_support")