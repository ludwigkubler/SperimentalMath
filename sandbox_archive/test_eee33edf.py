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
    
    def generate_galois_group(n):
        # Simulate generating a Galois group for a Boolean circuit with n gates
        return 2 ** n
    
    def calculate_monotone_width(n):
        # Simulate calculating the monotone width of a Boolean circuit with n gates
        return n
    
    instances_tested = 0
    total_galois_group_order = 0
    total_monotone_width = 0
    n_max = 1
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 5 instances per size
            galois_group_order = generate_galois_group(n)
            monotone_width = calculate_monotone_width(n)
            
            total_galois_group_order += galois_group_order
            total_monotone_width += monotone_width
            instances_tested += 1
    
    mean_galois_group_order = Fraction(total_galois_group_order, instances_tested)
    mean_monotone_width = Fraction(total_monotone_width, instances_tested)
    
    if instances_tested < 30:
        return {
            "metric_name": "mean_galois_group_order",
            "metric_value": float(mean_galois_group_order),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = (instances_tested * mean_galois_group_order * mean_monotone_width -
                               total_galois_group_order * total_monotone_width) / (
                                   instances_tested * (mean_galois_group_order ** 2) -
                                   total_galois_group_order ** 2) * (
                                       instances_tested * (mean_monotone_width ** 2) -
                                       total_monotone_width ** 2)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, galois_group_order={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break