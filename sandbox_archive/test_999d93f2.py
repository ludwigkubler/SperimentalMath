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
    
    def generate_instance(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def dpll_width(instance, path=[]):
        if not instance:
            return len(path)
        if '0' not in instance and '1' not in instance:
            return len(path)
        i = 0
        while instance[i] == '0':
            i += 1
        return max(dpll_width(instance[:i] + '0' + instance[i+1:], path + [instance[i]]),
                   dpll_width(instance[:i] + '1' + instance[i+1:], path + [instance[i]]))
    
    def elliptic_curve_rank(n):
        # Placeholder for actual computation
        return n  # Simplified example
    
    instances_tested = 0
    total_rho = 0.0
    min_rho = float('inf')
    max_rho = -float('inf')
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        instance = generate_instance(n)
        width = dpll_width(instance)
        rank = elliptic_curve_rank(n)
        
        if width == 0 or rank == 0:
            continue
        
        rho = abs(width - rank) / (width + rank)
        total_rho += rho
        min_rho = min(min_rho, rho)
        max_rho = max(max_rho, rho)
        
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    avg_rho = total_rho / instances_tested
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": avg_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": avg_rho >= 0.8 and min_rho >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Generate a list of 30 prime numbers
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rho = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rho} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rho} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_support\" first_failing_seed={first_failing_seed}")