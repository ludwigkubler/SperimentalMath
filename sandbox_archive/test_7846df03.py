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

def generate_circuit(depth):
    if depth == 0:
        return ['x1', 'x2']
    inputs = generate_circuit(depth - 1)
    gate = random.choice(['AND', 'OR'])
    new_input = f'({gate} {inputs[0]} {inputs[1]})'
    return [new_input]

def geometric_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        input_space_size = 2 ** len(circuit)
        probabilities = [Fraction(1, input_space_size)] * input_space_size
        H_geo_I_C = geometric_entropy(probabilities)
        d_C = n
        
        results.append({
            "n": n,
            "d_C": d_C,
            "H_geo_I_C": H_geo_I_C
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_sum = 0
    for result in results:
        correlation_sum += (result["d_C"] - sum(result["d_C"] for r in results) / len(results)) * \
                           (math.log2(result["H_geo_I_C"]) - sum(math.log2(r["H_geo_I_C"]) for r in results) / len(results))
    
    variance = sum((result["d_C"] - sum(result["d_C"] for r in results) / len(results)) ** 2 for result in results)
    
    if variance == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = correlation_sum / (len(results) * math.sqrt(variance))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": "" if correlation >= 0.8 else f"correlation={correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_correlation = sum(result["metric_value"] for result in results) / len(results)
        std_correlation = math.sqrt(sum((result["metric_value"] - mean_correlation) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        mean_correlation = sum(result["metric_value"] for result in results) / len(results)
        std_correlation = math.sqrt(sum((result["metric_value"] - mean_correlation) ** 2 for result in results) / len(results))
        support_fraction = (len([result for result in results if result["conjecture_holds"]]) / len(results)) * 100
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_correlation} std={std_correlation} support_fraction={support_fraction:.2f}%")