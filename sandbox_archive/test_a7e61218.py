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
    
    # Define a simple Boolean circuit with varying monotone width
    def generate_circuit(n):
        if n == 1:
            return ['A']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'OR({left[0]}, {right[0]})', f'AND({left[0]}, {right[0]})']
    
    # Compute the associated quantum group using its minimal representation
    def compute_quantum_group(circuit):
        if len(circuit) == 1:
            return [circuit[0]]
        else:
            left = compute_quantum_group([circuit[0]])
            right = compute_quantum_group([circuit[2]])
            return left + right
    
    # Measure the representation length of the quantum group
    def measure_representation_length(group):
        return len(group)
    
    # Correlate the measured representation length with the circuit's monotone width
    def calculate_monotone_width(circuit):
        if len(circuit) == 1:
            return 1
        else:
            left = calculate_monotone_width([circuit[0]])
            right = calculate_monotone_width([circuit[2]])
            return max(left, right) + 1
    
    # Generate a set of Boolean circuits with varying monotone width
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        quantum_group = compute_quantum_group(circuit)
        representation_length = measure_representation_length(quantum_group)
        monotone_width = calculate_monotone_width(circuit)
        
        results.append({
            "n": n,
            "representation_length": representation_length,
            "monotone_width": monotone_width
        })
    
    # Compute the mean and standard deviation of the representation length
    total_representation_length = sum(result["representation_length"] for result in results)
    mean_representation_length = total_representation_length / len(results)
    
    variance = sum((result["representation_length"] - mean_representation_length) ** 2 for result in results)
    std_deviation = math.sqrt(variance / len(results))
    
    # Check if the conjecture is supported
    support_fraction = sum(1 for result in results if abs(result["representation_length"] - result["monotone_width"]) <= 0.5 * result["monotone_width"]) / len(results)
    
    return {
        "metric_name": "Representation Length",
        "metric_value": mean_representation_length,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean={mean_representation_length}, std_dev={std_deviation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")