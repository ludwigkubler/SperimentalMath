# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def generate_random_protocol(n):
    return [random.randint(1, 2*n) for _ in range(n)]

def compute_tropical_derivative(protocol):
    n = len(protocol)
    derivative = []
    for i in range(n):
        max_val = -float('inf')
        for j in range(n):
            if i != j:
                max_val = max(max_val, protocol[i] + protocol[j])
        derivative.append(max_val)
    return derivative

def compute_local_index(tropical_derivative):
    n = len(tropical_derivative)
    visited = [False] * n
    local_indices = []
    
    for i in range(n):
        if not visited[i]:
            max_val = -float('inf')
            count = 0
            for j in range(n):
                if not visited[j]:
                    max_val = max(max_val, tropical_derivative[j])
                    count += 1
            local_indices.append(count)
            for j in range(n):
                if not visited[j] and tropical_derivative[j] == max_val:
                    visited[j] = True
    
    return len(set(local_indices))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        protocol = generate_random_protocol(n)
        tropical_derivative = compute_tropical_derivative(protocol)
        local_index = compute_local_index(tropical_derivative)
        
        results.append({
            "n": n,
            "local_index": local_index
        })
    
    mean_local_index = sum(result["local_index"] for result in results) / len(results)
    std_local_index = math.sqrt(sum((result["local_index"] - mean_local_index) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "mean_local_index",
        "metric_value": mean_local_index,
        "instances_tested": len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": std_local_index <= 0.8 * math.sqrt(mean_local_index),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_local_index = sum(result["metric_value"] for result in results) / len(results)
    std_local_index = math.sqrt(sum((result["metric_value"] - mean_local_index) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_local_index} std={std_local_index} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")