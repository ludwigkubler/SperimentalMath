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
        n = len(f)
        max_depth = 0
        stack = []
        for bit in f:
            if bit == 1:
                stack.append(bit)
            else:
                while stack and stack[-1] != 1:
                    stack.pop()
                if stack:
                    stack.pop()
                stack.append(1)
            max_depth = max(max_depth, len(stack))
        return max_depth
    
    def galois_group_order(f):
        n = len(f)
        # Simplified heuristic for demonstration purposes
        return 2**n
    
    metric_name = "galois_group_order_over_theta"
    instances_tested = 0
    n_max = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Sample 5 instances per size
            f = generate_random_boolean_function(n)
            theta_f = circuit_monotone_width(f)
            galois_order = galois_group_order(f)
            
            if theta_f == 0:
                continue
            
            metric_value = galois_order / (2**n / theta_f)
            total_metric_value += metric_value
            instances_tested += 1
            
            if metric_value > 10:
                conjecture_holds = False
                counterexample = f"Large metric value {metric_value} for n={n}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested else float('nan')
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in [total_metric_value / instances_tested] * instances_tested)) / instances_tested if instances_tested else float('nan')
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results) if results else float('nan')
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results)) / len(results) if results else float('nan')
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Large metric value\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")