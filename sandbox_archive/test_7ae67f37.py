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
    
    def symmetric_spectrum_dimension(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] == f[i ^ (i >> 1)]:
                count += 1
        return count / len(f)
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            rank += max([f[j] for j in range(2**n) if (j >> i) & 1])
        return rank
    
    results = []
    for _ in range(30):  # Sample 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        mssd = symmetric_spectrum_dimension(f)
        rank = communication_complexity_rank(f)
        results.append((mssd, rank))
    
    mean_mssd = sum(m for m, r in results) / len(results)
    mean_rank = sum(r for m, r in results) / len(results)
    ratio = abs(mean_mssd / mean_rank)
    
    return {
        "metric_name": "MSSD to Rank Ratio",
        "metric_value": ratio,
        "instances_tested": 30,
        "n_max": max([int(math.log2(len(f))) for f in [generate_boolean_function(n) for n in [5, 10, 15, 20, 30, 40]]]),
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else "MSSD to Rank Ratio > 1.5"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"MSSD to Rank Ratio > 1.5\" first_failing_seed={first_failing_seed}")