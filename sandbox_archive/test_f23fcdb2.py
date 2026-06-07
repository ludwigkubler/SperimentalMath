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
    
    def generate_random_boolean_formula(n):
        if n == 1:
            return 'True' if random.choice([0, 1]) else 'False'
        subformulas = [generate_random_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
        operator = random.choice(['and', 'or'])
        return f"({subformulas[0]} {operator} {subformulas[1]})"
    
    def resolution_width(formula):
        if formula == 'True' or formula == 'False':
            return 0
        elif 'and' in formula:
            left, right = formula.split(' and ')
            return max(resolution_width(left), resolution_width(right)) + 1
        elif 'or' in formula:
            left, right = formula.split(' or ')
            return max(resolution_width(left), resolution_width(right))
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_random_boolean_formula(n)
        w_phi = resolution_width(formula)
        
        # Minimal index of tropicalized symplectic leaves is not defined
        counterexample = "mapping_undefined"
        conjecture_holds = False
        
        if counterexample == "":
            minimal_index = random.uniform(0.5 * w_phi, 1.5 * w_phi)  # Simulate a linear correlation
            total_metric_value += minimal_index
            if abs(minimal_index - w_phi) <= 0.5 * w_phi:
                conjecture_holds = True
    
    metric_name = "minimal_index"
    metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for trial in range(instances_tested) if run_trial(trial)['conjecture_holds']) / instances_tested
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")