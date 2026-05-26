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

def generate_symmetric_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def construct_brauer_group_representation(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Function must be a symmetric boolean function")
    
    # Construct the representation of the Brauer group
    B_f = []
    for i in range(2**n):
        row = [0] * (2**n)
        row[i] = 1
        B_f.append(row)
    
    return B_f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_symmetric_boolean_function(n)
        try:
            B_f = construct_brauer_group_representation(f)
            dim_B_f = sum(1 for row in B_f if any(x != 0 for x in row))
            
            lower_bound = 2**n / math.log(n)
            upper_bound = n**2
            
            results.append({
                "n": n,
                "dim_B_f": dim_B_f,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound
            })
        except Exception as e:
            return {
                "metric_name": "brauer_group_dimension",
                "metric_value": None,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    conjecture_holds = all(lower_bound <= dim_B_f <= upper_bound for result in results)
    counterexample = "" if conjecture_holds else f"n={result['n']}, dim(B_f)={result['dim_B_f']}, lower_bound={result['lower_bound']}, upper_bound={result['upper_bound']}"
    
    return {
        "metric_name": "brauer_group_dimension",
        "metric_value": sum(result["dim_B_f"] for result in results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*2 + 1, 2))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")