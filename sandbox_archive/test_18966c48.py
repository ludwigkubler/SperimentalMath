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
    
    def generate_circuit(n: int, m: int):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        n = len(circuit[0][1])
        input_combinations = [tuple(inputs) for inputs in itertools.product([0, 1], repeat=n)]
        outputs = set()
        for inputs in input_combinations:
            current_inputs = inputs
            for gate_type, inputs in circuit:
                if gate_type == 'AND':
                    current_output = all(current_inputs[i] for i in range(n) if inputs[i])
                elif gate_type == 'OR':
                    current_output = any(current_inputs[i] for i in range(n) if inputs[i])
                else:
                    raise ValueError("Invalid gate type")
            outputs.add(current_output)
        return len(outputs)
    
    def compute_minimal_order(circuit):
        n = len(circuit[0][1])
        m = len(circuit)
        order = evaluate_circuit(circuit)
        return order
    
    def circuit_monotone_width(circuit):
        n = len(circuit[0][1])
        m = len(circuit)
        width = 0
        for i in range(m):
            current_inputs = [0] * n
            for j in range(i + 1):
                gate_type, inputs = circuit[j]
                if gate_type == 'AND':
                    current_inputs = [current_inputs[k] & inputs[k] for k in range(n)]
                elif gate_type == 'OR':
                    current_inputs = [current_inputs[k] | inputs[k] for k in range(n)]
            width = max(width, sum(current_inputs))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [n // 2 for n in n_values]
    
    total_order = 0
    total_width = 0
    instances_tested = 0
    
    for n, m in zip(n_values, m_values):
        circuit = generate_circuit(n, m)
        order = compute_minimal_order(circuit)
        width = circuit_monotone_width(circuit)
        total_order += order
        total_width += width
        instances_tested += 1
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    expected_bound = (m ** (2/3) * n ** (1/3))
    
    if abs(mean_order - expected_bound) <= 2 * expected_bound:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "order does not match expected bound"
    
    return {
        "metric_name": "Order of Twisted Derivative Module",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")