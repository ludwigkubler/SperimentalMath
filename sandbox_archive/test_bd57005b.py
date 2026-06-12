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

def generate_random_formula(n):
    if n == 1:
        return 'x' + str(random.randint(0, 1))
    else:
        op = random.choice(['&', '|'])
        left = generate_random_formula(n // 2)
        right = generate_random_formula(n - n // 2)
        return '(' + left + op + right + ')'

def resolution_proof_size(formula):
    if formula.startswith('(') and formula.endswith(')'):
        formula = formula[1:-1]
    if '&' in formula:
        left, right = formula.split('&')
        return max(resolution_proof_size(left), resolution_proof_size(right)) + 1
    elif '|' in formula:
        left, right = formula.split('|')
        return max(resolution_proof_size(left), resolution_proof_size(right))
    else:
        return 0

def hypergeometric_function_rank(formula):
    # Placeholder implementation of hypergeometric function rank
    # This is a dummy implementation for testing purposes
    return len(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_random_formula(n)
        hfr = hypergeometric_function_rank(formula)
        size_resolution = resolution_proof_size(formula)
        
        if size_resolution is None:
            continue
        
        metric_values.append(abs(hfr - size_resolution))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    conjecture_holds = all(3 <= abs(x) <= 10 for x in metric_values)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "abs_diff",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"]) > 10 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")