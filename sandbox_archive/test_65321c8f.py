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
    
    def generate_circuit(n, m):
        # Generate a random Boolean circuit with n inputs and m gates
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                input_index = random.randint(0, n-1)
                circuit.append((gate_type, input_index))
            else:
                input_indices = [random.randint(0, n-1) for _ in range(2)]
                circuit.append((gate_type, input_indices))
        return circuit
    
    def compute_symmetry_group(circuit):
        # Compute the symmetry group of the circuit
        # This is a placeholder function; actual implementation required
        return 1  # Placeholder value
    
    def compute_monotone_width(circuit):
        # Compute the monotone width of the circuit
        # This is a placeholder function; actual implementation required
        return 1  # Placeholder value
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n, random.randint(2*n, 3*n))
            symmetry_group_order = compute_symmetry_group(circuit)
            monotone_width = compute_monotone_width(circuit)
            results.append((symmetry_group_order, monotone_width))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    symmetry_group_orders = [r[0] for r in results]
    monotone_widths = [r[1] for r in results]
    
    n = len(symmetry_group_orders)
    mean_symmetry_group_order = sum(symmetry_group_orders) / n
    mean_monotone_width = sum(monotone_widths) / n
    
    covariance = sum((symmetry_group_orders[i] - mean_symmetry_group_order) * (monotone_widths[i] - mean_monotone_width) for i in range(n)) / n
    variance_symmetry_group_order = sum((symmetry_group_orders[i] - mean_symmetry_group_order) ** 2 for i in range(n)) / n
    variance_monotone_width = sum((monotone_widths[i] - mean_monotone_width) ** 2 for i in range(n)) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_symmetry_group_order) * math.sqrt(variance_monotone_width))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")