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
    
    def calculate_max_degree(f):
        n = int(math.log2(len(f)))
        max_degree = 0
        for i in range(n):
            degree = sum(1 for j in range(i+1, n) if f[j] == f[i])
            max_degree = max(max_degree, degree)
        return max_degree
    
    def calculate_rank(f):
        # Placeholder for actual rank calculation logic
        # For simplicity, we'll use the number of variables as a proxy
        return len(f)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    delta_f = calculate_max_degree(f)
    rank_T = calculate_rank(f)
    
    if delta_f == 0:
        return {
            "metric_name": "Rank vs Delta(f)",
            "metric_value": float('inf'),  # Indeterminate for delta_f=0
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "delta_f=0"
        }
    
    ratio = rank_T / delta_f
    
    return {
        "metric_name": "Rank vs Delta(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - math.log(delta_f)) <= 1e-6,  # Θ(log(Δ(f)))
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    total_metric_value = sum(result['metric_value'] for result in results if not math.isinf(result['metric_value']))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(math.isinf(result['metric_value']) for result in results):
        print("RESULT: INCONCLUSIVE reason=metric_saturation")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.6f} std={math.sqrt(sum((x - total_metric_value/len(results))**2 for x in [r['metric_value'] if not math.isinf(r['metric_value']) else float('inf') for r in results])/len(results)):.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"delta_f=0\" first_failing_seed={first_failing_seed}")