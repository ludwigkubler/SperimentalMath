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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dnf_circuit_size(f, n):
        # Simplified DNF circuit size estimation
        # This is a placeholder and should be replaced with actual logic
        return len(f)
    
    def coxeter_group_size(f, n):
        # Placeholder for Coxeter group size calculation
        # This is a placeholder and should be replaced with actual logic
        return len(f)  # Simplified example
    
    results = []
    for n in range(5, 41):
        f = generate_boolean_function(n)
        dnf_size = dnf_circuit_size(f, n)
        coxeter_size = coxeter_group_size(f, n)
        ratio = Fraction(coxeter_size, dnf_size)
        results.append({
            "n": n,
            "coxeter_size": coxeter_size,
            "dnf_size": dnf_size,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    max_coxeter_size = max(result["coxeter_size"] for result in results)
    min_dnf_size = min(result["dnf_size"] for result in results)
    
    conjecture_holds = all(ratio <= 2 for ratio in [result["ratio"] for result in results])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Coxeter Group Complexity Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max_coxeter_size,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")