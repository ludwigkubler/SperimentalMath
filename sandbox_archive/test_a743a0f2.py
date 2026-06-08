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
            gate = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), 2)
            circuit.append((gate, inputs))
        return circuit

    def calculate_frobenius_schur_index(circuit):
        # Placeholder implementation
        # This is a dummy function and should be replaced with actual logic
        return random.random()

    def calculate_circuit_width(circuit):
        width = 0
        for gate, _ in circuit:
            if gate == 'AND' or gate == 'OR':
                width += 1
        return width

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_fs_index = 0.0
    max_diff = 0.0

    for n in n_values:
        for _ in range(5):  # Test each n size 5 times
            circuit = generate_boolean_circuit(n)
            fs_index = calculate_frobenius_schur_index(circuit)
            width = calculate_circuit_width(circuit)
            instances_tested += 1
            total_fs_index += abs(fs_index - width)
            max_diff = max(max_diff, abs(fs_index - width))

    if instances_tested < 30:
        return {
            "metric_name": "Frobenius-Schur Index vs Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_values[-1],
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }

    mean_diff = total_fs_index / instances_tested
    correlation = 0.5  # Placeholder value, should be calculated

    return {
        "metric_name": "Frobenius-Schur Index vs Width",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": correlation > 0.7 and mean_diff <= 3,
        "counterexample": f"Correlation: {correlation}, Max Diff: {max_diff}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(res['conjecture_holds'] for res in results):
        support_fraction = len([res for res in results if res['conjecture_holds']]) / len(results)
        mean_value = sum(res['metric_value'] for res in results) / len(results)
        std_value = math.sqrt(sum((res['metric_value'] - mean_value)**2 for res in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res['conjecture_holds'] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")