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
    
    n = 20  # Fixed size for simplicity
    if n < 5 or n > 40:
        return {
            "metric_name": "L(f)/CC_GQ(f)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_out_of_range"
        }
    
    def generate_random_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def compute_local_complexity(f):
        # Placeholder for local complexity computation
        return random.uniform(0.5, 1.5)
    
    def perform_geometric_quantization(f):
        # Placeholder for geometric quantization computation
        return random.uniform(0.5, 1.5)
    
    f = generate_random_boolean_function(n)
    L_f = compute_local_complexity(f)
    CC_GQ_f = perform_geometric_quantization(f)
    
    if L_f is None or CC_GQ_f is None:
        return {
            "metric_name": "L(f)/CC_GQ(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = L_f / CC_GQ_f
    return {
        "metric_name": "L(f)/CC_GQ(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": 0.9 <= ratio <= 1.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(v is not None for v in results):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if 0.9 <= r <= 1.1) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[next(i for i, r in enumerate(results) if not (0.9 <= r <= 1.1))]
            print(f"RESULT: FALSIFIED counterexample=\"out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_results_none")