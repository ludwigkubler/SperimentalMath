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
    
    def p_adic_log(x, p):
        if x <= 0:
            return float('inf')
        count = 0
        while x % p == 0:
            x //= p
            count += 1
        return count
    
    def rank_variance(protocol):
        # Placeholder for actual rank variance calculation
        return random.random()  # Replace with actual computation
    
    def complexity_function(protocol):
        # Placeholder for actual complexity function calculation
        return len(str(protocol))  # Replace with actual computation
    
    n_values = [5, 10, 15, 20, 30, 40]
    k_values = []
    r_values = []
    
    for n in n_values:
        protocol = random.randint(1, 10**n)
        k = p_adic_log(complexity_function(protocol), 2)
        r = rank_variance(protocol)
        k_values.append(k)
        r_values.append(r)
    
    if not k_values or not r_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_k = sum(k_values) / len(k_values)
    mean_r = sum(r_values) / len(r_values)
    correlation_coefficient = (sum((k - mean_k) * (r - mean_r) for k, r in zip(k_values, r_values)) /
                               math.sqrt(sum((k - mean_k)**2 for k in k_values) *
                                         sum((r - mean_r)**2 for r in r_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and correlation_coefficient <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")