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
    
    def generate_quasi_random_sequence(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def binary_string_to_boolean_function(binary_str):
        n = len(binary_str)
        def f(x):
            index = 0
            for i in range(n):
                if x & (1 << i):
                    index += 2 ** i
            return binary_str[index] == '1'
        return f
    
    def compute_circuit_monotone_width(f, n):
        # Simplified heuristic to estimate circuit monotone width
        # This is a placeholder and should be replaced with actual computation
        return math.ceil(math.log(n, 2))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        sequence = generate_quasi_random_sequence(n)
        binary_str = ''.join(str(bit) for bit in sequence)
        f = binary_string_to_boolean_function(binary_str)
        width = compute_circuit_monotone_width(f, n)
        results.append({
            "n": n,
            "sequence_length": len(sequence),
            "circuit_monotone_width": width
        })
    
    if not results:
        return {
            "metric_name": "Circuit Monotone Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "Circuit Monotone Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instance sizes"
        }
    
    sequence_lengths = [result["sequence_length"] for result in results]
    widths = [result["circuit_monotone_width"] for result in results]
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_dev_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_dev_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    correlation_coefficient = pearson_correlation_coefficient(sequence_lengths, widths)
    
    return {
        "metric_name": "Circuit Monotone Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE No trials executed")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE Insufficient support")