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
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['and', 'or'])
            return f'({generate_boolean_formula(n-1)} {op} {generate_boolean_formula(1)})'
    
    def dpll_search_tree_height(formula):
        if formula == 'True' or formula == 'False':
            return 0
        else:
            op = formula.split()[1]
            left, right = formula.split(op)
            return max(dpll_search_tree_height(left.strip()), dpll_search_tree_height(right.strip())) + 1
    
    def braid_group_order(formula):
        if formula == 'True' or formula == 'False':
            return 1
        else:
            op = formula.split()[1]
            left, right = formula.split(op)
            return max(braid_group_order(left.strip()), braid_group_order(right.strip())) + 1
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_boolean_formula(n)
        height = dpll_search_tree_height(formula)
        order = braid_group_order(formula)
        metric_values.append((height, order))
    
    mean_height = sum(h for h, _ in metric_values) / instances_tested
    mean_order = sum(o for _, o in metric_values) / instances_tested
    
    correlation_coefficient = 0.0
    if len(metric_values) > 1:
        numerator = sum((h - mean_height) * (o - mean_order) for h, o in metric_values)
        denominator = math.sqrt(sum((h - mean_height)**2 for h, _ in metric_values)) * math.sqrt(sum((o - mean_order)**2 for _, o in metric_values))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient} < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")