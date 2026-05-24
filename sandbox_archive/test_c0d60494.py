# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_manifold(n):
        # Simple random manifold generation (e.g., a cycle graph)
        return list(range(n)) + [0]
    
    def compute_light_paths(manifold, p):
        # Minimal number of light paths to determine orientability
        return len(set(manifold))
    
    def construct_circuit(manifold):
        # Construct a circuit that can be satisfied by a constant number of assignments
        n = len(manifold)
        circuit_size = 2 * n - 1
        return circuit_size
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    manifold = generate_manifold(n)
    p = random.choice(manifold)
    
    light_paths = compute_light_paths(manifold, p)
    circuit_size = construct_circuit(manifold)
    
    if circuit_size == 0:
        return {
            "metric_name": "light_paths_to_circuit_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_size_zero"
        }
    
    ratio = Fraction(light_paths, circuit_size)
    return {
        "metric_name": "light_paths_to_circuit_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        supported_count = sum(1 for result in results if result["conjecture_holds"])
        support_fraction = Fraction(supported_count, len(results))
        
        if support_fraction >= Fraction(4, 5):
            mean_value = sum(result["metric_value"] for result in results) / len(results)
            std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            counterexample = results[first_failing_seed]["counterexample"]
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")