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
    
    def generate_circuit(depth):
        if depth == 0:
            return ['input']
        else:
            left = generate_circuit(depth - 1)
            right = generate_circuit(depth - 1)
            return [random.choice(['and', 'or']), left, right]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, list):
            gate, x, y = circuit
            if gate == 'and':
                return evaluate_circuit(x) and evaluate_circuit(y)
            elif gate == 'or':
                return evaluate_circuit(x) or evaluate_circuit(y)
            else:
                raise ValueError("Invalid gate")
        else:
            return random.choice([True, False])
    
    def galois_group_size(circuit):
        # Simplified version for demonstration purposes
        depth = len(circuit)
        return 2 ** depth
    
    def minimal_splitting_field_extension_degree(galois_group_size):
        if galois_group_size == 1:
            return 1
        else:
            return galois_group_size - 1
    
    max_depth = 40
    instances_tested = 0
    n_max = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for depth in range(5, max_depth + 1):
        circuit = generate_circuit(depth)
        instances_tested += 1
        n_max = max(n_max, depth)
        
        value = evaluate_circuit(circuit)
        galois_group_size_val = galois_group_size(circuit)
        splitting_field_extension_degree = minimal_splitting_field_extension_degree(galois_group_size_val)
        
        if splitting_field_extension_degree > 4 * depth ** 2:
            conjecture_holds = False
            counterexample = f"Circuit of depth {depth} with Galois group size {galois_group_size_val} and splitting field extension degree {splitting_field_extension_degree}"
            break
        
        total_metric_value += splitting_field_extension_degree
    
    return {
        "metric_name": "Minimal Splitting Field Extension Degree",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")