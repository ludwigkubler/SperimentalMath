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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_width(f):
        n = len(f)
        width = 0
        for i in range(n):
            if f[i] != f[0]:
                width += 1
        return width
    
    def compute_free_probability_space_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            if f[i % n] == f[(i + 1) % n]:
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    W_f = compute_width(f)
    RankFreeProb_P_f = compute_free_probability_space_rank(f)
    
    if W_f == 0:
        return {
            "metric_name": "Rank vs Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Width is zero"
        }
    
    ratio = RankFreeProb_P_f / math.log(W_f)
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        RESULT = f"SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Ratio outside [0.5, 2]"
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)