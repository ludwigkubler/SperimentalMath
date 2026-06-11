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
        return 'true' if random.choice([True, False]) else 'false'
    elif n == 1:
        return f'x{random.randint(0, n-1)}'
    else:
        op = random.choice(['&', '|'])
        left = generate_boolean_formula(random.randint(0, n-1))
        right = generate_boolean_formula(n - len(left) - 2)
        return f'({left} {op} {right})'

def compute_resolution_width(formula):
    stack = []
    for char in formula:
        if char == '(':
            stack.append(char)
        elif char == ')':
            count = 0
            while stack[-1] != '(':
                stack.pop()
                count += 1
            stack.pop()
            stack.append(count + 1)
        else:
            continue
    return max(stack)

def compute_quasi_commutative_braid_group_order(formula):
    # Placeholder for actual algorithm to compute the order of QCBG
    # This is a dummy implementation
    return len(formula) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_boolean_formula(n)
        mtr_qcbg = compute_quasi_commutative_braid_group_order(formula)
        w_phi = compute_resolution_width(formula)
        
        results.append({
            "n": n,
            "mtr_qcbg": mtr_qcbg,
            "w_phi": w_phi
        })
    
    if len(results) < 20:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_samples"
        }
    
    mtr_qcbg_values = [result["mtr_qcbg"] for result in results]
    w_phi_values = [result["w_phi"] for result in results]
    
    mean_mtr_qcbg = sum(mtr_qcbg_values) / len(mtr_qcbg_values)
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    
    correlation_sum = 0
    for mtr, w in zip(mtr_qcbg_values, w_phi_values):
        correlation_sum += (mtr - mean_mtr_qcbg) * (w - mean_w_phi)
    
    variance_mtr_qcbg = sum((mtr - mean_mtr_qcbg) ** 2 for mtr in mtr_qcbg_values) / len(mtr_qcbg_values)
    variance_w_phi = sum((w - mean_w_phi) ** 2 for w in w_phi_values) / len(w_phi_values)
    
    if variance_mtr_qcbg == 0 or variance_w_phi == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    correlation_coefficient = correlation_sum / (len(mtr_qcbg_values) * variance_mtr_qcbg ** 0.5 * variance_w_phi ** 0.5)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if "conjecture_holds" in result and result["conjecture_holds"]:
            results.append(result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_conjecture_holds")
    else:
        mean = sum(results) / len(results)
        std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if abs(r) >= 0.9]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(next((r for r in results if abs(r) < 0.9), None))]
            print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")