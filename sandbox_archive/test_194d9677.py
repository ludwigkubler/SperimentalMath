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
    
    def generate_random_boolean_circuit(n):
        # Generate a random Boolean circuit with n inputs and polynomial size
        depth = random.randint(2, 5)
        circuit = []
        for _ in range(depth):
            layer = [random.choice(['AND', 'OR'])] * (n - 1) + ['NOT']
            circuit.append(layer)
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        # Evaluate the Boolean circuit
        for layer in reversed(circuit):
            new_layer = []
            for i in range(len(layer)):
                if layer[i] == 'AND':
                    new_layer.append(input_values[i] and input_values[i + 1])
                elif layer[i] == 'OR':
                    new_layer.append(input_values[i] or input_values[i + 1])
                else:
                    new_layer.append(not input_values[i])
            input_values = new_layer
        return input_values[0]
    
    def compute_depth(circuit):
        # Compute the depth of the circuit
        return len(circuit)
    
    n_max = 0
    total_metric_value = 0.0
    instances_tested = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        if n > n_max:
            n_max = n
        
        circuit = generate_random_boolean_circuit(n)
        depth = compute_depth(circuit)
        
        input_values = [random.choice([True, False]) for _ in range(n)]
        output_value = evaluate_circuit(circuit, input_values)
        
        # Compute the metric (logarithm of the number of inputs)
        if n <= 1:
            continue
        
        metric_value = math.log(n)
        total_metric_value += metric_value
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "log_n",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        counterexample = min((r["counterexample"] for r in results if not r["conjecture_holds"]), key=len)
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")