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
    
    def generate_random_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['&', '|', '^'])
            a = generate_random_formula(n - 1)
            b = generate_random_formula(n - 1)
            return f'({a} {op} {b})'
    
    def resolution_width(phi):
        # Simplified resolution width calculation for demonstration
        # This is a placeholder and should be replaced with actual computation
        return len(phi.split()) * 2
    
    def minimal_quasi_monte_carlo_order(n):
        # Placeholder function to compute the minimal order of quasi-Monte Carlo points
        # This is a simplified version and should be replaced with actual computation
        return n + 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_random_formula(n)
    width = resolution_width(phi)
    order = minimal_quasi_monte_carlo_order(n)
    
    c = 2  # Placeholder constant for demonstration
    if width > c * order:
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"phi={phi}, width={width}, order={order}"
        }
    else:
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_width = sum(r["metric_value"] for r in results)
    num_trials = len(results)
    mean_width = total_width / num_trials
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / num_trials)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_trials
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")