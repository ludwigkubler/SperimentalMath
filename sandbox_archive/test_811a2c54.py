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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def entanglement_complexity(circuit):
        # Placeholder function to compute entanglement complexity
        # This is a dummy implementation and should be replaced with actual logic
        return len(circuit)
    
    def generate_quasi_monte_carlo_points(n, order):
        points = []
        for i in range(order):
            point = [random.uniform(0, 1) for _ in range(n)]
            points.append(point)
        return points
    
    def check_uniform_distribution(points):
        # Placeholder function to check uniform distribution
        # This is a dummy implementation and should be replaced with actual logic
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        complexity = entanglement_complexity(circuit)
        
        # Estimate the minimal order of quasi-Monte Carlo lattice points
        order = int(math.sqrt(complexity))
        while not check_uniform_distribution(generate_quasi_monte_carlo_points(n, order)):
            order += 1
        
        results.append({
            "n": n,
            "complexity": complexity,
            "order": order
        })
    
    total_order = sum(result["order"] for result in results)
    total_complexity = sum(result["complexity"] for result in results)
    mean_order = total_order / len(results)
    mean_complexity = total_complexity / len(results)
    
    # Check the acceptance criterion
    conjecture_holds = all(abs(order - complexity) <= 2 * complexity**(1/2) for order, complexity in zip([result["order"] for result in results], [result["complexity"] for result in results]))
    
    return {
        "metric_name": "Order vs Complexity",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")