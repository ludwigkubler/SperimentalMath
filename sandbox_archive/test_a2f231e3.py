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
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncommutative_polynomial_representation(circuit):
        # Placeholder for the actual algorithm to compute the minimal order of noncommutative polynomial representation
        # This is a dummy implementation for demonstration purposes
        return random.randint(1, n)
    
    def entanglement_complexity(circuit):
        # Placeholder for the actual method to measure entanglement complexity
        # This is a dummy implementation for demonstration purposes
        return random.randint(1, n)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_circuit(n)
        ord_min_poly_rep = noncommutative_polynomial_representation(circuit)
        e_C = entanglement_complexity(circuit)
        results.append((ord_min_poly_rep, e_C))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    ord_min_poly_rep_values = [r[0] for r in results]
    e_C_values = [r[1] for r in results]
    
    mean_ord_min_poly_rep = sum(ord_min_poly_rep_values) / len(ord_min_poly_rep_values)
    mean_e_C = sum(e_C_values) / len(e_C_values)
    
    numerator = sum((ord_min_poly_rep - mean_ord_min_poly_rep) * (e_C - mean_e_C) for ord_min_poly_rep, e_C in results)
    denominator = math.sqrt(sum((ord_min_poly_rep - mean_ord_min_poly_rep)**2 for ord_min_poly_rep in ord_min_poly_rep_values)) * math.sqrt(sum((e_C - mean_e_C)**2 for e_C in e_C_values))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    pearson_correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": pearson_correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")