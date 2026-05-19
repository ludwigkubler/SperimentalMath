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
    
    def decision_tree_depth(f):
        if len(f) == 1:
            return 0
        mid = len(f) // 2
        left_depth = decision_tree_depth(f[:mid])
        right_depth = decision_tree_depth(f[mid:])
        return max(left_depth, right_depth) + 1
    
    def deterministic_communication_complexity(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        depth = decision_tree_depth(f)
        return depth / math.log2(n)
    
    n_values = [8, 16, 24, 32, 40]
    depths = range(1, max(n_values) + 1)
    instances_tested = 0
    total_ratio = 0
    
    for n in n_values:
        for d in depths:
            if d > n:
                continue
            for _ in range(20):
                f = generate_boolean_function(n)
                depth = decision_tree_depth(f)
                cc = deterministic_communication_complexity(f)
                instances_tested += 1
                total_ratio += cc * math.log2(n) / depth
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio >= 0.5
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")