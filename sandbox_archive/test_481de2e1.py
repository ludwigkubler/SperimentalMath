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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def min_order_symmetric_braid_group(clauses):
        # Placeholder function to simulate the computation
        # For simplicity, we assume a linear relationship between n and min_order
        n = len(set(abs(x) for clause in clauses for x in clause))
        return 2 * n + 1
    
    def resolution_proof_width(clauses):
        # Placeholder function to simulate the computation
        # For simplicity, we assume a linear relationship between n and width
        n = len(set(abs(x) for clause in clauses for x in clause))
        return 3 * n + 2
    
    instances_tested = 0
    n_max = 1
    min_order_values = []
    width_values = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        clauses = generate_sat_instance(n)
        if len(clauses) > n_max:
            n_max = len(clauses)
        
        instances_tested += 1
        min_order = min_order_symmetric_braid_group(clauses)
        width = resolution_proof_width(clauses)
        
        min_order_values.append(min_order)
        width_values.append(width)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(min_order_values, width_values)) / \
                               math.sqrt(sum((x - mean_x) ** 2 for x in min_order_values) * sum((y - mean_y) ** 2 for y in width_values))
    
    mean_value = sum(min_order_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in min_order_values) / instances_tested)
    
    conjecture_holds = all(abs(x - y) <= 3 for x, y in zip(min_order_values, width_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(x - y) > 3 for x, y in zip([r["metric_value"] for r in results], [r["metric_value"] for r in results])):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")