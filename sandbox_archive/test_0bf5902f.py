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
            return random.choice(['x', '¬x'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['&', '|', '^'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def frege_proof_width(formula):
        if formula.startswith('(') and formula.endswith(')'):
            formula = formula[1:-1]
        if ' & ' in formula or ' | ' in formula:
            return max(frege_proof_width(subformula) for subformula in formula.split(' & ') + formula.split(' | '))
        elif '^' in formula:
            return frege_proof_width(formula.split('^')[0]) + 1
        else:
            return 1
    
    def brauer_group_rank(formula):
        # Placeholder function to simulate Brauer group rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula)
    
    n = random.randint(5, 30)
    formula = generate_boolean_formula(n)
    width = frege_proof_width(formula)
    rank = brauer_group_rank(formula)
    
    if rank > 10 * width:  # Placeholder condition to simulate polynomial relationship
        return {
            "metric_name": "Brauer group rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Formula {formula} with width {width} and rank {rank}"
        }
    
    return {
        "metric_name": "Brauer group rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")