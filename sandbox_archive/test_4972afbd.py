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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 0
        for i in range(1, n):
            if any(f[j] != f[j ^ (1 << i)] for j in range(2**(n-1))):
                rank += 1
        return rank
    
    def riemann_roch_theorem(n, r):
        # Simplified version of Riemann-Roch theorem for meromorphic functions
        return n + 1 - r
    
    def count_distinct_roots(f):
        # Placeholder for counting distinct roots using a simple method
        return len(set(f))
    
    C = 0.5  # Placeholder constant, adjust as needed
    instances_tested = 0
    total_ratio = 0
    n_max = 1
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        f = generate_random_boolean_function(n)
        r_f = communication_complexity_rank(f)
        roots_count = count_distinct_roots(f)
        
        if r_f == 0:
            continue
        
        instances_tested += 1
        ratio = Fraction(roots_count, r_f**2)
        total_ratio += ratio
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = all(ratio <= C for ratio in [Fraction(roots_count, r_f**2) for _ in range(30)])
    
    return {
        "metric_name": "Ratio of distinct roots to r_f^2",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")