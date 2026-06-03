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
            return 'x'
        else:
            left = generate_formula(random.randint(1, n-1))
            right = generate_formula(n - len(left.split()))
            op = random.choice(['&', '|'])
            return f'({left}) {op} ({right})'
    
    def evaluate_formula(formula):
        if formula == 'x':
            return 1
        elif formula[0] == '(' and formula[-1] == ')':
            left, op, right = formula[1:-1].split()
            if op == '&':
                return min(evaluate_formula(left), evaluate_formula(right))
            else:
                return max(evaluate_formula(left), evaluate_formula(right))
        else:
            raise ValueError("Invalid formula")
    
    def sat_solver(formula):
        if formula == 'x':
            return 1
        elif formula[0] == '(' and formula[-1] == ')':
            left, op, right = formula[1:-1].split()
            if op == '&':
                return min(sat_solver(left), sat_solver(right))
            else:
                return max(sat_solver(left), sat_solver(right))
        else:
            raise ValueError("Invalid formula")
    
    n_max = 40
    instances_tested = 0
    tpar_values = []
    proof_sizes = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            formula = generate_formula(n)
            tpar_value = evaluate_formula(formula)
            proof_size = sat_solver(formula)
            
            tpar_values.append(tpar_value)
            proof_sizes.append(proof_size)
            instances_tested += 1
    
    correlation_coefficient = sum((tpar_values[i] - mean_tpar) * (proof_sizes[i] - mean_proof_size) for i in range(instances_tested)) / instances_tested
    mean_tpar = sum(tpar_values) / instances_tested
    mean_proof_size = sum(proof_sizes) / instances_tested
    
    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.5"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")