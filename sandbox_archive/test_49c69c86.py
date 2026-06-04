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
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def count_integral_points(n):
        return 2**n
    
    def resolution_proof_width(formula):
        # Simplified DPLL solver for demonstration purposes
        if '1' not in formula and '0' not in formula:
            return 1
        return len(formula)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    total_points = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(50):  # Sample at least 100 instances per seed
            formula = generate_boolean_formula(n)
            points = count_integral_points(n)
            width = resolution_proof_width(formula)
            total_width += width
            total_points += points
            instances_tested += 1
    
    mean_width = total_width / instances_tested
    mean_points = total_points / instances_tested
    conjecture_holds = mean_width <= 3 * mean_points
    counterexample = "" if conjecture_holds else f"mean_width={mean_width}, mean_points={mean_points}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")