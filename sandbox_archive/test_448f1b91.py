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
    
    def generate_random_circuit(n, d):
        if n <= 0 or d <= 0:
            return None, []
        
        circuit = []
        inputs = set()
        for _ in range(d):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                input_index = random.randint(0, len(inputs) - 1)
                inputs.remove(input_index)
                output_index = len(inputs)
                inputs.add(output_index)
                circuit.append((gate_type, input_index))
            else:
                input_indices = [random.randint(0, len(inputs) - 1) for _ in range(2)]
                inputs.difference_update(input_indices)
                output_index = len(inputs)
                inputs.add(output_index)
                circuit.append((gate_type, input_indices[0], input_indices[1]))
        return circuit, list(inputs)

    def evaluate_circuit(circuit):
        if not circuit:
            return None
        
        stack = []
        for gate in reversed(circuit):
            if gate[0] == 'NOT':
                right = stack.pop()
                stack.append(not right)
            else:
                right = stack.pop()
                left = stack.pop()
                if gate[0] == 'AND':
                    stack.append(left and right)
                elif gate[0] == 'OR':
                    stack.append(left or right)
        return stack[0]

    def hdim(V):
        # Placeholder for Hodge-De Rham cohomology dimension calculation
        # This is a dummy implementation that returns the number of inputs as an example
        return len(V)

    def entanglement_complexity(n, d):
        # Placeholder for entanglement complexity calculation
        # This is a dummy implementation that returns n * d as an example
        return n * d

    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        d = random.randint(1, 40)
        circuit, inputs = generate_random_circuit(n, d)
        if circuit is None:
            continue
        V = evaluate_circuit(circuit)
        if V is None:
            continue
        hdim_value = hdim(V)
        e_phi = entanglement_complexity(n, d)
        results.append((hdim_value, e_phi))

    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }

    hdim_values = [r[0] for r in results]
    e_phi_values = [r[1] for r in results]

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        return cov_xy / (std_x * std_y)

    correlation_coefficient = pearson_correlation(hdim_values, e_phi_values)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")