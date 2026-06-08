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
    
    def generate_random_circuit(n: int, max_depth: int):
        if n == 1:
            return ['0']
        depth = random.randint(1, max_depth)
        circuit = []
        for _ in range(depth):
            gate = random.choice(['AND', 'OR'])
            inputs = [generate_random_circuit(random.randint(1, n), max_depth-1) for _ in range(gate == 'AND')]
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_circuit_depth(circuit):
        if isinstance(circuit, str):
            return 0
        else:
            gate, inputs = circuit
            return 1 + max(calculate_circuit_depth(inp) for inp in inputs)
    
    def calculate_minimal_symmetric_braid_length(circuit):
        if isinstance(circuit, str):
            return 1
        else:
            gate, inputs = circuit
            lengths = [calculate_minimal_symmetric_braid_length(inp) for inp in inputs]
            if gate == 'AND':
                return sum(lengths)
            elif gate == 'OR':
                return max(lengths)
    
    def calculate_correlation_coefficient(msl_values, depth_values):
        n = len(msl_values)
        mean_msl = sum(msl_values) / n
        mean_depth = sum(depth_values) / n
        numerator = sum((msl - mean_msl) * (depth - mean_depth) for msl, depth in zip(msl_values, depth_values))
        denominator = math.sqrt(sum((msl - mean_msl) ** 2 for msl in msl_values)) * math.sqrt(sum((depth - mean_depth) ** 2 for depth in depth_values))
        return numerator / denominator if denominator != 0 else 0
    
    def calculate_median(values):
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 1:
            return sorted_values[n // 2]
        else:
            return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    
    def calculate_mean(values):
        return sum(values) / len(values)
    
    msl_values = []
    depth_values = []
    n_max = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_random_circuit(n, n)
            msl = calculate_minimal_symmetric_braid_length(circuit)
            depth = calculate_circuit_depth(circuit)
            
            msl_values.append(msl)
            depth_values.append(depth)
            instances_tested += 1
    
    correlation_coefficient = calculate_correlation_coefficient(msl_values, depth_values)
    mean_msl = calculate_mean(msl_values)
    median_msl = calculate_median(msl_values)
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_msl / median_msl - 1) <= 2
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or mean_msl not within a factor of 3 of median"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")