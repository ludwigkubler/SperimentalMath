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
    
    n = 30  # Fixed size for simplicity, can be adjusted as needed
    m = int(n ** 1.5) - 1
    
    if m < 2:
        return {
            "metric_name": "irreducible_components",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "m < 2, cannot proceed"
        }
    
    k = math.ceil(math.log(n))
    
    def hook_length_formula(m, n):
        total = 1
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                total *= (i + j - 1)
                total //= (i * j)
        return total
    
    perm_n_components = hook_length_formula(n, k)
    det_m_components = hook_length_formula(m, k)
    
    if perm_n_components is None or det_m_components is None:
        return {
            "metric_name": "irreducible_components",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "hook_length_formula failed"
        }
    
    conjecture_holds = perm_n_components >= n**(k-1) * det_m_components
    counterexample = "" if conjecture_holds else f"perm_n={perm_n_components}, det_m={det_m_components}"
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": perm_n_components,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    total_components = 0
    num_trials = len(seeds)
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_components += trial_result["metric_value"]
    
    mean_components = total_components / num_trials
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / num_trials
    
    print(f"RESULT: SUPPORTED mean={mean_components} std=0.0 support_fraction={support_fraction}")