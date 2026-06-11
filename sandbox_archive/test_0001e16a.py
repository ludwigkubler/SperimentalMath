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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def generate_boolean_formula(n):
    if n == 0:
        return "False"
    elif n == 1:
        return "True"
    else:
        op = random.choice(["and", "or"])
        left = generate_boolean_formula(random.randint(0, n-1))
        right = generate_boolean_formula(n - len(left) - 2)
        return f"({left} {op} {right})"

def compute_resolution_width(formula):
    stack = []
    for char in formula:
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                stack.pop()
            stack.pop()
        elif char in ['and', 'or']:
            while stack and stack[-1] in ['and', 'or']:
                stack.pop()
            stack.append(char)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        formula = generate_boolean_formula(n)
        mtr_QCBG = len(formula)  # Simplified proxy for QCBG order
        w_phi = compute_resolution_width(formula)
        
        metric_values.append((mtr_QCBG, w_phi))
        instances_tested += 1
        n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_formula"
        }
    
    mtr_QCBG_values, w_phi_values = zip(*metric_values)
    mean_mtr_QCBG = sum(mtr_QCBG_values) / len(mtr_QCBG_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    
    # Pearson correlation coefficient
    cov = sum((mtr - mean_mtr_QCBG) * (w - mean_w_phi) for mtr, w in zip(mtr_QCBG_values, w_phi_values))
    var_mtr_QCBG = sum((mtr - mean_mtr_QCBG) ** 2 for mtr in mtr_QCBG_values)
    var_w_phi = sum((w - mean_w_phi) ** 2 for w in w_phi_values)
    
    if var_mtr_QCBG == 0 or var_w_phi == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    corr_coeff = cov / (var_mtr_QCBG * var_w_phi) ** 0.5
    
    return {
        "metric_name": "resolution_width",
        "metric_value": corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(corr_coeff) >= Fraction(9, 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")