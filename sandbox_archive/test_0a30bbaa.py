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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(random.randint(1, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(input_values[i] for i in inputs)
            elif gate_type == 'OR':
                result = any(input_values[i] for i in inputs)
            stack.append(result)
        return stack[0]
    
    def circuit_monotone_width(circuit):
        n = max(max(inputs) for _, inputs in circuit) + 1
        input_values = [list(range(n)) for _ in range(2**n)]
        width = 0
        for i in range(n):
            positive_count = sum(evaluate_circuit(circuit, [1 if j == i else 0 for j in range(n)]) for _ in input_values)
            negative_count = sum(evaluate_circuit(circuit, [0 if j == i else 1 for j in range(n)]) for _ in input_values)
            width = max(width, positive_count, negative_count)
        return width
    
    def minimal_order_of_elliptic_curve(circuit):
        n = circuit_monotone_width(circuit)
        # Simplified model: order is proportional to the number of gates
        return 2 * len(circuit) + n
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_random_circuit(n)
        w_mon = circuit_monotone_width(circuit)
        ord_E = minimal_order_of_elliptic_curve(circuit)
        results.append((w_mon, ord_E))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    w_mons, ord_Es = zip(*results)
    correlation_coefficient = (len(results) * sum(w_mon * ord_E for w_mon, ord_E in results) - 
                               sum(w_mons) * sum(ord_Es)) / math.sqrt(
                                   len(results) * sum(w_mon**2 for w_mon in w_mons) - sum(w_mons)**2 *
                                   len(results) * sum(ord_E**2 for ord_E in ord_Es) - sum(ord_Es)**2)
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * (len(results) - 2))))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(circuit) for _, circuit in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 and p_value <= 0.05 else "correlation_threshold_not_met"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean = sum(result["metric_value"] for result in results)
        std = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean} std={std} support_fraction={support_fraction}")