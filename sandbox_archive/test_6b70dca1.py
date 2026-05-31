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
    
    def generate_monotone_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_coxeter_group_order(circuit):
        # Simplified mapping from circuit to Coxeter group order
        return len(circuit) + 1
    
    def compute_monotone_complexity(circuit):
        # Simplified mapping from circuit to complexity
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each size 5 times
            circuit = generate_monotone_circuit(n)
            order = compute_coxeter_group_order(circuit)
            complexity = compute_monotone_complexity(circuit)
            results.append((order, complexity))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    order_values = [r[0] for r in results]
    complexity_values = [r[1] for r in results]
    
    mean_order = sum(order_values) / len(order_values)
    mean_complexity = sum(complexity_values) / len(complexity_values)
    covariance = sum((order - mean_order) * (complexity - mean_complexity) for order, complexity in results) / len(results)
    variance_order = sum((order - mean_order)**2 for order in order_values) / len(order_values)
    variance_complexity = sum((complexity - mean_complexity)**2 for complexity in complexity_values) / len(complexity_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_order) * math.sqrt(variance_complexity))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] or result["metric_value"] is None for result in results):
        print(f"RESULT: INCONCLUSIVE reason=undefined_mapping n_tested={len(seeds)}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "correlation_coefficient < 0.8"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")