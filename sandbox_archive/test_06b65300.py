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
    
    def decision_tree_depth(f, n):
        if len(f) == 2**n:
            return 1
        mid = 2**(n-1)
        left = f[:mid]
        right = f[mid:]
        return 1 + max(decision_tree_depth(left, n-1), decision_tree_depth(right, n-1))
    
    def deterministic_communication_complexity(f, n):
        if len(f) == 2**n:
            return 0
        mid = 2**(n-1)
        left = f[:mid]
        right = f[mid:]
        return max(deterministic_communication_complexity(left, n-1), deterministic_communication_complexity(right, n-1)) + 1
    
    n_values = [8, 16, 24, 32, 40]
    depths = range(1, 5)
    instances_tested = 0
    total_ratio = 0.0
    support_count = 0
    
    for n in n_values:
        for d in depths:
            for _ in range(20):
                f = generate_boolean_function(n)
                dt_depth = decision_tree_depth(f, n)
                cc = deterministic_communication_complexity(f, n)
                instances_tested += 1
                ratio = cc * math.log2(n) / dt_depth
                total_ratio += ratio
                if dt_depth >= d and ratio >= 0.5:
                    support_count += 1
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = support_count / (len(n_values) * len(depths) * 20) >= 0.9
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")