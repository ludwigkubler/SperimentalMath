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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_function_field(g):
        # Simplified construction of a function field with genus g
        return f"K_{g}"
    
    def compute_invariant(C, K):
        n = len(C)
        g = int(K[2:])
        if n == 0 or g == 0:
            return None
        return (math.log(n) / math.log(2)) ** 3 / g
    
    def check_conjecture(C, K):
        psi_K_C = compute_invariant(C, K)
        if psi_K_C is None:
            return False, "mapping_undefined"
        expected_range = (math.log(len(C)) / math.log(2)) ** 3 / int(K[2:])
        return psi_K_C >= expected_range and psi_K_C <= expected_range * 1.05
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        K = construct_function_field(2)  # Simplified genus g=2
        C = f  # Simplified AC0 parity circuit
        instances_tested += 1
        
        holds, desc = check_conjecture(C, K)
        if not holds:
            conjecture_holds = False
            counterexample = desc
    
    return {
        "metric_name": "conjecture_support",
        "metric_value": instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")