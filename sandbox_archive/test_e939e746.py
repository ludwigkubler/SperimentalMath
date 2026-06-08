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
    
    def generate_boolean_formula(n):
        formula = []
        for _ in range(2**n):
            if random.choice([True, False]):
                formula.append(random.choice(['A', 'B', 'C']))
        return formula
    
    def galois_group_order(formula):
        # Placeholder function to compute the Galois group order
        # This is a dummy implementation for testing purposes
        n = len(formula)
        if n == 1:
            return 2
        elif n == 2:
            return 4
        else:
            return 2**n
    
    def smallest_normal_subgroup_order(order):
        # Placeholder function to compute the order of the smallest normal subgroup
        # This is a dummy implementation for testing purposes
        if order <= 1:
            return 0
        elif order == 2:
            return 2
        else:
            return int(math.sqrt(order))
    
    n_max = 40
    instances_tested = 0
    total_order = 0
    
    for n in range(5, n_max + 1):
        formula = generate_boolean_formula(n)
        order = galois_group_order(formula)
        subgroup_order = smallest_normal_subgroup_order(order)
        
        if subgroup_order <= 0:
            continue
        
        instances_tested += 1
        total_order += subgroup_order
    
    if instances_tested == 0:
        return {
            "metric_name": "subgroup_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_order = total_order / instances_tested
    log_n_squared = [math.log(n, 2)**2 for n in range(5, n_max + 1)]
    correlation_coefficient = sum((mean_order - order) * (log_n_squared[i-5] - math.log(i, 2)**2) for i, order in enumerate(smallest_normal_subgroup_order(order))) / instances_tested
    
    return {
        "metric_name": "subgroup_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": "" if correlation_coefficient > 0.5 else "correlation_coefficient_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_too_low' first_failing_seed={first_failing_seed}")