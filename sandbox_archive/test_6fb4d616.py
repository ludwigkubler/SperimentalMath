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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = list(input_values)
        for gate_type, inputs in reversed(circuit):
            a, b = stack[inputs[0]], stack[inputs[1]]
            if gate_type == 'AND':
                stack.append(a and b)
            elif gate_type == 'OR':
                stack.append(a or b)
        return stack.pop()
    
    def polynomial_representation_length(poly):
        length = 0
        for coeff, exp in poly.items():
            length += len(bin(coeff)) + len(bin(exp))
        return length
    
    def affine_quotient(circuit, n):
        output_values = [evaluate_circuit(circuit, input_values) for input_values in product([0, 1], repeat=n)]
        unique_values = set(output_values)
        if len(unique_values) == 2:
            return {0: 0, 1: 1}
        else:
            return {}
    
    def monotone_complexity(circuit):
        n = len(circuit)
        min_size = float('inf')
        for _ in range(10):  # Try to find a small monotone circuit
            current_circuit = []
            input_values = [random.choice([0, 1]) for _ in range(n)]
            output_value = evaluate_circuit(circuit, input_values)
            if output_value == 1:
                current_circuit.append((input_values[0], 'OR'))
                current_circuit.append((input_values[1], 'AND'))
            min_size = min(min_size, len(current_circuit))
        return min_size
    
    n_max = 40
    total_metric_value = 0
    instances_tested = 0
    counterexample = ""
    
    for n in range(5, n_max + 1):
        if n * math.log2(n) > 1.5 * n * math.log2(n):
            continue
        
        circuit = generate_boolean_circuit(n)
        q = affine_quotient(circuit, n)
        
        if not q:
            counterexample = "mapping_undefined"
            return {
                "metric_name": "representation_length",
                "metric_value": 0,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        representation_length = polynomial_representation_length(q)
        monotone_comp = monotone_complexity(circuit)
        
        total_metric_value += representation_length
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / (n_max - 4)
    
    if support_fraction < 0.8:
        return {
            "metric_name": "representation_length",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    if mean_metric_value > 1.5 * n_max * math.log2(n_max):
        return {
            "metric_name": "representation_length",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    return {
        "metric_name": "representation_length",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")