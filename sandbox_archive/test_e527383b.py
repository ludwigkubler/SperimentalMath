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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            op = random.choice(['&', '|'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left} {op} {right})'
    
    def dpll_solve(formula):
        if '0' in formula and '1' in formula:
            return None
        if '0' not in formula:
            return True
        if '1' not in formula:
            return False
        
        var = next(c for c in formula if c.isalpha())
        true_branch = dpll_solve(formula.replace(var, '1'))
        if true_branch is not None:
            return true_branch
        false_branch = dpll_solve(formula.replace(var, '0'))
        return false_branch
    
    def calculate_minimal_order(n):
        # Simplified calculation for demonstration purposes
        return n * (n + 1) // 2
    
    def calculate_frege_proof_length(formula):
        if formula == '0' or formula == '1':
            return 1
        else:
            left, op, right = formula[1:-1].split()
            return 3 + max(calculate_frege_proof_length(left), calculate_frege_proof_length(right))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        length = calculate_frege_proof_length(formula)
        minimal_order = calculate_minimal_order(n)
        results.append((length, minimal_order))
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in results) / math.sqrt(sum((x - mean_x) ** 2 for x, _ in results) * sum((y - mean_y) ** 2 for _, y in results))
    mean_length = sum(x for x, _ in results) / len(results)
    mean_order = sum(y for _, y in results) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 else f"Correlation coefficient {correlation_coefficient} < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")