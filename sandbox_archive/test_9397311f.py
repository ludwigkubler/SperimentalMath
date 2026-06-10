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
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def construct_phase_space(circuit):
        phase_space = []
        for entry in circuit:
            if entry[0] == 'AND':
                result = all(entry[1])
            else:  # OR
                result = any(entry[1])
            phase_space.append(result)
        return phase_space
    
    def symplectic_volume(phase_space):
        n = len(phase_space)
        volume = 0
        for i in range(n):
            for j in range(i+1, n):
                if phase_space[i] != phase_space[j]:
                    volume += 1
        return volume / (n * (n - 1) / 2)
    
    def correlation_coefficient(values, expected):
        mean_values = sum(values) / len(values)
        mean_expected = sum(expected) / len(expected)
        numerator = sum((v - mean_values) * (e - mean_expected) for v, e in zip(values, expected))
        denominator = math.sqrt(sum((v - mean_values)**2 for v in values)) * math.sqrt(sum((e - mean_expected)**2 for e in expected))
        return numerator / denominator if denominator != 0 else 0
    
    def mean_absolute_difference(values, expected):
        return sum(abs(v - e) for v, e in zip(values, expected)) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    volumes = []
    expected_volumes = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        phase_space = construct_phase_space(circuit)
        volume = symplectic_volume(phase_space)
        volumes.append(volume)
        expected_volumes.append(n * math.log2(n))
    
    correlation = correlation_coefficient(volumes, expected_volumes)
    mean_diff = mean_absolute_difference(volumes, expected_volumes)
    
    return {
        "metric_name": "symplectic_volume",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and mean_diff <= 3,
        "counterexample": "" if correlation >= 0.8 and mean_diff <= 3 else f"Correlation: {correlation}, Mean Absolute Difference: {mean_diff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")