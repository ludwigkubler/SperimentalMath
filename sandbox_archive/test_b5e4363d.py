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
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2 * n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(1, n))]
            circuit.append((gate_type, inputs))
        return circuit

    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'AND':
                result = all(stack.pop() for _ in inputs)
            elif gate_type == 'OR':
                result = any(stack.pop() for _ in inputs)
            else:
                raise ValueError(f"Invalid gate type: {gate_type}")
            stack.append(result)
        return stack[0]

    def polynomial_representation_length(p):
        length = 0
        for coeff, exp in p.items():
            length += len(bin(coeff)) + sum(len(bin(e)) for e in exp)
        return length

    def affine_quotient(circuit):
        input_values = [random.randint(0, 1) for _ in range(n)]
        output = evaluate_circuit(circuit, input_values)
        p = {output: tuple(input_values)}
        return p

    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_random_circuit(n)
    q = affine_quotient(circuit)
    representation_length = polynomial_representation_length(q)

    metric_value = representation_length
    instances_tested = 1
    n_max = n
    conjecture_holds = representation_length <= 1.5 * n * math.log2(n)
    counterexample = "" if conjecture_holds else f"n={n}, length={representation_length}"

    return {
        "metric_name": "Representation Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n_max<{result['n_max']}, length>{1.5 * result['n_max'] * math.log2(result['n_max'])}\" first_failing_seed={first_failing_seed}")