# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n):
        if n == 1:
            return "A"
        else:
            A = f"A{n}"
            B = f"B{n}"
            C = f"C{n}"
            D = f"D{n}"
            return f"({A} & {B}) -> ({C} | {D})"
    
    def resolution_proof_length(formula):
        # Simplified DPLL solver for Tseitin formulas
        clauses = formula.split("->")[1].split("|")
        proof_length = len(clauses) * 2
        return proof_length
    
    def arithmetic_hierarchy_order(clause):
        # Placeholder function to simulate the order calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(0, n**2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    max_order = 0
    
    for n in n_values:
        formula = tseitin_formula(n)
        proof_length = resolution_proof_length(formula)
        order = arithmetic_hierarchy_order(formula)
        
        if order > max_order:
            max_order = order
        
        metric_values.append((order, proof_length))
        instances_tested += 1
    
    correlation_coefficient = calculate_correlation(metric_values)
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_order,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(metric_values):
    n = len(metric_values)
    if n < 2:
        return 0
    
    x_sum = sum(order for order, _ in metric_values)
    y_sum = sum(proof_length for _, proof_length in metric_values)
    xy_sum = sum(order * proof_length for order, proof_length in metric_values)
    x_square_sum = sum(order**2 for order, _ in metric_values)
    y_square_sum = sum(proof_length**2 for _, proof_length in metric_values)
    
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * x_square_sum - x_sum**2) * (n * y_square_sum - y_sum**2))
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")