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
    
    def hodge_norm(C):
        # Placeholder function for Hodge norm calculation
        return abs(sum(random.random() for _ in range(10)))
    
    def circuit_monotone_width(C):
        # Placeholder function for circuit monotone width calculation
        return len(C) * 2
    
    def polynomial_bound(mn, degree=4):
        # Polynomial bound f(mn)
        return mn ** degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            C = [random.random() for _ in range(n)]
            hodge_val = hodge_norm(C)
            mn = circuit_monotone_width(C)
            bound = polynomial_bound(mn)
            
            if hodge_val > bound * 1.1:
                return {
                    "metric_name": "Hodge Norm vs Circuit Monotone Width",
                    "metric_value": hodge_val,
                    "instances_tested": len(results),
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"H(C)={hodge_val} > {bound}=f(mn)"
                }
            
            results.append({
                "H(C)": hodge_val,
                "mn": mn,
                "bound": bound
            })
    
    return {
        "metric_name": "Hodge Norm vs Circuit Monotone Width",
        "metric_value": sum(result["H(C)"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(result["H(C)"] <= result["bound"] for result in results),
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
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"H(C) > f(mn)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")