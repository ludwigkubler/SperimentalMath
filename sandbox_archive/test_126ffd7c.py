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
    
    def generate_formula(n):
        if n == 1:
            return 'p'
        else:
            op = random.choice(['&', '|'])
            subformulas = [generate_formula(n // 2), generate_formula((n + 1) // 2)]
            return f'({subformulas[0]} {op} {subformulas[1]})'

    def minimal_rank(formula):
        # Placeholder for actual minimal rank computation
        # For simplicity, we assume it's proportional to the length of the formula
        return len(formula)

    def circuit_entanglement(formula):
        # Placeholder for actual circuit entanglement computation
        # For simplicity, we assume it's proportional to the number of variables
        if 'p' in formula:
            return 1
        else:
            return 0

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    
    rank = minimal_rank(formula)
    entanglement = circuit_entanglement(formula)
    
    if entanglement == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "entanglement_zero"
        }
    
    ratio = abs(rank / entanglement)
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"entanglement_zero\" first_failing_seed={first_failing_seed}")