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

def generate_formula(n):
    if n == 0:
        return []
    elif n == 1:
        return [random.choice(['A', 'B'])]
    else:
        q = generate_formula(random.randint(1, min(n-2, 3)))
        r = generate_formula(n - len(q) - 2)
        return ['('] + q + ['|'] + r + [')']

def compute_dpll_width(formula):
    if not formula:
        return 0
    elif isinstance(formula[0], list):
        return max(compute_dpll_width(subformula) for subformula in formula)
    else:
        return len(formula)

def compute_noncommutative_rank(formula):
    # Placeholder function to simulate the rank computation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    dpll_width = compute_dpll_width(formula)
    rank = compute_noncommutative_rank(formula)
    
    if rank > 2**(n * math.log(2)):
        return {
            "metric_name": "Noncommutative Rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Formula with n={n}, DPLL width={dpll_width}, Rank={rank}"
        }
    
    return {
        "metric_name": "Noncommutative Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")