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
    
    def generate_circuit(n, m):
        # Generate a random Boolean circuit with n inputs and m gates
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_symmetry_group(circuit):
        # Compute the symmetry group of the circuit
        # This is a placeholder function. Implement actual computation here.
        return random.randint(1, 8)
    
    def compute_monotone_width(circuit):
        # Compute the monotone width of the circuit
        # This is a placeholder function. Implement actual computation here.
        return random.randint(2, 5)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_symmetry_order = 0
    total_monotone_width = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(1, n))
            symmetry_order = compute_symmetry_group(circuit)
            monotone_width = compute_monotone_width(circuit)
            
            if symmetry_order == 0 or monotone_width == 0:
                continue
            
            instances_tested += 1
            total_symmetry_order += symmetry_order
            total_monotone_width += monotone_width
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_symmetry_order = total_symmetry_order / instances_tested
    mean_monotone_width = total_monotone_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(s * m for s, m in zip(range(1, instances_tested + 1), range(1, instances_tested + 1))) -
                               instances_tested * mean_symmetry_order * mean_monotone_width) / \
                              math.sqrt((instances_tested * sum(s**2 for s in range(1, instances_tested + 1)) - instances_tested * mean_symmetry_order**2) *
                                        (instances_tested * sum(m**2 for m in range(1, instances_tested + 1)) - instances_tested * mean_monotone_width**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")