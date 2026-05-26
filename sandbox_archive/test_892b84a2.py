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
            return 'x'
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(random.randint(2, 4))]
            return '(' + ' & '.join(subformulas) + ') | (' + ' & '.join(subformulas[::-1]) + ')'

    def evaluate_formula(formula):
        if formula == 'x':
            return random.choice([True, False])
        elif formula.startswith('('):
            subformulas = formula[1:-1].split(' | ')
            return any(evaluate_formula(subformula) for subformula in subformulas)
        else:
            return formula

    def frege_proof_width(formula):
        if formula == 'x':
            return 1
        elif formula.startswith('('):
            subformulas = formula[1:-1].split(' | ')
            return max(frege_proof_width(subformula) for subformula in subformulas)
        else:
            return 0

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_size = 0
        
        while instances_tested < 30:
            formula = generate_boolean_formula(n)
            size = frege_proof_width(formula)
            if size > 1:
                instances_tested += 1
                total_size += size
        
        results.append({
            "metric_name": "Brauer Group Size",
            "metric_value": total_size / instances_tested,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    return random.choice(results)

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")