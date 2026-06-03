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

def generate_formula(n):
    if n == 1:
        return 'T' if random.choice([True, False]) else 'F'
    elif n == 2:
        op = random.choice(['&', '|'])
        left = generate_formula(1)
        right = generate_formula(1)
        return f"({left} {op} {right})"
    else:
        op = random.choice(['&', '|'])
        left = generate_formula(n // 2)
        right = generate_formula(n - n // 2)
        return f"({left} {op} {right})"

def dpll(formula):
    if formula == 'T':
        return []
    elif formula == 'F':
        return None
    else:
        var, op, subformula = formula[1:-1].split()
        if op == '&':
            left = dpll(subformula)
            right = dpll(subformula.replace(var, 'F'))
            if left is not None and right is not None:
                return left + right
            elif left is not None:
                return left
            else:
                return right
        elif op == '|':
            left = dpll(subformula)
            right = dpll(subformula.replace(var, 'T'))
            if left is not None or right is not None:
                return left or right
            else:
                return None

def regular_grammar_order(formula):
    if formula == 'T' or formula == 'F':
        return 1
    elif formula[0] == '(' and formula[-1] == ')':
        var, op, subformula = formula[1:-1].split()
        if op == '&':
            left = regular_grammar_order(subformula)
            right = regular_grammar_order(subformula.replace(var, 'F'))
            return max(left, right) + 1
        elif op == '|':
            left = regular_grammar_order(subformula)
            right = regular_grammar_order(subformula.replace(var, 'T'))
            return min(left, right) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        dpll_length = dpll(formula)
        if dpll_length is None:
            continue
        order = regular_grammar_order(formula)
        results.append((order, dpll_length))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    order_values = [r[0] for r in results]
    dpll_length_values = [r[1] for r in results]
    
    n = len(order_values)
    mean_order = sum(order_values) / n
    mean_dpll_length = sum(dpll_length_values) / n
    
    covariance = sum((order_values[i] - mean_order) * (dpll_length_values[i] - mean_dpll_length) for i in range(n)) / n
    variance_order = sum((order_values[i] - mean_order) ** 2 for i in range(n)) / n
    variance_dpll_length = sum((dpll_length_values[i] - mean_dpll_length) ** 2 for i in range(n)) / n
    
    pearson_correlation = covariance / (math.sqrt(variance_order) * math.sqrt(variance_dpll_length))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")