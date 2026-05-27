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
    
    def compute_nonlinearity(f):
        n = int(math.log2(len(f)))
        max_linear_approximation = sum(abs(sum(f[i:i+n] for i in range(j, len(f), n)) - (len(f) // n)) for j in range(n))
        return max(0, len(f) - max_linear_approximation)
    
    def compute_coxeter_group_action(f):
        n = int(math.log2(len(f)))
        transpositions = set()
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    transpositions.add((i, j))
        return len(transpositions)
    
    def factorial(x):
        if x == 0 or x == 1:
            return 1
        result = 1
        for i in range(2, x + 1):
            result *= i
        return result
    
    def inverse_ackermann(n):
        a = [0] * (n + 1)
        a[1] = 1
        for i in range(2, n + 1):
            j = 1
            while True:
                if a[j] >= i:
                    break
                j += 1
            a[i] = j
        return a[n]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        nonlinearity = compute_nonlinearity(f)
        transpositions = compute_coxeter_group_action(f)
        
        if transpositions > 2**n / (nonlinearity ** 2):
            counterexample = "Too many transpositions for given nonlinearity"
            return {
                "metric_name": "Transpositions",
                "metric_value": transpositions,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append({
            "n": n,
            "transpositions": transpositions,
            "nonlinearity": nonlinearity
        })
    
    mean_transpositions = sum(result["transpositions"] for result in results) / len(results)
    std_transpositions = math.sqrt(sum((result["transpositions"] - mean_transpositions) ** 2 for result in results) / len(results))
    support_fraction = all(result["transpositions"] <= 2**n / (result["nonlinearity"] ** 2) for result in results)
    
    return {
        "metric_name": "Transpositions",
        "metric_value": mean_transpositions,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*3 + 1))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_transpositions = sum(result["metric_value"] for result in results) / len(results)
    std_transpositions = math.sqrt(sum((result["metric_value"] - mean_transpositions) ** 2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_transpositions} std={std_transpositions} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = "Too many transpositions for given nonlinearity"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")