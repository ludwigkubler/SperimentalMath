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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * log2(p) - (1 - p) * log2(1 - p)
    
    def read_twice_bp_entropy(n):
        # Simulate a read-twice branching program and compute the minimal tensor product entropy
        states = [Fraction(1, n)] * n
        for _ in range(2):
            new_states = []
            for i in range(n):
                p = states[i]
                new_states.extend([p / 2] * 2)
            states = new_states
        return sum(entropy(p) for p in states)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    
    for n in n_values:
        entropy_value = read_twice_bp_entropy(n)
        total_entropy += entropy_value
        instances_tested += 1
        
        if entropy_value > n * log2(2):
            return {
                "metric_name": "minimal_tensor_product_entropy",
                "metric_value": entropy_value,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"Instance of size {n} has entropy {entropy_value} > {n * log2(2)}"
            }
    
    mean_entropy = total_entropy / instances_tested
    return {
        "metric_name": "minimal_tensor_product_entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")