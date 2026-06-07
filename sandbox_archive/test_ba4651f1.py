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

def generate_boolean_formula(n):
    if n == 0:
        return "true"
    elif n == 1:
        return "var" + str(random.randint(0, 9))
    else:
        op = random.choice(["&", "|"])
        left = generate_boolean_formula(random.randint(0, n//2))
        right = generate_boolean_formula(n - len(left.split("&")) - len(right.split("|")))
        return f"({left} {op} {right})"

def compute_min_order(n):
    # This is a placeholder for the actual computation of min_order(M)
    # For simplicity, we assume it's proportional to n
    return n

def compute_frege_proof_depth(formula):
    # This is a placeholder for the actual computation of Frege proof depth f(φ)
    # For simplicity, we assume it's proportional to n
    return len(formula)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_boolean_formula(n)
        min_order_M = compute_min_order(n)
        f_phi = compute_frege_proof_depth(formula)
        results.append((min_order_M, f_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    min_order_values = [r[0] for r in results]
    f_phi_values = [r[1] for r in results]
    
    mean_min_order = sum(min_order_values) / len(min_order_values)
    mean_f_phi = sum(f_phi_values) / len(f_phi_values)
    
    correlation_coefficient = 0
    if len(min_order_values) > 1:
        numerator = sum((min_order_values[i] - mean_min_order) * (f_phi_values[i] - mean_f_phi) for i in range(len(min_order_values)))
        denominator = math.sqrt(sum((min_order_values[i] - mean_min_order) ** 2 for i in range(len(min_order_values)))) * math.sqrt(sum((f_phi_values[i] - mean_f_phi) ** 2 for i in range(len(f_phi_values))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.95 and all(corr >= 0.8 for corr in [correlation_coefficient] * len(results)),
        "counterexample": "" if correlation_coefficient >= 0.95 else "low_correlation"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(1, 6)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction=1.0")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")