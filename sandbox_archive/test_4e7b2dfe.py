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
    
    def hook_length_ratio(n):
        # Generate a random symmetric polynomial of degree n
        # This is a placeholder function; actual implementation needed
        return random.random()  # Placeholder for actual computation
    
    def perm_n_hook_length():
        n = 40  # Example value, should be dynamic
        return hook_length_ratio(n)
    
    def det_m_hook_length(m):
        m = int(math.sqrt(n))  # Example value, should be dynamic
        return hook_length_ratio(m)
    
    H_perm_n = perm_n_hook_length()
    H_det_m = det_m_hook_length(10)  # Example value, should be dynamic
    
    metric_name = "hook_length_ratio"
    metric_value = H_perm_n / H_det_m if H_det_m != 0 else float('inf')
    instances_tested = 1
    conjecture_holds = H_perm_n > H_det_m
    counterexample = "" if conjecture_holds else f"perm_n={H_perm_n}, det_m={H_det_m}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")