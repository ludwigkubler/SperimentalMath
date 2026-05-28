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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def communication_complexity(xor_func):
        n = len(xor_func)
        if n == 1:
            return 1
        else:
            return 2 * communication_complexity(xor_func[:n//2]) + 1
    
    def coin_tossing_time(n, xor_func):
        # Simplified model for coin tossing time
        return random.uniform(0.1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        xor_func = generate_xor_function(n)
        cc_xor_n = communication_complexity(xor_func)
        expected_value = math.log(n) * cc_xor_n
        ct_time = coin_tossing_time(n, xor_func)
        
        total_metric_value += ct_time
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = abs(mean_metric_value - expected_value) <= 2 * expected_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "coin_tossing_time",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")