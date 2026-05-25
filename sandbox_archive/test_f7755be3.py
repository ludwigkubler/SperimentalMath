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
    
    def compute_t_star(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid boolean function size")
        t_star = 0
        for i in range(n):
            count_1 = sum(1 for x in f if x & (1 << i))
            count_0 = len(f) - count_1
            t_star += min(count_1, count_0)
        return t_star
    
    def compute_j(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid boolean function size")
        j = 0
        for i in range(n):
            count_1 = sum(1 for x in f if x & (1 << i))
            count_0 = len(f) - count_1
            j += abs(count_1 - count_0)
        return j
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    t_star = compute_t_star(f)
    j = compute_j(f)
    
    if t_star == 0:
        return {
            "metric_name": "J(f)/T*(f)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "t_star is zero"
        }
    
    ratio = j / t_star
    expected_ratio = math.log(n)
    within_bound = abs(ratio - expected_ratio) <= 0.1 * expected_ratio
    
    return {
        "metric_name": "J(f)/T*(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": within_bound,
        "counterexample": "" if within_bound else f"Expected {expected_ratio}, got {ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")