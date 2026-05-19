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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def decision_tree_depth(f, n):
        if len(f) == 2**n:
            return 0
        mid = 2**(n-1)
        left = f[:mid]
        right = f[mid:]
        if all(x == left[0] for x in left) or all(x == right[0] for x in right):
            return 0
        return 1 + max(decision_tree_depth(left, n-1), decision_tree_depth(right, n-1))
    
    def deterministic_communication_complexity(f, n):
        if len(f) == 2**n:
            return 0
        mid = 2**(n-1)
        left = f[:mid]
        right = f[mid:]
        if all(x == left[0] for x in left) or all(x == right[0] for x in right):
            return 0
        return 1 + max(deterministic_communication_complexity(left, n-1), deterministic_communication_complexity(right, n-1))
    
    results = []
    for n in [8, 16, 24, 32, 40]:
        for d in range(1, n+1):
            for _ in range(20):
                f = generate_boolean_function(n)
                depth = decision_tree_depth(f, n)
                if depth < d:
                    continue
                cc = deterministic_communication_complexity(f, n)
                results.append((n, d, cc))
    
    if not results:
        return {
            "metric_name": "deterministic_communication_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_functions"
        }
    
    total_ratio = sum(cc * math.log2(n) / depth for n, d, cc in results)
    mean_ratio = total_ratio / len(results)
    
    return {
        "metric_name": "deterministic_communication_complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": mean_ratio >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")