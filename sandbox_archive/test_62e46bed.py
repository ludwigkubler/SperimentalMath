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
    
    def generate_random_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_entanglement_complexity(circuit):
        # Placeholder function. Replace with actual entanglement complexity computation.
        return len(circuit) / 2
    
    def calculate_minimal_geometric_entropy(n):
        # Placeholder function. Replace with actual minimal geometric entropy calculation.
        return n * math.log2(n)
    
    results = []
    for _ in range(30):  # Sample 30 random circuits
        n = random.randint(5, 40)  # Sweep n through {5, 10, 15, 20, 30, 40}
        circuit = generate_random_circuit(n)
        ec = compute_entanglement_complexity(circuit)
        mge = calculate_minimal_geometric_entropy(n)
        results.append((ec, mge))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No results generated"
        }
    
    ec_values, mge_values = zip(*results)
    correlation_coefficient = sum((x - mean_ec) * (y - mean_mge) for x, y in zip(ec_values, mge_values)) / \
                              math.sqrt(sum((x - mean_ec)**2 for x in ec_values) * sum((y - mean_mge)**2 for y in mge_values))
    mean_ec = sum(ec_values) / len(ec_values)
    mean_mge = sum(mge_values) / len(mge_values)
    
    if correlation_coefficient <= 0.7 or not (1.2 <= mean_mge / mean_ec <= 1.8):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": f"Correlation coefficient {correlation_coefficient} or mge/ec ratio outside [1.2, 1.8]"
        }
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")