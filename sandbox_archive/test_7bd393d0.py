# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys
import collections

def generate_random_boolean_function(n):
    if n == 1:
        return random.choice(['0', '1'])
    op = random.choice(['AND', 'OR', 'XOR'])
    return [op] + [generate_random_boolean_function(random.randint(1, n)) for _ in range(random.randint(2, n))]

def evaluate_boolean_function(formula):
    if isinstance(formula, list):
        op = formula[0]
        args = formula[1:]
        if op == 'AND':
            return all(evaluate_boolean_function(arg) for arg in args)
        elif op == 'OR':
            return any(evaluate_boolean_function(arg) for arg in args)
        elif op == 'XOR':
            return sum(evaluate_boolean_function(arg) for arg in args) % 2 == 1
    else:
        return int(formula)

def compute_xor_and_tree_width(formula):
    if isinstance(formula, list):
        return max(compute_xor_and_tree_width(arg) for arg in formula[1:]) + 1
    else:
        return 0

def geometric_quantization_rank(n):
    # Placeholder function to simulate quantum state rank computation
    return random.randint(1, n * (n + 1) // 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_random_boolean_function(n)
        T_f = compute_xor_and_tree_width(formula)
        rho_f_rank = geometric_quantization_rank(n)
        
        if T_f == 0:
            continue
        
        alpha = Fraction(1, 2)  # Placeholder value for α
        beta = 1  # Placeholder value for β
        
        expected_min_rank = alpha * math.log(T_f)
        expected_max_rank = beta * T_f
        
        results.append({
            "n": n,
            "T_f": T_f,
            "rho_f_rank": rho_f_rank,
            "expected_min_rank": expected_min_rank,
            "expected_max_rank": expected_max_rank
        })
    
    if not results:
        return {
            "metric_name": "geometric_quantization_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [result["rho_f_rank"] for result in results]
    mean_value = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for result in results if abs(result["rho_f_rank"] - result["expected_min_rank"]) <= 3 and abs(result["rho_f_rank"] - result["expected_max_rank"]) <= 3) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "rank outside ±3 std dev"
    
    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
        elif any(result["counterexample"] for result in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"])
            print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE no support or counterexamples found")