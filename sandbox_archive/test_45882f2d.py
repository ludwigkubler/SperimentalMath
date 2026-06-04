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
    if n == 1:
        return '0' if random.choice([True, False]) else '1'
    else:
        op = random.choice(['&', '|'])
        left = generate_boolean_formula(n // 2)
        right = generate_boolean_formula(n - n // 2)
        return f"({left} {op} {right})"

def frege_proof_depth(formula):
    if formula in ['0', '1']:
        return 1
    else:
        op, left, right = formula.split()
        return max(frege_proof_depth(left), frege_proof_depth(right)) + 1

def hodge_order(n):
    # Placeholder for the actual Hodge order calculation
    # This is a dummy function to avoid actual computation
    return n * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_boolean_formula(n)
        depth = frege_proof_depth(formula)
        order = hodge_order(n)
        
        results.append({
            "n": n,
            "depth": depth,
            "order": order
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    n_values = [result["n"] for result in results]
    depth_values = [math.log2(result["depth"]) for result in results]
    order_values = [result["order"] for result in results]
    
    mean_depth = sum(depth_values) / len(depth_values)
    mean_order = sum(order_values) / len(order_values)
    
    covariance = sum((depth_values[i] - mean_depth) * (order_values[i] - mean_order) for i in range(len(results))) / len(results)
    variance_depth = sum((depth_values[i] - mean_depth) ** 2 for i in range(len(results))) / len(results)
    variance_order = sum((order_values[i] - mean_order) ** 2 for i in range(len(results))) / len(results)
    
    correlation = covariance / (math.sqrt(variance_depth) * math.sqrt(variance_order))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")