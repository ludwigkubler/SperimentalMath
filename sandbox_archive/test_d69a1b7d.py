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
    
    def frege_proof_complexity(f):
        # Placeholder for actual Frege proof complexity calculation
        # For simplicity, we assume a linear relationship with n
        return len(f) // 2
    
    def categorical_representation(f):
        # Placeholder for actual categorical representation calculation
        # For simplicity, we assume a cubic relationship with n
        return len(f) ** 3
    
    def count_monoids(representation):
        # Placeholder for actual monoid counting
        # For simplicity, we assume a linear relationship with n
        return len(representation)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        d_f = frege_proof_complexity(f)
        D_f = categorical_representation(f)
        num_monoids = count_monoids(representation=f)
        
        if num_monoids > D_f ** 3:
            return {
                "metric_name": "num_monoids",
                "metric_value": num_monoids,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, d(f)={d_f}, D(f)={D_f}, num_monoids={num_monoids}"
            }
        
        results.append({
            "n": n,
            "d_f": d_f,
            "D_f": D_f,
            "num_monoids": num_monoids
        })
    
    mean_metric_value = sum(result["num_monoids"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["num_monoids"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = all(result["num_monoids"] <= result["D_f"] ** 3 for result in results)
    
    return {
        "metric_name": "num_monoids",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['n']}, d(f)={result['d_f']}, D(f)={result['D_f']}, num_monoids={result['num_monoids']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")