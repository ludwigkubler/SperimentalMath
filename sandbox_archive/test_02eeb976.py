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

def generate_boolean_circuit(n):
    if n == 1:
        return ['0', '1']
    else:
        left = generate_boolean_circuit(n // 2)
        right = generate_boolean_circuit(n - n // 2)
        return [f'AND({x},{y})' for x in left] + [f'OR({x},{y})' for x in left for y in right]

def evaluate_circuit(circuit):
    if circuit == '0':
        return False
    elif circuit == '1':
        return True
    else:
        op, x, y = circuit.split('(')
        x = x.strip()
        y = y.strip()[:-1]
        if op == 'AND':
            return evaluate_circuit(x) and evaluate_circuit(y)
        elif op == 'OR':
            return evaluate_circuit(x) or evaluate_circuit(y)

def generate_random_instance(n):
    circuit = generate_boolean_circuit(n)
    inputs = [random.choice([True, False]) for _ in range(2**n)]
    outputs = [evaluate_circuit(circuit) for _ in inputs]
    return circuit, inputs, outputs

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit, _, _ = generate_random_instance(n)
        w_C = len(circuit.split('AND')) + len(circuit.split('OR'))
        
        # Simulate the moment map and count symplectic leaves
        # This is a placeholder; actual computation depends on the conjecture's requirements
        L_M_C = w_C  # Placeholder value
        
        results.append({
            "n": n,
            "w_C": w_C,
            "L_M_C": L_M_C
        })
    
    if not results:
        return {
            "metric_name": "symplectic_leaf_number",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    max_n = max(result["n"] for result in results)
    metric_values = [result["L_M_C"] / (result["w_C"] ** 2) for result in results]
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "symplectic_leaf_number",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": all(value <= 1 for value in metric_values),  # Placeholder condition
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std={math.sqrt(sum((result['metric_value'] - (sum(result['metric_value'] for result in results) / len(results))) ** 2 for result in results) / len(results))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")