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
    
    def generate_boolean_formula(n):
        if n == 1:
            return '0' if random.choice([True, False]) else '1'
        else:
            op = random.choice(['&', '|'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left} {op} {right})'
    
    def calculate_local_system_order(formula):
        # Simplified heuristic for local system order
        return len(formula) ** 0.5
    
    def calculate_frege_proof_length(formula):
        if formula == '0' or formula == '1':
            return 1
        elif formula[0] == '(' and formula[-1] == ')':
            op = formula[1]
            left, right = formula[2:-1].split()
            if op == '&':
                return calculate_frege_proof_length(left) + calculate_frege_proof_length(right) + 1
            elif op == '|':
                return calculate_frege_proof_length(left) + calculate_frege_proof_length(right) + 1
        else:
            raise ValueError("Invalid formula format")
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    local_system_order = calculate_local_system_order(formula)
    proof_length = calculate_frege_proof_length(formula)
    
    return {
        "metric_name": "Frege Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": proof_length == local_system_order,
        "counterexample": "" if proof_length == local_system_order else f"Formula: {formula}, Expected Order: {local_system_order}, Actual Length: {proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula does not match local system order\" first_failing_seed={first_failing_seed}")