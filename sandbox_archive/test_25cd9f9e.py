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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return "x"
        else:
            formulas = [generate_formula(i) for i in range(1, n)]
            return "(" + "&".join(formulas) + ")"
    
    def dpll_depth(formula):
        if formula == "x":
            return 1
        elif formula.startswith("("):
            parts = formula[1:-1].split("&")
            return max(dpll_depth(part) for part in parts) + 1
    
    def symmetric_tensor_rank(formula):
        # Placeholder function to simulate the computation of STR(φ)
        # This is a dummy implementation and should be replaced with actual logic
        if formula == "x":
            return 1
        else:
            return sum(symmetric_tensor_rank(part) for part in formula.split("&"))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_ranks = []
    total_depths = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            formula = generate_formula(n)
            rank = symmetric_tensor_rank(formula)
            depth = dpll_depth(formula)
            total_instances += 1
            total_ranks.append(rank)
            total_depths.append(depth)
    
    correlation_coefficient = calculate_correlation(total_ranks, total_depths)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

def calculate_correlation(x, y):
    n = len(x)
    if n == 0:
        return None
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    var_x = sum((xi - mean_x) ** 2 for xi in x) / n
    var_y = sum((yi - mean_y) ** 2 for yi in y) / n
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

def p_value(correlation_coefficient, n):
    # Placeholder function to simulate the calculation of p-value
    # This is a dummy implementation and should be replaced with actual logic
    if correlation_coefficient == 0:
        return 1.0
    else:
        t_stat = correlation_coefficient * math.sqrt((n - 2) / (1 - correlation_coefficient ** 2))
        df = n - 2
        # Use a t-distribution table or library to find p-value
        # For simplicity, we return a dummy value
        return 0.5

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")