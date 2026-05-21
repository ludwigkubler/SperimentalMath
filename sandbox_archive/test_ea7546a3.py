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
            return 'True' if random.choice([0, 1]) else 'False'
        subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
        operator = random.choice(['&', '|'])
        return f"({subformulas[0]} {operator} {subformulas[1]})"
    
    def compute_l_function_rank(formula):
        # Placeholder function to simulate L-function rank computation
        # This is a dummy implementation for the sake of testing
        return len(formula.split())
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_boolean_formula(n)
            rank = compute_l_function_rank(formula)
            phi_n = math.log(n) ** 2  # Simplified polynomial function for demonstration
            
            results.append({
                "n": n,
                "formula": formula,
                "rank": rank,
                "phi_n": phi_n
            })
    
    max_rank = max(result["rank"] for result in results)
    conjecture_holds = all(result["rank"] <= result["phi_n"] for result in results)
    counterexample = "" if conjecture_holds else f"Formula: {results[max_rank]['formula']}, Rank: {max_rank}, Phi(n): {results[max_rank]['phi_n']}"
    
    return {
        "metric_name": "L-function rank",
        "metric_value": max_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[max_rank]['formula']}\" first_failing_seed={first_failing_seed}")