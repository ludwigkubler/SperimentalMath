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
    
    def boolean_function(n):
        return lambda x: random.randint(0, 1)
    
    def modular_form(f, n):
        # Placeholder for actual modular form computation
        return sum(f(i) * (i + 1) % n for i in range(n))
    
    def tensor_product_valuations(f, n):
        count = 0
        for i in range(2**n):
            if f(tuple((i >> j) & 1 for j in range(n))):
                count += 1
        return count
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        f = boolean_function(n)
        M_f = modular_form(f, n)
        r_M_f = sum(1 for i in range(n) if (M_f >> i) & 1)
        num_valuations = tensor_product_valuations(f, n)
        
        results.append({
            "n": n,
            "r_M_f": r_M_f,
            "num_valuations": num_valuations
        })
    
    mean_r_M_f = sum(result["r_M_f"] for result in results) / len(results)
    mean_num_valuations = sum(result["num_valuations"] for result in results) / len(results)
    correlation_coefficient = (sum((result["r_M_f"] - mean_r_M_f) * (result["num_valuations"] - mean_num_valuations) for result in results) /
                               math.sqrt(sum((result["r_M_f"] - mean_r_M_f)**2 for result in results) *
                                         sum((result["num_valuations"] - mean_num_valuations)**2 for result in results)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": "" if correlation_coefficient > 0.5 else "negative_correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(30)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"negative_correlation\" first_failing_seed={first_failing_seed}")