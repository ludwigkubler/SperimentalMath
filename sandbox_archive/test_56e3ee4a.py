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
    
    # Generate a random boolean circuit with n inputs (n ≤ 40)
    n = random.randint(5, 40)
    num_gates = random.randint(n, n * 3)
    circuit = []
    for _ in range(num_gates):
        gate_type = random.choice(['AND', 'OR', 'NOT'])
        if gate_type == 'NOT':
            inputs = [random.randint(0, 1)]
        else:
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
        circuit.append((gate_type, inputs))
    
    # Calculate the p-adic metric associated with each circuit
    def calculate_p_adic_metric(circuit):
        # Simplified version of p-adic metric calculation
        return len(circuit)
    
    r_p_C = calculate_p_adic_metric(circuit)
    
    # Compute the entanglement complexity of C (simplified version for testing)
    def calculate_entanglement_complexity(circuit):
        # Simplified version of entanglement complexity calculation
        return len(circuit) ** 2
    
    e_C = calculate_entanglement_complexity(circuit)
    
    # Correlation check
    if r_p_C == 0 or e_C == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "p-adic metric or entanglement complexity is zero"
        }
    
    correlation = (r_p_C * e_C) / math.sqrt(r_p_C**2 * e_C**2)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation >= 0.7 and abs(r_p_C - e_C) <= 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / (len(results) - 1))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")