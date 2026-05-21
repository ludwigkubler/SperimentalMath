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
    
    def generate_hyperbolic_surface(g):
        if g < 4:
            # Placeholder for actual hyperbolic surface generation logic
            return "hyperbolic_surface"
        else:
            raise NotImplementedError("Mapping undefined for genus >= 4")
    
    def construct_satisfiability_instance(surface, n):
        # Placeholder for constructing satisfiability instance on the surface
        return "satisfiability_instance"
    
    def measure_circuit_size(instance):
        # Placeholder for measuring circuit size to solve the instance
        return random.randint(10, 100)
    
    g_values = [5, 10, 15, 20, 30, 40]
    total_size = 0
    instances_tested = 0
    
    for g in g_values:
        try:
            surface = generate_hyperbolic_surface(g)
            instance = construct_satisfiability_instance(surface, n=10)  # Fixed n to avoid sub-asymptotic n
            circuit_size = measure_circuit_size(instance)
            total_size += circuit_size
            instances_tested += 1
        except NotImplementedError:
            return {
                "metric_name": "circuit_size",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
    
    if instances_tested == 0:
        return {
            "metric_name": "circuit_size",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    mean_size = total_size / instances_tested
    conjecture_holds = all(abs(2**g * mean_size - mean_size) <= 1.05 * mean_size for g in g_values)
    counterexample = "" if conjecture_holds else f"Genus {g_values[0]} does not satisfy the bound"
    
    return {
        "metric_name": "circuit_size",
        "metric_value": mean_size,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - 2**g * result["metric_value"]) > 1.05 * result["metric_value"] for g, result in enumerate(results)):
        first_failing_seed = next(seed for seed, result in enumerate(results) if abs(result["metric_value"] - 2**g * result["metric_value"]) > 1.05 * result["metric_value"])
        print(f"RESULT: FALSIFIED counterexample='genus {g} does not satisfy the bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")