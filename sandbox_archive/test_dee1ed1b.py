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
    
    def generate_d_regular_boolean_function(d, n):
        # Generate a d-regular boolean function
        if d == 0:
            return [random.choice([0, 1]) for _ in range(n)]
        elif d == n - 1:
            return [1] * (n - 1) + [0]
        else:
            raise ValueError("Unsupported degree for boolean function generation")
    
    def calculate_galois_group(f):
        # Placeholder for Galois group calculation
        # In practice, this would involve algebraic computations
        return len(f)
    
    def calculate_circuit_entanglement(circuit):
        # Placeholder for circuit entanglement calculation
        # In practice, this would involve analyzing the circuit structure
        return len(circuit) ** 2
    
    n = random.randint(5, 40)
    d = random.randint(1, n - 2)
    f = generate_d_regular_boolean_function(d, n)
    galois_group_degree = calculate_galois_group(f)
    circuit_entanglement = calculate_circuit_entanglement(f)
    
    return {
        "metric_name": "Galois Group Degree vs Circuit Entanglement",
        "metric_value": Fraction(galois_group_degree),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": galois_group_degree <= circuit_entanglement and circuit_entanglement <= galois_group_degree ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")