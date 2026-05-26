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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_tensor_product_valuation(f):
        n = len(f)
        if n == 1:
            return f[0]
        else:
            mid = n // 2
            left = generate_random_boolean_function(mid)
            right = generate_random_boolean_function(n - mid)
            return [boolean_tensor_product_valuation(left[:mid]) and boolean_tensor_product_valuation(right[mid:]) for _ in range(2**(n-mid))]
    
    def symplectic_cell_decomposition(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            mid = n // 2
            left = generate_random_boolean_function(mid)
            right = generate_random_boolean_function(n - mid)
            return symplectic_cell_decomposition(left) + symplectic_cell_decomposition(right)
    
    def complexity(f):
        return len(boolean_tensor_product_valuation(f))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        r_delta = symplectic_cell_decomposition(f)
        c_f = complexity(f)
        results.append((r_delta, c_f))
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [r_delta / c_f for r_delta, c_f in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio)**2 for x in ratios) / len(ratios))
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(1.5 >= ratio <= 2.0 for ratio in ratios),
        "counterexample": "" if all(1.5 >= ratio <= 2.0 for ratio in ratios) else f"First failing seed: {seed}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["instances_tested"] > 0) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results if result["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")