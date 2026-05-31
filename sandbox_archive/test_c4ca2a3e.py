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
    
    def generate_formula(n):
        if n == 1:
            return "x"
        else:
            p = random.choice(["AND", "OR"])
            q = random.choice(["NOT", ""])
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f"({q}{left} {p} {right})"
    
    def count_variables(formula):
        variables = set()
        for char in formula:
            if char.isalpha():
                variables.add(char)
        return len(variables)
    
    def resolution_width(formula, variables):
        # Simplified version of resolution width calculation
        return max(len(v) for v in variables)
    
    def matrix_algebra_size(n):
        # Simplified size of matrix algebra associated with n variables
        return 2 ** n
    
    def aut_order(matrix_size):
        # Simplified order of automorphism group for a given matrix size
        if matrix_size == 1:
            return 1
        elif matrix_size == 2:
            return 2
        else:
            return matrix_size * (matrix_size - 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    aut_orders = []
    
    for n in n_values:
        formula = generate_formula(n)
        variables = count_variables(formula)
        width = resolution_width(formula, list(variables))
        matrix_size = matrix_algebra_size(variables)
        order = aut_order(matrix_size)
        
        widths.append(width)
        aut_orders.append(order)
    
    mean_width = sum(widths) / len(widths)
    mean_log_order = sum(math.log(order) for order in aut_orders) / len(aut_orders)
    correlation_coefficient = sum((width - mean_width) * (math.log(order) - mean_log_order) for width, order in zip(widths, aut_orders)) / (len(widths) * math.sqrt(sum((width - mean_width) ** 2 for width in widths) * sum((math.log(order) - mean_log_order) ** 2 for order in aut_orders)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(abs(math.log(order) - mean_log_order) <= 3 for order in aut_orders),
        "counterexample": "" if correlation_coefficient >= 0.8 else "correlation_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(math.log(order) - mean_log_order) <= 3 for order in aut_orders):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={next(seed for seed, result in enumerate(results, start=1) if not result['conjecture_holds'] and any(abs(math.log(order) - mean_log_order) <= 3 for order in aut_orders))}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")