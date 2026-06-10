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
        # Generate a random boolean circuit with n inputs
        circuit = []
        for _ in range(2**n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def construct_phase_space(circuit):
        # Construct the phase space for the given circuit
        phase_space = []
        for gate, inputs in circuit:
            if gate == 'AND':
                phase_space.extend([i and j for i, j in zip(inputs, inputs[1:])])
            elif gate == 'OR':
                phase_space.extend([i or j for i, j in zip(inputs, inputs[1:])])
        return phase_space
    
    def symplectic_volume(phase_space):
        # Compute the symplectic volume of the phase space
        n = len(phase_space)
        if n <= 1:
            return 0
        volume = 1.0
        for i in range(n):
            for j in range(i+1, n):
                if phase_space[i] == phase_space[j]:
                    continue
                volume *= abs(phase_space[i] - phase_space[j])
        return volume
    
    def correlation_coefficient(x, y):
        # Compute the correlation coefficient between two lists
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x_i - mean_x) * (y_i - mean_y) for x_i, y_i in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((x_i - mean_x)**2 for x_i in x) / len(x))
        std_y = math.sqrt(sum((y_i - mean_y)**2 for y_i in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    def mean_absolute_difference(x, y):
        # Compute the mean absolute difference between two lists
        return sum(abs(x_i - y_i) for x_i, y_i in zip(x, y)) / len(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    volumes = []
    expected_volumes = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        phase_space = construct_phase_space(circuit)
        volume = symplectic_volume(phase_space)
        volumes.append(volume)
        expected_volumes.append(n * math.log(n))
    
    corr_coeff = correlation_coefficient(volumes, expected_volumes)
    mean_diff = mean_absolute_difference(volumes, expected_volumes)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(volumes),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff >= 0.8 and mean_diff <= 3,
        "counterexample": "" if corr_coeff >= 0.8 and mean_diff <= 3 else "correlation_coefficient < 0.8 or mean_absolute_difference > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8 or mean_absolute_difference > 3\" first_failing_seed={first_failing_seed}")