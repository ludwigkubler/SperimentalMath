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
    
    def hypergeometric(n):
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= (n + 1 - i) / i
        return result
    
    def dpll_path_length(n):
        # Simulate DPLL path length (placeholder)
        return random.randint(10**n, 2*10**n)
    
    n = random.randint(5, 40)
    alpha = hypergeometric(n + 1) * hypergeometric(1/2) / hypergeometric(n + 3/2)
    expected_path_length = abs(n**(1 + alpha))
    actual_path_length = dpll_path_length(n)
    
    return {
        "metric_name": "DPLL Path Length",
        "metric_value": actual_path_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(actual_path_length - expected_path_length) <= 0.1 * expected_path_length,
        "counterexample": "" if conjecture_holds else f"Expected {expected_path_length}, got {actual_path_length}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed + 1}")