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
        phase_space = set()
        n = len(circuit[0][1])
        for i in range(2**n):
            state = [i >> j & 1 for j in range(n)]
            phase_space.add(tuple(state))
        return phase_space
    
    def symplectic_volume(phase_space, n):
        volume = 0
        n_cells = 2**(n-1)
        for state in phase_space:
            if sum(state) % 2 == 0:
                volume += n_cells
            else:
                volume -= n_cells
        return abs(volume / (2**n))
    
    def correlation_coefficient(values, expected):
        mean_value = sum(values) / len(values)
        mean_expected = sum(expected) / len(expected)
        numerator = sum((v - mean_value) * (e - mean_expected) for v, e in zip(values, expected))
        denominator = math.sqrt(sum((v - mean_value)**2 for v in values)) * math.sqrt(sum((e - mean_expected)**2 for e in expected))
        return numerator / denominator
    
    def mean_absolute_difference(values, expected):
        return sum(abs(v - e) for v, e in zip(values, expected)) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    volumes = []
    expected_volumes = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        phase_space = construct_phase_space(circuit)
        volume = symplectic_volume(phase_space, n)
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
        "counterexample": "" if correlation >= 0.8 and mean_diff <= 3 else "correlation<0.8 or mean_diff>3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")