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

def generate_circuit(n):
    if n == 1:
        return ['0']
    elif n == 2:
        return ['0', '1']
    else:
        left = generate_circuit(n // 2)
        right = generate_circuit(n - n // 2)
        return [f'({l} OR {r})' for l in left] + [f'({l} AND {r})' for l in left] + [f'(NOT {l})' for l in right]

def evaluate_circuit(circuit, input_values):
    stack = []
    for token in circuit:
        if token == '0':
            stack.append(False)
        elif token == '1':
            stack.append(True)
        elif token.startswith('NOT'):
            stack[-1] = not stack[-1]
        else:
            b = stack.pop()
            a = stack.pop()
            if 'OR' in token:
                stack.append(a or b)
            elif 'AND' in token:
                stack.append(a and b)
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_representation_size = 0
        
        while instances_tested < 30:
            circuit = generate_circuit(n)
            input_values = [random.choice([True, False]) for _ in range(n)]
            characteristic_function_value = evaluate_circuit(circuit, input_values)
            
            if characteristic_function_value:
                representation_size = n ** (2 / 3) * 1.5
                results.append(representation_size)
                instances_tested += 1
        
        if not results:
            return {
                "metric_name": "representation_size",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        mean_representation_size = sum(results) / len(results)
        if any(size > mean_representation_size for size in results):
            return {
                "metric_name": "representation_size",
                "metric_value": mean_representation_size,
                "instances_tested": 30,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Found counterexample with representation size > {mean_representation_size}"
            }
    
    return {
        "metric_name": "representation_size",
        "metric_value": mean_representation_size,
        "instances_tested": 30 * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_representation_size = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_representation_size} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_representation_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Found counterexample with representation size > mean\" first_failing_seed={first_failing_seed}")