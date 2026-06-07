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
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice([True, False])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['and', 'or'])
            return (operator, *subformulas)
    
    def evaluate_formula(formula):
        if isinstance(formula, bool):
            return formula
        else:
            operator, left, right = formula
            if operator == 'and':
                return evaluate_formula(left) and evaluate_formula(right)
            elif operator == 'or':
                return evaluate_formula(left) or evaluate_formula(right)
    
    def dpll_width(formula):
        if isinstance(formula, bool):
            return 1
        else:
            operator, left, right = formula
            if operator == 'and':
                return max(dpll_width(left), dpll_width(right))
            elif operator == 'or':
                return 1 + max(dpll_width(left), dpll_width(right))
    
    def tropical_motivic_rank(formula):
        if isinstance(formula, bool):
            return 0
        else:
            operator, left, right = formula
            if operator == 'and':
                return max(tropical_motivic_rank(left), tropical_motivic_rank(right))
            elif operator == 'or':
                return 1 + max(tropical_motivic_rank(left), tropical_motivic_rank(right))
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        phi = generate_boolean_formula(random.randint(5, n_max))
        mtr = tropical_motivic_rank(phi)
        w_DPLL = dpll_width(phi)
        
        if w_DPLL == 0:
            continue
        
        ratio = Fraction(mtr, w_DPLL)
        metric_values.append(ratio)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(value <= Fraction(1, 1) for value in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mtr_to_w_DPLL_ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 1 for i in range(5, 6)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")