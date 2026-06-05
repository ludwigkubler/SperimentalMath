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

def generate_random_circuit(n, depth):
    circuit = []
    for _ in range(depth):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate_type, inputs))
    return circuit

def compute_polynomial_representation(circuit):
    n = len(circuit[0][1])
    poly_rep = [[0] * (2 ** n) for _ in range(n + 1)]
    
    def evaluate(gate_type, inputs):
        if gate_type == 'AND':
            return all(inputs)
        elif gate_type == 'OR':
            return any(inputs)
        else:
            raise ValueError("Invalid gate type")
    
    for i in range(2 ** n):
        input_vals = [(i >> j) & 1 for j in range(n)]
        result = evaluate(circuit[0][0], circuit[0][1])
        poly_rep[0][i] = result
    
    for layer in range(1, len(circuit)):
        gate_type, inputs = circuit[layer]
        for i in range(2 ** n):
            input_vals = [(i >> j) & 1 for j in range(n)]
            result = evaluate(gate_type, input_vals)
            poly_rep[layer][i] = result
    
    return poly_rep

def compute_frobenius_norm(poly_rep):
    n = len(poly_rep[0])
    norm = 0
    for i in range(n):
        norm += sum(x * x for x in poly_rep[i]) ** Fraction(1, 2)
    return norm

def compute_monotone_width(circuit):
    n = len(circuit[0][1])
    width = 0
    
    def is_monotone(gate_type, inputs):
        if gate_type == 'AND':
            return all(inputs)
        elif gate_type == 'OR':
            return any(inputs)
        else:
            raise ValueError("Invalid gate type")
    
    for i in range(2 ** n):
        input_vals = [(i >> j) & 1 for j in range(n)]
        if is_monotone(circuit[0][0], circuit[0][1]):
            width += 1
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_random_circuit(n, depth=3)
        poly_rep = compute_polynomial_representation(circuit)
        frobenius_norm = compute_frobenius_norm(poly_rep)
        monotone_width = compute_monotone_width(circuit)
        
        results.append({
            "n": n,
            "frobenius_norm": frobenius_norm,
            "monotone_width": monotone_width
        })
    
    correlation_sum = 0
    for i in range(len(n_values)):
        for j in range(i + 1, len(n_values)):
            n1, n2 = n_values[i], n_values[j]
            frobenius_norm1, frobenius_norm2 = results[i]["frobenius_norm"], results[j]["frobenius_norm"]
            monotone_width1, monotone_width2 = results[i]["monotone_width"], results[j]["monotone_width"]
            
            if frobenius_norm1 == 0 or frobenius_norm2 == 0:
                correlation_sum += 0
            else:
                correlation_sum += (frobenius_norm1 * monotone_width2 - frobenius_norm2 * monotone_width1) / (frobenius_norm1 * frobenius_norm2)
    
    mean_correlation = correlation_sum / (len(n_values) * (len(n_values) - 1))
    conjecture_holds = mean_correlation >= 0.8
    counterexample = "" if conjecture_holds else "correlation_too_low"
    
    return {
        "metric_name": "mean_correlation",
        "metric_value": mean_correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")