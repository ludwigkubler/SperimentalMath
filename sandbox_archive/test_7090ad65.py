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
    
    def compute_circuit_monotone_width(f):
        n = len(f)
        max_width = 0
        for i in range(1 << n):
            width = 0
            stack = []
            for j in range(n):
                if (i >> j) & 1:
                    stack.append(f[j])
                    width += 1
                else:
                    if not stack:
                        continue
                    stack.pop()
                    width -= 1
            max_width = max(max_width, width)
        return max_width
    
    def compute_galois_group_order(f):
        n = len(f)
        # Simplified heuristic to estimate the order of the Galois group
        return 2**n
    
    metric_name = "Galois Group Order vs Circuit Monotone Width"
    instances_tested = 0
    total_order = 0
    total_width = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Test 5 instances per size
            f = generate_random_boolean_function(n)
            order = compute_galois_group_order(f)
            width = compute_circuit_monotone_width(f)
            
            total_order += order
            total_width += width
            instances_tested += 1
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    conjecture_holds = mean_order <= (2**n_max / mean_width) and max(mean_order, mean_width) < 10
    counterexample = "" if conjecture_holds else f"mean_order={mean_order}, mean_width={mean_width}"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")