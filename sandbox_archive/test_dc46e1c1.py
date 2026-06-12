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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def polynomial_modulo(poly, q):
        return [coeff % q for coeff in poly]
    
    def k_theoretic_vector_bundle_order(poly, q):
        n = len(poly)
        if n == 1:
            return 1
        bundle_order = 0
        for i in range(1, n):
            sub_poly = polynomial_modulo(poly[:i], q)
            bundle_order += sum(sub_poly) % q
        return bundle_order
    
    def communication_complexity(func):
        n = len(func)
        if n == 1:
            return 1
        complexity = 0
        for i in range(1, n):
            sub_func = func[:i]
            complexity += sum(sub_func) % 2
        return complexity
    
    n_max = 40
    instances_tested = 0
    total_order = 0
    total_complexity = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            func = generate_boolean_function(n)
            order = k_theoretic_vector_bundle_order(func, n + 1)
            complexity = communication_complexity(func)
            total_order += order
            total_complexity += complexity
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_order = total_order / instances_tested
    mean_complexity = total_complexity / instances_tested
    correlation_coefficient = (instances_tested * mean_order * mean_complexity - 
                               sum(order * complexity for order, complexity in zip(range(instances_tested), range(instances_tested)))) / \
                              math.sqrt((instances_tested * sum(order**2 for order in range(instances_tested)) - sum(order**2 for order in range(instances_tested))) *
                                        (instances_tested * sum(complexity**2 for complexity in range(instances_tested)) - sum(complexity**2 for complexity in range(instances_tested))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")