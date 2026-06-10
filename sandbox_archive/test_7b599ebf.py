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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def hyperplane_arrangement(f):
        n = len(f)
        arrangement = []
        for i in range(2**n):
            point = [(i >> j) & 1 for j in range(n)]
            arrangement.append(point)
        return arrangement
    
    def p_adic_logarithmic_capacity(arrangement, p=5):
        n = len(arrangement[0])
        capacity = 0
        for point in arrangement:
            product = 1
            for coord in point:
                product *= (coord + 1) % p
            capacity += math.log(product, p)
        return capacity / len(arrangement)
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank_variance = 0
        for i in range(2**n):
            point = [(i >> j) & 1 for j in range(n)]
            value = f[i]
            rank_variance += abs(value - 0.5) ** 2
        return rank_variance / (2**n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        arr = hyperplane_arrangement(f)
        log_cap = p_adic_logarithmic_capacity(arr)
        rank_var = communication_complexity_rank_variance(f)
        results.append((log_cap, rank_var))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_caps, rank_vars = zip(*results)
    correlation_coefficient = sum((x - y) ** 2 for x, y in zip(log_caps, rank_vars)) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and math.isclose(correlation_coefficient, 0.8, abs_tol=0.1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")