# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_random_formula(n):
    if n == 1:
        return '0' if random.random() < 0.5 else '1'
    else:
        op = random.choice(['&', '|'])
        left = generate_random_formula(n // 2)
        right = generate_random_formula(n - n // 2)
        return f"({left} {op} {right})"

def dpll_solver(formula):
    if formula == '0':
        return 1
    elif formula == '1':
        return 0
    else:
        operator = formula[1]
        left, right = formula.split(operator)[0].strip(), formula.split(operator)[2].strip()
        if operator == '&':
            return max(dpll_solver(left), dpll_solver(right))
        elif operator == '|':
            return min(dpll_solver(left), dpll_solver(right))

def p_adic_exponentiation_complexity(formula, p):
    def is_power_of_p(n):
        while n % p == 0:
            n //= p
        return n == 1

    def count_powers(formula):
        if formula == '0' or formula == '1':
            return 0
        else:
            operator = formula[1]
            left, right = formula.split(operator)[0].strip(), formula.split(operator)[2].strip()
            return (count_powers(left) + count_powers(right)) if operator == '&' else max(count_powers(left), count_powers(right))

    return count_powers(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_random_formula(n)
        d_F = dpll_solver(formula)
        E_p = p_adic_exponentiation_complexity(formula, 2)  # Using prime number 2
        results.append((d_F, E_p))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    d_F_values, E_p_values = zip(*results)
    n = len(d_F_values)
    mean_d_F = sum(d_F_values) / n
    mean_E_p = sum(E_p_values) / n
    
    covariance = sum((d_F - mean_d_F) * (E_p - mean_E_p) for d_F, E_p in zip(d_F_values, E_p_values)) / n
    variance_d_F = sum((d_F - mean_d_F) ** 2 for d_F in d_F_values) / n
    variance_E_p = sum((E_p - mean_E_p) ** 2 for E_p in E_p_values) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_d_F) * math.sqrt(variance_E_p))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(correlation_coefficient >= -0.5 for _ in range(25, 31)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < -0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < -0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_neg_0_5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support")