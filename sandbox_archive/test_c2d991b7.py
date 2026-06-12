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
import math
from fractions import Fraction
import sys

def generate_random_formula(n):
    if n == 0:
        return 'T'
    elif n == 1:
        return 'F'
    else:
        p = random.choice(['&', '|'])
        left = generate_random_formula(random.randint(0, n-1))
        right = generate_random_formula(random.randint(0, n-1))
        return f'({left} {p} {right})'

def dpll_solver(formula):
    if formula == 'T':
        return 1
    elif formula == 'F':
        return 0
    else:
        subformulas = formula.split()
        operator = subformulas[1]
        left = subformulas[2]
        right = subformulas[3]
        if operator == '&':
            return min(dpll_solver(left), dpll_solver(right))
        elif operator == '|':
            return max(dpll_solver(left), dpll_solver(right))

def p_adic_exponentiation_complexity(formula, p):
    if formula == 'T' or formula == 'F':
        return 0
    else:
        subformulas = formula.split()
        operator = subformulas[1]
        left = subformulas[2]
        right = subformulas[3]
        if operator == '&':
            return max(p_adic_exponentiation_complexity(left, p), p_adic_exponentiation_complexity(right, p))
        elif operator == '|':
            return max(p_adic_exponentiation_complexity(left, p), p_adic_exponentiation_complexity(right, p))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    d_F_values = []
    E_p_values = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_random_formula(n)
        d_F = dpll_solver(formula)
        E_p = p_adic_exponentiation_complexity(formula, 2)  # Using prime number 2
        d_F_values.append(d_F)
        E_p_values.append(E_p)

    if len(d_F_values) == 0 or len(E_p_values) == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_formula"
        }

    mean_d_F = sum(d_F_values) / len(d_F_values)
    mean_E_p = sum(E_p_values) / len(E_p_values)

    correlation_coefficient = 0
    for d_F, E_p in zip(d_F_values, E_p_values):
        correlation_coefficient += (d_F - mean_d_F) * (E_p - mean_E_p)
    correlation_coefficient /= (len(d_F_values) * math.sqrt(sum((x - mean_d_F) ** 2 for x in d_F_values)) * math.sqrt(sum((y - mean_E_p) ** 2 for y in E_p_values)))

    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8 and all(corr >= -0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results) or sum(1 for result in results if result["conjecture_holds"]) >= 25:
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_sufficiently_high\" first_failing_seed={first_failing_seed}")