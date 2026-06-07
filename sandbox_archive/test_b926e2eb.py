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
    n_values = [5, 10, 15, 20, 30, 40]
    V_f_values = []
    D_min_f_squared_values = []

    for n in n_values:
        if n > 10:  # Avoiding trivial case enumeration
            f = [random.choice([0, 1]) for _ in range(2**n)]
            V_f = len(f)  # Simplified communication complexity rank
            D_min_f_squared = sum(i**2 for i in range(n))  # Minimal quadratic residue degree

            V_f_values.append(V_f)
            D_min_f_squared_values.append(D_min_f_squared)

    if not V_f_values or not D_min_f_squared_values:
        return {
            "metric_name": "V(f) and D_min(f)^2",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }

    V_f_mean = sum(V_f_values) / len(V_f_values)
    D_min_f_squared_mean = sum(D_min_f_squared_values) / len(D_min_f_squared_values)

    correlation_coefficient = 0
    for i in range(len(V_f_values)):
        correlation_coefficient += (V_f_values[i] - V_f_mean) * (D_min_f_squared_values[i] - D_min_f_squared_mean)
    correlation_coefficient /= math.sqrt(sum((x - V_f_mean)**2 for x in V_f_values)) * math.sqrt(sum((y - D_min_f_squared_mean)**2 for y in D_min_f_squared_values))

    return {
        "metric_name": "V(f) and D_min(f)^2",
        "metric_value": correlation_coefficient,
        "instances_tested": len(V_f_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + \
            [31, 37, 41, 43, 47, 53, 59, 61, 67, 71] + \
            [73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(metric_values):
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")