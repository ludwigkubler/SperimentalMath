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
from fractions import Fraction
import math

def generate_random_formula(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
        clauses.append(' & '.join(clause))
    return ' | '.join(clauses)

def tropical_polynomial(clause):
    terms = []
    for term in clause.split(' & '):
        if term.startswith('~'):
            var = term[2:]
            coeff = -1
        else:
            var = term
            coeff = 1
        terms.append((var, coeff))
    return terms

def tropical_monomial_ideal(formula):
    ideal = []
    for clause in formula.split(' | '):
        ideal.extend(tropical_polynomial(clause))
    return ideal

def resolution_width(formula):
    stack = [formula]
    while stack:
        current = stack.pop()
        if ' | ' not in current:
            continue
        left, right = current.split(' | ')
        stack.append(left)
        stack.append(right)
    return len(stack)

def min_order(ideal):
    order = 0
    for var, coeff in ideal:
        order = max(order, abs(coeff))
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_random_formula(n)
        ideal = tropical_monomial_ideal(formula)
        width = resolution_width(formula)
        order = min_order(ideal)
        
        if width == 0 or order == 0:
            continue
        
        ratio = Fraction(order, width)
        results.append((n, ratio))
    
    if not results:
        return {
            "metric_name": "order_over_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = sum(ratio for _, ratio in results) / len(results)
    instances_tested = len(results)
    n_max = max(n_values)
    conjecture_holds = 0.5 <= metric_value <= 2
    counterexample = "" if conjecture_holds else "order_over_width out of range"
    
    return {
        "metric_name": "order_over_width",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=no_results")
    else:
        mean_value = sum(result['metric_value'] for result in results) / len(results)
        std_value = math.sqrt(sum((result['metric_value'] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not result['conjecture_holds'] for result in results):
            first_failing_seed = next(result['seed'] for result in results if not result['conjecture_holds'])
            print(f"RESULT: FALSIFIED counterexample=\"order_over_width out of range\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")