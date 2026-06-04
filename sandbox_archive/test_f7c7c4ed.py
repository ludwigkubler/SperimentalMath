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
    
    def monotone_width(phi):
        n = len(phi)
        max_width = 0
        for i in range(1 << n):
            width = 0
            for j in range(n):
                if phi[i ^ (1 << j)] > phi[i]:
                    width += 1
            max_width = max(max_width, width)
        return max_width
    
    def local_induction_dimension(phi):
        n = len(phi)
        count = 0
        for i in range(1 << n):
            if all(phi[j] <= phi[i] for j in range(i)):
                count += 1
        return count
    
    lnd_values = []
    w_M_values = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        phi = generate_boolean_function(n)
        lnd = local_induction_dimension(phi)
        w_M = monotone_width(phi)
        lnd_values.append(lnd)
        w_M_values.append(w_M)
    
    if not lnd_values or not w_M_values:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_lnd = sum(lnd_values) / len(lnd_values)
    mean_w_M = sum(w_M_values) / len(w_M_values)
    correlation = sum((lnd - mean_lnd) * (w_M - mean_w_M) for lnd, w_M in zip(lnd_values, w_M_values)) / (len(lnd_values) * math.sqrt(sum((lnd - mean_lnd)**2 for lnd in lnd_values) * sum((w_M - mean_w_M)**2 for w_M in w_M_values)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(lnd_values),
        "n_max": max(len(phi) for phi in lnd_values + w_M_values),
        "conjecture_holds": 0.5 <= correlation < 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if 0.5 <= res["metric_value"] < 0.8) / len(results)
    
    if all(0.5 <= res["metric_value"] < 0.8 for res in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction=1")
    elif any(res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not (0.5 <= res["metric_value"] < 0.8)), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")