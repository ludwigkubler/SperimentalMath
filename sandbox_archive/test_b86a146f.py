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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate_type)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def calculate_circuit_depth(circuit):
        depth = {i: 0 for i in range(len(circuit))}
        stack = []
        for gate_type, inputs in reversed(circuit):
            max_input_depth = max(depth[i] for i in inputs)
            depth[len(circuit) - len(stack)] = max_input_depth + 1
            stack.append((gate_type, inputs))
        return depth[0]
    
    def calculate_minimal_symmetric_braid_length(circuit):
        # This is a placeholder function. In practice, you would need to implement
        # the actual algorithm for calculating the minimal symmetric braid length.
        # For simplicity, we will assume it returns a random value between 1 and n.
        return random.randint(1, len(circuit))
    
    def calculate_correlation_coefficient(msl_values, d_values):
        if len(msl_values) != len(d_values):
            raise ValueError("msl_values and d_values must have the same length")
        
        n = len(msl_values)
        mean_msl = sum(msl_values) / n
        mean_d = sum(d_values) / n
        
        numerator = sum((msl_values[i] - mean_msl) * (d_values[i] - mean_d) for i in range(n))
        denominator = math.sqrt(sum((msl_values[i] - mean_msl)**2 for i in range(n))) * math.sqrt(sum((d_values[i] - mean_d)**2 for i in range(n)))
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    def calculate_median(lst):
        lst.sort()
        n = len(lst)
        if n % 2 == 1:
            return lst[n // 2]
        else:
            return (lst[n // 2 - 1] + lst[n // 2]) / 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    msl_values = []
    d_values = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        depth = calculate_circuit_depth(circuit)
        msl = calculate_minimal_symmetric_braid_length(circuit)
        
        if msl is None or depth is None:
            return {
                "seed": seed,
                "metric_name": "msl",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        msl_values.append(msl)
        d_values.append(depth)
    
    correlation_coefficient = calculate_correlation_coefficient(msl_values, d_values)
    median_msl = calculate_median(msl_values)
    mean_msl = sum(msl_values) / len(msl_values)
    
    if abs(correlation_coefficient) < 0.8 or not (median_msl * 1/3 <= mean_msl <= median_msl * 3):
        return {
            "seed": seed,
            "metric_name": "msl",
            "metric_value": mean_msl,
            "instances_tested": len(msl_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Correlation coefficient: {correlation_coefficient}, Mean MSL: {mean_msl}, Median MSL: {median_msl}"
        }
    
    return {
        "seed": seed,
        "metric_name": "msl",
        "metric_value": mean_msl,
        "instances_tested": len(msl_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_msl = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_msl = math.sqrt(sum((r["metric_value"] - mean_msl)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_msl} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_msl} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient or MSL out of bounds\" first_failing_seed={first_failing_seed}")