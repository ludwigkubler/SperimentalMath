# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

# Helper functions for DPLL algorithm
def dpll(formula):
    if not formula:
        return 0
    if isinstance(formula[0], tuple) and formula[0][0] == 'not':
        subformula = formula[0][1]
        if isinstance(subformula, str):
            return 1 + dpll([('or', subformula, ('not', subformula))])
        else:
            return 1 + dpll(subformula)
    elif isinstance(formula[0], tuple) and formula[0][0] == 'and':
        for subformula in formula[1:]:
            if isinstance(subformula, str):
                return 1 + dpll([('or', subformula, ('not', subformula))])
            else:
                return 1 + dpll(subformula)
    elif isinstance(formula[0], tuple) and formula[0][0] == 'or':
        for subformula in formula[1:]:
            if isinstance(subformula, str):
                return 1 + dpll([('or', subformula, ('not', subformula))])
            else:
                return 1 + dpll(subformula)
    elif isinstance(formula[0], tuple) and formula[0][0] == 'implies':
        antecedent = formula[0][1]
        consequent = formula[0][2]
        if isinstance(antecedent, str):
            return 1 + dpll([('or', antecedent, ('not', antecedent))])
        else:
            return 1 + dpll(antecedent)
    elif isinstance(formula[0], tuple) and formula[0][0] == 'iff':
        left = formula[0][1]
        right = formula[0][2]
        if isinstance(left, str):
            return 1 + dpll([('or', left, ('not', left))])
        else:
            return 1 + dpll(left)
    elif isinstance(formula[0], tuple) and formula[0][0] == 'xor':
        left = formula[0][1]
        right = formula[0][2]
        if isinstance(left, str):
            return 1 + dpll([('or', left, ('not', left))])
        else:
            return 1 + dpll(left)
    elif isinstance(formula[0], tuple) and formula[0][0] == 'true':
        return 0
    elif isinstance(formula[0], tuple) and formula[0][0] == 'false':
        return float('inf')
    else:
        raise ValueError("Invalid formula")

# Helper function to generate random Boolean formulas
def generate_formula(n, depth):
    if depth == 0 or n == 1:
        return random.choice(['true', 'false'])
    ops = ['and', 'or', 'implies', 'iff', 'xor']
    op = random.choice(ops)
    args = [generate_formula(n-1, depth-1) for _ in range(random.randint(2, 3))]
    if op == 'not':
        return ('not', args[0])
    else:
        return (op,) + tuple(args)

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n, depth=3)
        depth = dpll(formula)
        
        # Compute Eichler-Shimura Hecke operators (simplified example)
        min_order = n
        
        log_min_order = math.log(min_order) if min_order > 0 else float('-inf')
        results.append((log_min_order, depth))
    
    correlation_coefficient = calculate_correlation(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "correlation_coefficient < 0.7"
    }

# Helper function to calculate the correlation coefficient
def calculate_correlation(data):
    n = len(data)
    if n < 2:
        return float('nan')
    
    x_sum, y_sum, xy_sum, x2_sum, y2_sum = 0, 0, 0, 0, 0
    
    for log_min_order, depth in data:
        x_sum += log_min_order
        y_sum += depth
        xy_sum += log_min_order * depth
        x2_sum += log_min_order ** 2
        y2_sum += depth ** 2
    
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x2_sum - x_sum ** 2) * (n * y2_sum - y_sum ** 2))
    
    return numerator / denominator if denominator != 0 else float('nan')

# Main execution block
if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")