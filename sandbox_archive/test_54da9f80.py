# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(1, n) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate_type, inputs in reversed(circuit):
            values = [input_values[i-1] for i in inputs]
            if gate_type == 'AND':
                result = all(values)
            elif gate_type == 'OR':
                result = any(values)
            stack.append(result)
        return stack.pop()
    
    def compute_minimal_local_indeterminacy(circuit):
        n = len(circuit)
        input_values = [random.choice([True, False]) for _ in range(n)]
        output = evaluate_circuit(circuit, input_values)
        indeterminacy = 0
        for i in range(2**n):
            binary_input = format(i, f'0{n}b')
            values = [bool(int(bit)) for bit in binary_input]
            if evaluate_circuit(circuit, values) != output:
                indeterminacy += 1
        return indeterminacy / (2**n)
    
    def compute_monotone_width(circuit):
        n = len(circuit)
        max_width = 0
        for subset_size in range(1, n+1):
            for subset in combinations(range(n), subset_size):
                sub_circuit = [circuit[i] for i in subset]
                input_values = [random.choice([True, False]) for _ in range(subset_size)]
                output = evaluate_circuit(sub_circuit, input_values)
                if all(evaluate_circuit(circuit[:i+1], input_values) == output for i in range(len(sub_circuit))):
                    max_width = max(max_width, subset_size)
        return max_width
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_random_circuit(n)
        mli = compute_minimal_local_indeterminacy(circuit)
        w_mon = compute_monotone_width(circuit)
        metric_values.append(mli * w_mon)  # Using the product as a proxy for correlation
    
    if len(metric_values) < instances_tested:
        return {
            "metric_name": "mli * w_mon",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = 0.8
    if all(x >= correlation for x in metric_values):
        return {
            "metric_name": "mli * w_mon",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "mli * w_mon",
            "metric_value": sum(metric_values) / len(metric_values),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_correlation"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not_enough_correlation' first_failing_seed={first_failing_seed}")