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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return ['0'] if random.choice([True, False]) else ['1']
        elif depth == 1:
            return [random.choice(['NOT', 'AND', 'OR'])]
        else:
            left = generate_boolean_circuit(random.randint(0, depth-1))
            right = generate_boolean_circuit(random.randint(0, depth-1))
            op = random.choice(['NOT', 'AND', 'OR'])
            return [op] + left + right
    
    def count_noncommutative_variables(circuit):
        if not circuit:
            return 0
        elif circuit[0] in ['NOT', 'AND', 'OR']:
            return 1 + count_noncommutative_variables(circuit[1:])
        else:
            return count_noncommutative_variables(circuit[1:])
    
    depths = [5, 10, 15, 20, 30, 40]
    results = []
    for depth in depths:
        circuit = generate_boolean_circuit(depth)
        n_G = count_noncommutative_variables(circuit)
        results.append((depth, n_G))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    depths, n_Gs = zip(*results)
    mean_depth = sum(depths) / len(depths)
    mean_n_G = sum(n_Gs) / len(n_Gs)
    
    covariance = sum((depth - mean_depth) * (n_G - mean_n_G) for depth, n_G in results) / len(results)
    variance_depth = sum((depth - mean_depth) ** 2 for depth in depths) / len(depths)
    variance_n_G = sum((n_G - mean_n_G) ** 2 for n_G in n_Gs) / len(n_Gs)
    
    if variance_depth == 0 or variance_n_G == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": max(depths),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_depth) * math.sqrt(variance_n_G))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(depths),
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")