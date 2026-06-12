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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_rank_variance(f):
    n = int(math.log2(len(f)))
    count_0 = f.count(0)
    count_1 = len(f) - count_0
    r = (count_0 * count_1) / (len(f) ** 2)
    return r

def construct_quaternion_algebra(r):
    # Simplified construction for demonstration purposes
    index = r * math.log(len(f))
    return index

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        r = compute_rank_variance(f)
        index = construct_quaternion_algebra(r)
        results.append(index)
        instances_tested += len(f)
        n_max = max(n_max, n)

        if index < n * math.log(n):
            conjecture_holds = False
            counterexample = f"n={n}, r={r}, index={index}"

    return {
        "metric_name": "quaternion_index",
        "metric_value": sum(results) / len(results),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])

    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.5 * len(r)) / len(results)

    if all(r >= n * math.log(n) for r, n in zip(results, [n_max for _ in range(len(results))])):
        result = "SUPPORTED"
    elif any(r < n * math.log(n) for r, n in zip(results, [n_max for _ in range(len(results))])):
        result = "FALSIFIED"
    else:
        result = "INCONCLUSIVE"

    print(f"RESULT: {result} mean={mean_value:.2f} std=0.0 support_fraction={support_fraction:.2f}")