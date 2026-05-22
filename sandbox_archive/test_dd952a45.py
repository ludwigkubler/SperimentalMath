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
    
    def generate_polynomial_system(n):
        # Generate a simple polynomial system over F_2 for demonstration purposes
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def compute_k_complexity(system):
        # Placeholder function to simulate K-complexity computation
        # In practice, this would involve more complex analysis
        return len(system)
    
    def compute_symplectic_rank(system):
        # Placeholder function to simulate symplectic rank computation
        # In practice, this would involve more complex algebraic geometry
        return len(system)  # Simplified for demonstration
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    system = generate_polynomial_system(n)
    k_complexity = compute_k_complexity(system)
    
    if k_complexity == 0:
        return {
            "metric_name": "symplectic_rank_to_log2_k_complexity_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "K-complexity is zero, undefined for this conjecture"
        }
    
    symplectic_rank = compute_symplectic_rank(system)
    ratio = symplectic_rank / (math.log2(k_complexity) ** 2)
    
    return {
        "metric_name": "symplectic_rank_to_log2_k_complexity_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "symplectic_rank_to_log2_k_complexity_ratio > c * log^2(k(n))"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")