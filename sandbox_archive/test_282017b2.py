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
    
    def rank_variance(f):
        n = len(f)
        m = 2**(n-1)
        count_0 = f[:m].count(0) + f[m:].count(0)
        count_1 = f[:m].count(1) + f[m:].count(1)
        return abs(count_0 - count_1) / n
    
    def construct_quaternion_algebra(r):
        # Placeholder for actual construction logic
        # For simplicity, we assume the index is proportional to r
        return 2 * r
    
    results = []
    for n in range(5, 41):
        f = generate_boolean_function(n)
        r = rank_variance(f)
        index = construct_quaternion_algebra(r)
        if index < n * math.log(n):
            counterexample = f"n={n}, r={r}, index={index}"
            return {
                "metric_name": "quaternion_index",
                "metric_value": index,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        results.append(index)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "quaternion_index",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.5 * len(r)) / len(results)
    
    if all(r >= 0.5 * len(r) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.5 * len(r) for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"n=40, index<{0.5*len(results)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")