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
            return "x"
        else:
            parts = [generate_formula(random.randint(1, n-1)) for _ in range(random.randint(2, 4))]
            return "(" + " & ".join(parts) + ")"
    
    def dpll_depth(formula):
        if formula.startswith("(") and formula.endswith(")"):
            formula = formula[1:-1]
        if "&" not in formula:
            return 1
        else:
            parts = formula.split("&")
            return max(dpll_depth(part) for part in parts)
    
    def symmetric_tensor_rank(formula):
        if formula == "x":
            return 1
        elif formula.startswith("(") and formula.endswith(")"):
            formula = formula[1:-1]
        if "&" not in formula:
            return 2
        else:
            parts = formula.split("&")
            return sum(symmetric_tensor_rank(part) for part in parts)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    str_values = []
    dpll_depths = []
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            str_value = symmetric_tensor_rank(formula)
            dpll_depth_value = dpll_depth(formula)
            instances_tested += 1
            str_values.append(str_value)
            dpll_depths.append(dpll_depth_value)
    
    correlation_coefficient = sum((str_values[i] - mean_str) * (dpll_depths[i] - mean_dpll) for i in range(len(str_values))) / len(str_values)
    mean_str = sum(str_values) / len(str_values)
    mean_dpll = sum(dpll_depths) / len(dpll_depths)
    
    if correlation_coefficient >= 0.7 and p_value <= 0.05:
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")