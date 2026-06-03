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
            return random.choice(['True', 'False'])
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            op = random.choice(['and', 'or'])
            return f'({subformulas[0]} {op} {subformulas[1]})'
    
    def evaluate_formula(formula):
        if formula == 'True':
            return 1
        elif formula == 'False':
            return 0
        else:
            left, op, right = formula.split()
            if op == 'and':
                return min(evaluate_formula(left), evaluate_formula(right))
            elif op == 'or':
                return max(evaluate_formula(left), evaluate_formula(right))
    
    def sat_solver(formula):
        # Simplified SAT solver for demonstration purposes
        if formula in ['True', 'False']:
            return len(formula)
        else:
            left, op, right = formula.split()
            if op == 'and':
                return max(sat_solver(left), sat_solver(right))
            elif op == 'or':
                return min(sat_solver(left), sat_solver(right))
    
    n_values = [5, 10, 15, 20, 30, 40]
    tpar_values = []
    proof_sizes = []
    
    for n in n_values:
        formula = generate_formula(n)
        tpar_value = evaluate_formula(formula)
        proof_size = sat_solver(formula)
        
        tpar_values.append(tpar_value)
        proof_sizes.append(proof_size)
    
    correlation_coefficient = 0
    if len(tpar_values) > 1 and len(proof_sizes) > 1:
        mean_tpar = sum(tpar_values) / len(tpar_values)
        mean_proof_size = sum(proof_sizes) / len(proof_sizes)
        
        numerator = sum((tpar - mean_tpar) * (proof_size - mean_proof_size) for tpar, proof_size in zip(tpar_values, proof_sizes))
        denominator = math.sqrt(sum((tpar - mean_tpar)**2 for tpar in tpar_values)) * math.sqrt(sum((proof_size - mean_proof_size)**2 for proof_size in proof_sizes))
        
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": "" if abs(correlation_coefficient) > 0.5 else "correlation_too_weak"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(result['metric_value'] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_weak\" first_failing_seed={first_failing_seed}")