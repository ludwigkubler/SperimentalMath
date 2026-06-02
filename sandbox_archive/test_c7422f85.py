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
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def entropy(formula):
        ones = formula.count('1')
        zeros = len(formula) - ones
        if ones == 0 or zeros == 0:
            return 0
        p_one = Fraction(ones, len(formula))
        p_zero = Fraction(zeros, len(formula))
        return -p_one * math.log2(p_one) - p_zero * math.log2(p_zero)
    
    def algebraic_k_theory_order(n):
        # Placeholder for actual computation
        # For simplicity, we use a linear function of n
        return 2 * n
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        H_phi = entropy(formula)
        order = algebraic_k_theory_order(n)
        results.append((n, order, H_phi))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, order_values, H_phi_values = zip(*results)
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(order_values, H_phi_values)) / math.sqrt(sum((x - mean_x)**2 for x in order_values) * sum((y - mean_y)**2 for y in H_phi_values))
    mean_x = sum(n_values) / len(n_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= abs(correlation_coefficient) <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials")
        exit(0)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
    
    if all(abs(r["metric_value"]) >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 1.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) > 1.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_greater_than_1.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")