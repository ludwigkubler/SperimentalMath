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

def generate_random_circuit(n):
    circuit = []
    for _ in range(2 * n - 1):
        gate = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(2 if gate == 'AND' else 1)]
        circuit.append((gate, inputs))
    return circuit

def evaluate_circuit(circuit, input_values):
    stack = []
    for gate, inputs in circuit:
        if gate == 'AND':
            a, b = inputs
            stack.append(a and b)
        elif gate == 'OR':
            a = inputs[0]
            stack.append(a or input_values[1])
    return stack.pop()

def threshold_function(circuit, indicator):
    input_values = [indicator[i] for i in range(len(indicator))]
    return evaluate_circuit(circuit, input_values) >= 0.5

def count_ramanujan_matrices(circuit):
    n = len(circuit)
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 4
    # Placeholder for actual Ramanujan matrix counting logic
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 30
    total_ramanujan_matrices = 0
    n_max = 0

    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_random_circuit(n)
        indicator = [random.randint(0, 1) for _ in range(n)]
        if threshold_function(circuit, indicator):
            total_ramanujan_matrices += count_ramanujan_matrices(circuit)
        n_max = max(n_max, n)

    metric_value = total_ramanujan_matrices / instances_tested
    conjecture_holds = False  # Placeholder for actual conjecture check logic
    counterexample = ""

    return {
        "metric_name": "#RamanujanMatrices",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")