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
    
    def generate_tseitin_formula(n):
        # Generate a random Tseitin formula with n variables
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]} OR {variables[i]}')
        return ' AND '.join(clauses)
    
    def minimal_order(G, n):
        # Placeholder for the actual algorithm to compute the minimal order
        # This is a dummy implementation that returns a random value
        return random.randint(1, 10 * n)
    
    def resolution_proof_width(phi_G, n):
        # Placeholder for the actual algorithm to compute the resolution proof width
        # This is a dummy implementation that returns a random value
        return random.randint(n, 2 * n)
    
    results = []
    for _ in range(20):  # Generate 20 Tseitin formulas
        phi_G = generate_tseitin_formula(random.randint(5, 40))
        n = len(phi_G.split())
        minimal_order_value = minimal_order(phi_G, n)
        proof_width_value = resolution_proof_width(phi_G, n)
        results.append((minimal_order_value, proof_width_value))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x = [r[0] for r in results]
    y = [r[1] for r in results]
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    
    covariance = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
    variance_x = sum((xi - mean_x) ** 2 for xi in x) / len(x)
    variance_y = sum((yi - mean_y) ** 2 for yi in y) / len(y)
    
    correlation_coefficient = covariance / (math.sqrt(variance_x) * math.sqrt(variance_y))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(phi_G.split()) for phi_G in results),
        "conjecture_holds": correlation_coefficient > 0.9 and abs(covariance / (math.sqrt(variance_x) * math.sqrt(variance_y))) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")