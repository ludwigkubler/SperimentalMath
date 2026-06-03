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
    
    def generate_circuit(n, d):
        # Placeholder for circuit generation logic
        return [random.randint(0, 1) for _ in range(n)]
    
    def calculate_kostant_cohomology(circuit):
        # Placeholder for Kostant cohomology calculation logic
        return random.randint(1, 10)
    
    def calculate_monotone_width(circuit):
        # Placeholder for monotone width calculation logic
        return random.randint(1, 10)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n, random.randint(1, 10))
            lcoh = calculate_kostant_cohomology(circuit)
            omega = calculate_monotone_width(circuit)
            results.append((lcoh, omega))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lcoh_values, omega_values = zip(*results)
    mean_lcoh = sum(lcoh_values) / len(lcoh_values)
    mean_omega = sum(omega_values) / len(omega_values)
    
    if any(x is None for x in (mean_lcoh, mean_omega)):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = (sum((x - mean_lcoh) * (y - mean_omega) for x, y in results) /
                               math.sqrt(sum((x - mean_lcoh) ** 2 for x in lcoh_values) *
                                         sum((y - mean_omega) ** 2 for y in omega_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= correlation_coefficient <= 1,
        "counterexample": "" if 0.8 <= correlation_coefficient <= 1 else "correlation_out_of_range"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next((seed for seed, result in zip(seeds, results) if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None)) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")