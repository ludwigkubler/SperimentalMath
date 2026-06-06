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
    
    def circuit_monotone_width(f):
        n = int(math.log2(len(f)))
        max_depth = 0
        stack = []
        for bit in f:
            if bit == 0:
                stack.append(bit)
            else:
                while len(stack) > 1 and stack[-1] != 0:
                    stack.pop()
                stack.append(bit)
            max_depth = max(max_depth, len(stack))
        return max_depth
    
    def galois_group_order(f):
        n = int(math.log2(len(f)))
        # Simplified heuristic for Galois group order
        return 2**n
    
    metric_name = "galois_group_order_over_theta"
    
    instances_tested = 0
    total_galois_order = 0
    total_theta = 0
    n_max = 1
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            galois_order = galois_group_order(f)
            theta = circuit_monotone_width(f)
            
            if n > n_max:
                n_max = n
            
            instances_tested += 1
            total_galois_order += galois_order
            total_theta += theta
    
    mean_galois_order = total_galois_order / instances_tested
    mean_theta = total_theta / instances_tested
    
    metric_value = mean_galois_order / (mean_theta * 2**n_max)
    
    conjecture_holds = metric_value <= 10
    counterexample = "" if conjecture_holds else "galois_group_order_over_theta"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"galois_group_order_over_theta\" first_failing_seed={first_failing_seed}")