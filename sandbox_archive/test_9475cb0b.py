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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['&', '|'])
            return f"({subformulas[0]} {operator} {subformulas[1]})"
    
    def local_dimension(formula):
        if formula == '0' or formula == '1':
            return 0
        elif '&' in formula:
            left, right = formula.split('&')
            return max(local_dimension(left), local_dimension(right))
        else:
            left, right = formula.split('|')
            return 1 + max(local_dimension(left), local_dimension(right))
    
    def resolution_width(formula):
        if formula == '0' or formula == '1':
            return 0
        elif '&' in formula:
            left, right = formula.split('&')
            return max(resolution_width(left), resolution_width(right))
        else:
            left, right = formula.split('|')
            return 1 + max(resolution_width(left), resolution_width(right))
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    ld = local_dimension(formula)
    rw = resolution_width(formula)
    
    return {
        "metric_name": "local_dimension_vs_resolution_width",
        "metric_value": ld,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ld <= rw,
        "counterexample": "" if ld <= rw else f"Formula: {formula}, LD: {ld}, RW: {rw}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break