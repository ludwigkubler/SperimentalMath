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

def generate_polynomial(n, d):
    coeffs = [random.randint(1, 10) for _ in range(d + 1)]
    x = 'x'
    return sum(c * eval(f'{x}**{i}') for i, c in enumerate(coeffs))

def generate_xor_circuit(depth, n):
    circuit = []
    for _ in range(depth):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate, inputs))
    return circuit

def evaluate_polynomial(poly, x_val):
    x = x_val
    return eval(poly)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            d = random.randint(1, n // 2)
            poly = generate_polynomial(n, d)
            depth = len(generate_xor_circuit(d, n))
            
            p_value = evaluate_polynomial(poly, 1)  # Evaluate at x=1 for simplicity
            rho_squared = p_value ** 2
            
            results.append({
                "n": n,
                "d": d,
                "poly": poly,
                "depth": depth,
                "rho_squared": rho_squared
            })
    
    correlation_sum = 0
    diff_sum = 0
    instances_tested = len(results)
    
    for result in results:
        correlation_sum += result["depth"] / math.sqrt(result["rho_squared"])
        diff_sum += abs(result["depth"] - result["rho_squared"])
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation_mean = correlation_sum / instances_tested
    diff_mean = diff_sum / instances_tested
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_mean >= 0.8 and diff_mean <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    correlation_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(correlation_values) / len(results)
    
    if not correlation_values:
        RESULT = "INCONCLUSIVE no_valid_data"
    elif support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(correlation_values)/len(correlation_values):.2f} std={math.sqrt(sum((x - sum(correlation_values)/len(correlation_values))**2 for x in correlation_values) / len(correlation_values)):.2f} support_fraction={support_fraction:.2f}"
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)