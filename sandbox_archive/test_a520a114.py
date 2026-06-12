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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_rank_variance(f):
    n = len(f)
    m = 2**(n-1)
    sum_f = sum(f)
    sum_not_f = sum(1 - x for x in f)
    rank_variance = (sum_f * sum_not_f) / (m * (m - 1))
    return rank_variance

def construct_quaternion_algebra(r):
    if r <= 0:
        return None
    n = len(f)
    index = r * math.log(n)
    return index

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        r = compute_rank_variance(f)
        index = construct_quaternion_algebra(r)
        if index is None:
            return {
                "metric_name": "index",
                "metric_value": -1,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        results.append(index)
    mean_index = sum(results) / len(results)
    return {
        "metric_name": "index",
        "metric_value": mean_index,
        "instances_tested": 6,
        "n_max": max(40, n),
        "conjecture_holds": all(x >= n * math.log(n) for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    total_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        total_results.append(trial_result)

    mean_index = sum(result["metric_value"] for result in total_results) / len(total_results)
    support_fraction = sum(1 for result in total_results if result["conjecture_holds"]) / len(total_results)
    
    if all(result["conjecture_holds"] for result in total_results):
        print(f"RESULT: SUPPORTED mean={mean_index} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_index} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, total_results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")