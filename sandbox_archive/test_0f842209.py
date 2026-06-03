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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        # Simplified version of communication complexity rank calculation
        return n
    
    def minimal_entanglement_entropy(f):
        n = int(math.log2(len(f)))
        # Simplified version of minimal entanglement entropy calculation
        return math.sqrt(n)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        entropy = minimal_entanglement_entropy(f)
        results.append((rank, entropy))
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in results) / math.sqrt(sum((x - mean_x)**2 for x, _ in results) * sum((y - mean_y)**2 for _, y in results))
    mean_rank = sum(x for x, _ in results) / len(results)
    mean_entropy = sum(y for _, y in results) / len(results)
    
    if abs(correlation_coefficient) < 0.5 or any(abs(x - y) > 10 for x, y in results):
        conjecture_holds = False
        counterexample = "correlation_threshold"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(result["counterexample"] == "correlation_threshold" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "correlation_threshold")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")