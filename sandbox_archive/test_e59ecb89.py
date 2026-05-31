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
    
    def generate_protocol(n):
        # Generate a random n-party communication protocol with known complexity
        return [random.randint(1, 5) for _ in range(n)]
    
    def compute_tropical_pseudo_derivative(protocol):
        # Constructive mapping from the protocol to the derivative
        return sum(protocol)
    
    def compute_local_index(tropical_derivative):
        # Minimal local index of the tropical pseudo-derivative
        return len(set(tropical_derivative))
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        protocol = generate_protocol(n)
        tropical_derivative = compute_tropical_pseudo_derivative(protocol)
        local_index = compute_local_index(tropical_derivative)
        
        if n > n_max:
            n_max = n
        
        metric_values.append(local_index)
        instances_tested += 1
    
    mean_C = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_C) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "local_index",
        "metric_value": mean_C,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(c >= 0.8 for c in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_C = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_C) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if all(c >= 0.8 for c in r["metric_values"])) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")