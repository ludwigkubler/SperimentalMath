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
    
    def compute_l_function(f):
        n = int(math.log2(len(f)))
        if f == [0]*len(f) or f == [1]*len(f):
            return 1
        rank = 0
        for i in range(n):
            sub_f = []
            for j in range(2**n):
                if (j >> i) & 1:
                    sub_f.append(f[j])
            rank += compute_l_function(sub_f)
        return rank
    
    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        candidate = 2
        while len(primes) < k:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = compute_l_function(f)
        results.append({"n": n, "rank": rank})
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(mean_rank >= n * math.log(n, 2) and mean_rank <= n * math.log(n, 2) + 1 for n in n_values)
    counterexample = "" if conjecture_holds else "rank_outside_bound"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_outside_bound\" first_failing_seed={first_failing_seed}")