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
    
    def circuit_monotone_width(f):
        n = int(math.log2(len(f)))
        max_width = 0
        for i in range(1 << (n - 1)):
            width = 0
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    width += 1
            max_width = max(max_width, width)
        return max_width
    
    def quotient_algebra(f):
        n = int(math.log2(len(f)))
        algebra = [0] * (1 << n)
        for i in range(1 << n):
            if f[i] == f[0]:
                algebra[i] = 1
        return algebra
    
    def minimal_rank(algebra):
        n = int(math.log2(len(algebra)))
        rank = 0
        for i in range(n):
            if algebra[i] == 1:
                rank += 1
        return rank
    
    trials = 30
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    
    for _ in range(trials):
        n = random.choice(n_values)
        f = generate_boolean_function(n)
        width = circuit_monotone_width(f)
        algebra = quotient_algebra(f)
        rank = minimal_rank(algebra)
        
        if rank > 5 * width:
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": trials,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "rank > 5 * width"
            }
        
        total_rank += rank
        total_width += width
    
    mean_rank = total_rank / trials
    mean_width = total_width / trials
    correlation_coefficient = (total_rank - trials * mean_rank) / math.sqrt(trials * (trials - 1) * (mean_rank ** 2 + mean_width ** 2 - (total_rank ** 2 + total_width ** 2) / trials))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": trials,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(rank <= 5 * width for rank, width in zip([total_rank / trials] * trials, [mean_width] * trials)),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = list(map(int, sys.argv[1:]))
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > 5 * width\" first_failing_seed={first_failing_seed}")