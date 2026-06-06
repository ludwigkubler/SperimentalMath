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

# Helper functions for Boolean formula evaluation and SAT solvability
def evaluate(expression):
    if isinstance(expression, str):
        return expression == 'True'
    elif isinstance(expression, list):
        operator = expression[0]
        left = evaluate(expression[1])
        right = evaluate(expression[2])
        if operator == 'and':
            return left and right
        elif operator == 'or':
            return left or right
        elif operator == 'not':
            return not left
    else:
        raise ValueError("Invalid expression")

def is_satisfiable(formula):
    variables = set()
    def collect_variables(expression):
        if isinstance(expression, str) and expression.isalpha():
            variables.add(expression)
        elif isinstance(expression, list):
            collect_variables(expression[1])
            collect_variables(expression[2])
    collect_variables(formula)

    def backtrack(assignment):
        unassigned = [v for v in variables if v not in assignment]
        if not unassigned:
            return evaluate(formula, assignment)
        var = unassigned[0]
        for val in [True, False]:
            assignment[var] = val
            result = backtrack(assignment)
            if result is not None:
                return result
        del assignment[var]
        return None

    return backtrack({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    tau_values = []
    d_values = []

    for n in range(5, 41):
        for _ in range(3):  # Sample 3 instances per size
            variables = [f'x{i}' for i in range(n)]
            clauses = []
            for _ in range(n):
                clause = random.sample(variables + ['not ' + v for v in variables], n)
                clauses.append(clause)
            formula = ['and'] + [[['or'] + clause] for clause in clauses]
            satisfiable = is_satisfiable(formula)
            tau_values.append(len(clauses))
            d_values.append(satisfiable)

    metric_name = "Tropicalization Order vs. Satisfiability Degree"
    metric_value = sum(tau_values) / len(tau_values)
    n_max = 40
    conjecture_holds = False
    counterexample = ""

    if len(d_values) >= 24:
        correlation_coefficient = calculate_correlation(tau_values, d_values)
        mean_abs_diff = sum(abs(t - d) for t, d in zip(tau_values, d_values)) / len(tau_values)
        conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 1

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": len(d_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = "Not enough seeds supported the conjecture"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")