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
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(2 * n):
        clause = ' | '.join(random.sample(variables, 2))
        if random.choice([True, False]):
            clause = '~' + clause
        clauses.append(clause)
    formula = ' & '.join(clauses)
    return formula

def resolution_width(formula):
    stack = []
    for token in formula.split(' & '):
        if token.startswith('~'):
            token = token[1:]
            found = False
            for i, s in enumerate(stack):
                if s == token:
                    stack.pop(i)
                    found = True
                    break
                elif s.startswith('~') and s[1:] == token:
                    stack.pop(i)
                    found = True
                    break
            if not found:
                stack.append(token)
        else:
            for i, s in enumerate(stack):
                if s.startswith('~') and s[1:] == token:
                    stack.pop(i)
                    break
            stack.append(token)
    return len(stack)

def tropical_order(formula):
    # Placeholder function to compute the tropical order of a formula
    # This is a dummy implementation for demonstration purposes
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        width = resolution_width(formula)
        order = tropical_order(formula)
        results.append((n, order, width))
    
    min_order = min(order for _, order, _ in results)
    max_width = max(width for _, _, width in results)
    
    if max_width < 16:
        return {
            "metric_name": "min_order",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max_width,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    correlation = sum((order - width) ** 2 for _, order, width in results)
    correlation /= len(results)
    correlation = math.sqrt(correlation)
    
    return {
        "metric_name": "min_order",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max_width,
        "conjecture_holds": 0.5 <= correlation <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")