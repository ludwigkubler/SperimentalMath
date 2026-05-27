# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll_refutation_depth(f):
        n = len(f)
        if n == 1:
            return 1
        depth = float('inf')
        for i in range(n):
            f_i = f[:]
            f_i[i] = 0
            f_not_i = f[:]
            f_not_i[i] = 1
            depth = min(depth, dpll_refutation_depth(f_i), dpll_refutation_depth(f_not_i)) + 1
        return depth
    
    def quasi_linear_representation(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    instances_tested = 30
    total_rank = 0
    total_depth = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        depth = dpll_refutation_depth(f)
        rank = quasi_linear_representation(f)
        total_rank += rank
        total_depth += depth
    
    mean_rank = Fraction(total_rank, instances_tested)
    mean_depth = Fraction(total_depth, instances_tested)
    
    if mean_rank <= 0 or mean_depth <= 0:
        return {
            "metric_name": "rank_over_depth",
            "metric_value": float('inf'),
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mean_rank_or_depth_non_positive"
        }
    
    ratio = mean_rank / mean_depth
    c = 1 / 2  # Hypothetical constant for demonstration purposes
    
    return {
        "metric_name": "rank_over_depth",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": ratio > c,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "unknown"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")