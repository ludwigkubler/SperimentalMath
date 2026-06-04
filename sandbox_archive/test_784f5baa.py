# auto-injected by SEC sandbox
import math
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

def generate_formula(n):
    if n == 1:
        return "x"
    else:
        left = generate_formula(random.randint(1, n-2))
        right = generate_formula(n - len(left) - 2)
        return f"({left} & {right})"

def calculate_ramanujan_q(formula):
    # Placeholder for Ramanujan's Q-function calculation
    # This is a dummy implementation and should be replaced with actual logic
    return random.random()

def calculate_resolution_width(formula):
    # Placeholder for resolution proof width calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(formula.split())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        q_value = calculate_ramanujan_q(formula)
        w_value = calculate_resolution_width(formula)
        
        results.append({
            "n": n,
            "q_value": q_value,
            "w_value": w_value
        })
    
    if not results:
        return {
            "metric_name": "Ramanujan Q and Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    q_values = [r["q_value"] for r in results]
    w_values = [r["w_value"] for r in results]
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    
    # Placeholder for linear regression
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    slope, _ = linear_regression(q_values, w_values)
    
    conjecture_holds = abs(slope) >= 0.7
    counterexample = "" if conjecture_holds else "slope < 0.7"
    
    return {
        "metric_name": "Ramanujan Q and Resolution Width",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" not in trial_result or trial_result["metric_value"] is None:
            continue
        
        results.append(trial_result["metric_value"])
    
    if not results:
        print("RESULT: INCONCLUSIVE no_valid_results")
    else:
        mean = sum(results) / len(results)
        std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if abs(r) >= 0.7) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(next(r for r in results if abs(r) < 0.7))]
            print(f"RESULT: FALSIFIED counterexample=\"slope < 0.7\" first_failing_seed={first_failing_seed}")