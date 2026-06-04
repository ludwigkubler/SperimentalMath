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
            return "A"
        else:
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f"({left} AND {right})"
    
    def ramanujan_q(formula):
        if formula == "A":
            return 1
        elif formula.startswith("(") and formula.endswith(")"):
            left, _, right = formula[1:-1].partition(" AND ")
            return ramanujan_q(left) * ramanujan_q(right)
        else:
            raise ValueError("Invalid formula")
    
    def resolution_width(formula):
        if formula == "A":
            return 1
        elif formula.startswith("(") and formula.endswith(")"):
            left, _, right = formula[1:-1].partition(" AND ")
            return max(resolution_width(left), resolution_width(right)) + 1
        else:
            raise ValueError("Invalid formula")
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        Q_min_sum = 0
        w_sum = 0
        
        while len(results) < 30:
            formula = generate_formula(n)
            Q_min = ramanujan_q(formula)
            w = resolution_width(formula)
            
            if Q_min is not None and w is not None:
                instances_tested += 1
                Q_min_sum += Q_min
                w_sum += w
                results.append((Q_min, w))
        
        if instances_tested < 30:
            return {
                "metric_name": "correlation",
                "metric_value": -1,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
    
    Q_min_avg = Q_min_sum / len(results)
    w_avg = w_sum / len(results)
    
    def linear_regression(x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        ss_xy = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
        ss_xx = sum((xi - x_mean) ** 2 for xi in x)
        
        b1 = ss_xy / ss_xx
        b0 = y_mean - b1 * x_mean
        
        return b0, b1
    
    Q_min_values, w_values = zip(*results)
    b0, b1 = linear_regression(Q_min_values, w_values)
    
    correlation_coefficient = (n - 1) / math.sqrt((sum(xi**2 for xi in Q_min_values) - n * Q_min_avg**2) *
                                                   (sum(xi**2 for xi in w_values) - n * w_avg**2))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            counterexample = f"seed={seed}, n_max={trial_result['n_max']}"
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
            sys.exit(0)
        
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")