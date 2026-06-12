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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            op = random.choice(['&', '|'])
            return f'({subformulas[0]} {op} {subformulas[1]})'
    
    def evaluate(formula):
        if formula == '0':
            return 0
        elif formula == '1':
            return 1
        else:
            op_index = formula.find(' ')
            left, right = formula[:op_index], formula[op_index+2:]
            op = formula[op_index+1]
            if op == '&':
                return evaluate(left) & evaluate(right)
            elif op == '|':
                return evaluate(left) | evaluate(right)
    
    def hypergeometric_function_rank(formula):
        # Placeholder implementation for demonstration
        return len(formula.split())
    
    def resolution_proof_size(formula):
        # Simplified DPLL solver for demonstration
        if formula == '0':
            return 1
        elif formula == '1':
            return 1
        else:
            op_index = formula.find(' ')
            left, right = formula[:op_index], formula[op_index+2:]
            op = formula[op_index+1]
            if op == '&':
                return resolution_proof_size(left) + resolution_proof_size(right)
            elif op == '|':
                return max(resolution_proof_size(left), resolution_proof_size(right))
    
    n_max = 0
    metric_values = []
    for _ in range(30):
        n = random.randint(5, 40)
        if n > n_max:
            n_max = n
        formula = generate_formula(n)
        hfr = hypergeometric_function_rank(formula)
        size_resolution = resolution_proof_size(formula)
        metric_values.append(abs(hfr - size_resolution))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(abs(x) <= 3 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "abs_diff",
        "metric_value": mean_value,
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 10 for r in results):
        first_failing_seed = next((r["seed"] for r in results if abs(r["metric_value"]) > 10), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")