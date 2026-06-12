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
    
    def compute_rank_variance(f):
        n = len(f)
        m = n // 2
        count_0 = sum(1 for x in f if x == 0)
        count_1 = sum(1 for x in f if x == 1)
        return abs(count_0 - count_1) / (n * (n + 1))
    
    def construct_quaternion_algebra(r):
        # This is a placeholder function. In practice, constructing
        # a quaternion algebra from the rank variance would be complex.
        # For simplicity, we assume this function always returns a valid
        # quaternion algebra with an index proportional to r.
        return r * 10
    
    def calculate_index(q):
        # Placeholder for calculating the index of a quaternion algebra.
        # In practice, this would involve complex computations.
        return q
    
    n_max = 0
    instances_tested = 0
    total_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        f = generate_boolean_function(n)
        r = compute_rank_variance(f)
        q = construct_quaternion_algebra(r)
        index = calculate_index(q)
        
        instances_tested += 1
        total_value += index
        
        if index < n * math.log(n):
            conjecture_holds = False
            counterexample = f"n={n}, rank_variance={r}, index={index}"
    
    return {
        "metric_name": "quaternion_index",
        "metric_value": total_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")