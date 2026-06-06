# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['&', '|'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def communication_complexity(formula):
        # Simplified version of communication complexity calculation
        if formula == '0':
            return 0
        elif formula == '1':
            return 0
        else:
            return len(formula)
    
    def cohomology_group_size(n):
        # Simplified version of cohomology group size calculation
        return n
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    rank_variance = communication_complexity(formula)
    cohomology_size = cohomology_group_size(n)
    
    metric_value = log_factorial(n) * (max(cohomology_size, 1) / min(cohomology_size, 1))
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "Cohomology Size Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def log_factorial(n):
    if n == 0:
        return Fraction(1)
    else:
        result = Fraction(1)
        for i in range(1, n + 1):
            result *= Fraction(i)
        return result.log()

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")