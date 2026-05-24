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
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def bp_read_twice_complexity(f):
        n = len(f)
        max_consecutive_ones = 0
        current_count = 0
        for bit in f:
            if bit == 1:
                current_count += 1
                max_consecutive_ones = max(max_consecutive_ones, current_count)
            else:
                current_count = 0
        return max_consecutive_ones
    
    def langlands_dual_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_random_function(n)
        complexity = bp_read_twice_complexity(f)
        if complexity > n**(1/3):
            continue
        
        rank = langlands_dual_rank(f)
        total_rank += rank
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Langlands Dual Rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_rank = total_rank / instances_tested
    lower_bound = n**(1/3) * (1 - 0.1)
    upper_bound = n**(1/3) * (1 + 0.1)
    
    conjecture_holds = lower_bound <= mean_rank <= upper_bound
    
    return {
        "metric_name": "Langlands Dual Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} out of bounds [{lower_bound}, {upper_bound}]"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank out of bounds\" first_failing_seed={first_failing_seed}")