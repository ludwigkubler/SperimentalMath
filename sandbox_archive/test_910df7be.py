# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def communication_rank(f):
    n = len(f)
    rank = 0
    for i in range(n):
        if f[i] != f[0]:
            rank += 1
    return rank

def quaternionic_representation(k):
    return [[random.randint(0, 1) for _ in range(k)] for _ in range(k)]

def approximate_function(f, representation):
    n = len(f)
    approximations = [sum(representation[i]) % 2 for i in range(n)]
    error = sum(abs(approximations[i] - f[i]) for i in range(n))
    return error

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_rank(f)
        
        if r_f > n:
            continue
        
        min_order = float('inf')
        best_representation = None
        best_error = float('inf')
        
        for k in range(1, 2*n):
            representation = quaternionic_representation(k)
            error = approximate_function(f, representation)
            
            if error < best_error:
                best_representation = representation
                best_error = error
            
            if error <= 3 * (best_error / len(results)) - 3 * (best_error / len(results))**2:
                min_order = k
                break
        
        results.append({
            "n": n,
            "r_f": r_f,
            "min_order": min_order,
            "best_representation": best_representation,
            "best_error": best_error
        })
    
    mean_min_order = sum(result["min_order"] for result in results) / len(results)
    std_min_order = (sum((result["min_order"] - mean_min_order)**2 for result in results) / len(results))**0.5
    
    support_fraction = sum(1 for result in results if result["min_order"] <= 4 * result["r_f"]**2 and result["best_error"] <= 3 * (result["best_error"] / len(results)) - 3 * (result["best_error"] / len(results))**2) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "min_order > 4r(f)^2 or best_error > 3*std(best_error)"
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_min_order,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_min_order = sum(result["metric_value"] for result in results) / len(results)
    std_min_order = (sum((result["metric_value"] - mean_min_order)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_min_order} std={std_min_order} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")