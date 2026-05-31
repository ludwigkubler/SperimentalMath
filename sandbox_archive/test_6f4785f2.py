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
    
    def noncrossing_partition_complex(f, n):
        # Placeholder function to compute the noncrossing partition complex
        # This is a dummy implementation and should be replaced with actual logic
        return f
    
    def automorphism_group_order(noncrossing_partition):
        # Placeholder function to compute the order of the automorphism group
        # This is a dummy implementation and should be replaced with actual logic
        return len(noncrossing_partition)
    
    def communication_complexity(f, n):
        # Placeholder function to compute the communication complexity
        # This is a dummy implementation and should be replaced with actual logic
        return n
    
    metric_name = "communication_complexity"
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 1
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        f = generate_random_boolean_function(n)
        noncrossing_partition = noncrossing_partition_complex(f, n)
        order_of_automorphism_group = automorphism_group_order(noncrossing_partition)
        comm_complexity = communication_complexity(f, n)
        
        if comm_complexity == 0:
            continue
        
        instances_tested += 1
        total_metric_value += order_of_automorphism_group / comm_complexity
    
    if instances_tested > 0:
        mean_C = total_metric_value / instances_tested
        std_dev = math.sqrt(sum((order_of_automorphism_group / comm_complexity - mean_C) ** 2 for f, n in zip(f_list, n_list)) / instances_tested)
        
        if mean_C < 1 or std_dev >= 0.5:
            conjecture_holds = False
            counterexample = "mean_C out of bounds"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_C,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_C = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_C) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_dev} support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_C out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")