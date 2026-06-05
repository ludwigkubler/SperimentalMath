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
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with n inputs
        circuit = []
        for _ in range(2**n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_polynomial_representation(circuit):
        # Compute the polynomial representation of the circuit
        n = len(circuit[0][1])
        poly_rep = [0] * (2**n)
        for gate in reversed(circuit):
            gate_type, inputs = gate
            if gate_type == 'AND':
                result = 1
                for input_val in inputs:
                    result *= input_val
                poly_rep[result] += 1
            elif gate_type == 'OR':
                result = 0
                for input_val in inputs:
                    result |= input_val
                poly_rep[result] += 1
        return poly_rep
    
    def compute_frobenius_norm(poly_rep):
        # Compute the Frobenius norm of the polynomial representation
        sum_of_squares = sum(x**2 for x in poly_rep)
        frobenius_norm = math.sqrt(sum_of_squares)
        return frobenius_norm
    
    def compute_monotone_width(circuit):
        # Compute the monotone width of the circuit
        n = len(circuit[0][1])
        max_width = 0
        for i in range(2**n):
            width = sum(1 for gate in circuit if all(input_val == 1 for input_val in gate[1] if i & (1 << j) != 0))
            max_width = max(max_width, width)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        poly_rep = compute_polynomial_representation(circuit)
        frobenius_norm = compute_frobenius_norm(poly_rep)
        monotone_width = compute_monotone_width(circuit)
        results.append((frobenius_norm, monotone_width))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_sum = 0
    for i in range(30):
        frobenius_norm_i, monotone_width_i = results[i]
        frobenius_norm_j, monotone_width_j = results[(i + 1) % 30]
        correlation_sum += (frobenius_norm_i - frobenius_norm_j) * (monotone_width_i - monotone_width_j)
    
    n_pairs = 30 * 29 // 2
    mean_correlation = correlation_sum / n_pairs
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": mean_correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")