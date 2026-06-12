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

def generate_boolean_formula(n):
    if n == 1:
        return '0' if random.choice([True, False]) else '1'
    else:
        op = '&' if random.choice([True, False]) else '|'
        left = generate_boolean_formula(n // 2)
        right = generate_boolean_formula(n - n // 2)
        return f"({left} {op} {right})"

def dpll_solver(formula):
    def evaluate(formula):
        if formula == '0':
            return False
        elif formula == '1':
            return True
        else:
            op, left, right = formula[1], formula[2:-1].split(' ')[0], formula[2:-1].split(' ')[1]
            if op == '&':
                return evaluate(left) and evaluate(right)
            elif op == '|':
                return evaluate(left) or evaluate(right)
    
    return evaluate(formula)

def p_adic_exponentiation_complexity(formula, p):
    def count_powers(formula):
        if formula[0] != '(':
            return 1
        else:
            operator = formula[1]
            left = formula[2:-1].split(' ')[0]
            right = formula[2:-1].split(' ')[1]
            if operator == '&':
                return count_powers(left) + count_powers(right)
            elif operator == '|':
                return max(count_powers(left), count_powers(right))
    
    return count_powers(formula)

def pearson_correlation_coefficient(data_x, data_y):
    n = len(data_x)
    mean_x = sum(data_x) / n
    mean_y = sum(data_y) / n
    covariance = sum((data_x[i] - mean_x) * (data_y[i] - mean_y) for i in range(n)) / n
    std_dev_x = math.sqrt(sum((data_x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_dev_y = math.sqrt(sum((data_y[i] - mean_y) ** 2 for i in range(n)) / n)
    return covariance / (std_dev_x * std_dev_y)

def run_trial(seed: int):
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    d_F_values = []
    E_p_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_boolean_formula(n)
        
        if not formula:
            continue
        
        d_F = dpll_solver(formula)
        E_p = p_adic_exponentiation_complexity(formula, 2)  # Using prime number 2
        
        metric_values.append(d_F * E_p)
        d_F_values.append(d_F)
        E_p_values.append(E_p)
    
    if not metric_values:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = pearson_correlation_coefficient(d_F_values, E_p_values)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8 and all(corr >= -0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["metric_value"] < -0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < -0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_minus_0_5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")