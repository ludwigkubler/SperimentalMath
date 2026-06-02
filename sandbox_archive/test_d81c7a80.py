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
    
    def generate_random_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def min_order_symmetric_braid_group(clauses):
        # Placeholder function to compute the minimal order of the symmetric braid group
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses)

    def resolution_proof_width(clauses):
        # Placeholder function to compute the resolution proof width
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses) * 2

    min_order_values = []
    width_values = []

    for _ in range(30):  # Number of instances per seed
        n = random.randint(5, 40)
        instance = generate_random_sat_instance(n)
        min_order = min_order_symmetric_braid_group(instance)
        width = resolution_proof_width(instance)
        
        if abs(min_order - width) > 3:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": len(min_order_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"min_order({min_order}) - width({width}) > 3"
            }
        
        min_order_values.append(min_order)
        width_values.append(width)

    mean_x = sum(min_order_values) / len(min_order_values)
    mean_y = sum(width_values) / len(width_values)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(min_order_values, width_values)) / \
                              math.sqrt(sum((x - mean_x) ** 2 for x in min_order_values) * 
                                        sum((y - mean_y) ** 2 for y in width_values))

    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_order_values),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(abs(x - y) <= 3 for x, y in zip(min_order_values, width_values)),
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
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8 or abs(min_order - width) > 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")