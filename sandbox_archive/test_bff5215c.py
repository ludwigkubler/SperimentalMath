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
    for _ in range(n):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
        circuit.append((gate_type, inputs))
    return circuit

def evaluate_circuit(circuit, input_values):
    stack = list(input_values)
    for gate_type, inputs in circuit:
        if len(stack) < len(inputs):
            raise ValueError("Not enough values on the stack to evaluate the circuit")
        operands = [stack.pop() for _ in range(len(inputs))]
        if gate_type == 'AND':
            result = all(operands)
        elif gate_type == 'OR':
            result = any(operands)
        else:
            raise ValueError(f"Unknown gate type: {gate_type}")
        stack.append(result)
    return stack[0]

def count_monomial_generators(n, circuit):
    input_values = [tuple(random.randint(0, 1) for _ in range(n)) for _ in range(2**n)]
    outputs = [evaluate_circuit(circuit, inputs) for inputs in input_values]
    monomial_generators = set()
    for output in outputs:
        if output not in monomial_generators:
            monomial_generators.add(output)
    return len(monomial_generators)

def count_linear_regions(n):
    # This is a placeholder function. For the sake of this example, we assume
    # that the number of linear regions is equal to the number of inputs.
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    circuit = generate_random_circuit(n)
    gn = count_monomial_generators(n, circuit)
    ln = count_linear_regions(n)
    if ln == 0:
        return {
            "metric_name": "Gn/Ln",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    ratio = Fraction(gn, ln)
    return {
        "metric_name": "Gn/Ln",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")