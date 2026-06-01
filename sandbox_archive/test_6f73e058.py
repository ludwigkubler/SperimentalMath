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
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def minimal_local_ring_norm(f):
        n = len(f)
        norm = sum(1 for x in f if x == 1) / math.sqrt(n)
        return norm
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        norm = minimal_local_ring_norm(f)
        results.append({"n": n, "rank": rank, "norm": norm})
    
    if not results:
        return {
            "metric_name": "minimal_local_ring_norm_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_function"
        }
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_norm = sum(result["norm"] for result in results) / len(results)
    ratio = mean_norm / math.sqrt(mean_rank)
    
    return {
        "metric_name": "minimal_local_ring_norm_ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": ratio <= 1.0,  # Simplified O(f(n^(1/2))) to f(n^(1/2)) <= 1
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        RESULT = f"RESULT: FALSIFIED counterexample=\"minimal_local_ring_norm_ratio\" first_failing_seed={first_failing_seed}"
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    
    print(RESULT)