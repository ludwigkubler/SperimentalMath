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
        return 'x'
    else:
        left = generate_formula(random.randint(1, n-1))
        right = generate_formula(n - len(left.split('&')) - len(right.split('|')))
        op = random.choice(['&', '|'])
        return f'({left}{op}{right})'

def dpll_search_tree_depth(formula):
    if formula == 'x':
        return 0
    elif '&' in formula:
        left, right = formula[1:-1].split('&')
        return max(dpll_search_tree_depth(left), dpll_search_tree_depth(right)) + 1
    else:
        left, right = formula[1:-1].split('|')
        return max(dpll_search_tree_depth(left), dpll_search_tree_depth(right)) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        min_order = len(formula.split('&')) + len(formula.split('|'))
        d_phi = dpll_search_tree_depth(formula)
        
        if d_phi == 0:
            continue
        
        log_min_order = math.log(min_order) if min_order > 0 else -math.inf
        results.append((log_min_order, d_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_formula"
        }
    
    n = len(results)
    sum_log_min_order = sum(x[0] for x in results)
    sum_d_phi = sum(x[1] for x in results)
    sum_log_min_order_squared = sum(x[0]**2 for x in results)
    sum_d_phi_squared = sum(x[1]**2 for x in results)
    sum_log_min_order_d_phi = sum(x[0] * x[1] for x in results)
    
    mean_log_min_order = sum_log_min_order / n
    mean_d_phi = sum_d_phi / n
    
    cov = (sum_log_min_order_d_phi - mean_log_min_order * mean_d_phi) / (n - 1)
    var_log_min_order = (sum_log_min_order_squared - mean_log_min_order**2) / (n - 1)
    var_d_phi = (sum_d_phi_squared - mean_d_phi**2) / (n - 1)
    
    std_dev_log_min_order = math.sqrt(var_log_min_order)
    std_dev_d_phi = math.sqrt(var_d_phi)
    
    correlation_coefficient = cov / (std_dev_log_min_order * std_dev_d_phi)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 31))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(x['metric_value'] for x in results if x['metric_value'] is not None) / len(results)
    std_dev_value = math.sqrt(sum((x['metric_value'] - mean_value)**2 for x in results if x['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for x in results if x['conjecture_holds']) / len(results)
    
    if all(x['conjecture_holds'] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev_value} support_fraction={support_fraction}")
    elif any(not x['conjecture_holds'] for x in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={seeds[next(i for i, x in enumerate(results) if not x['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_low_support_fraction")