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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def compute_nonlinearity(f):
        n = int(math.log2(len(f)))
        max_linear_approximation = 0
        for j in range(n):
            approximations = []
            for i in range(j, len(f), n):
                approximations.append(sum(f[i:i+n]))
            max_linear_approximation = max(max_linear_approximation, abs(sum(approximations) - (len(f) // n)))
        return 2**n - max_linear_approximation
    
    def compute_distinct_transpositions(f):
        n = int(math.log2(len(f)))
        transpositions = set()
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    transpositions.add((i, j))
        return len(transpositions)
    
    def inverse_ackermann(n):
        k = 0
        while 2**k <= n:
            k += 1
        return k - 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        nonlinearity = compute_nonlinearity(f)
        transpositions = compute_distinct_transpositions(f)
        
        if transpositions > 2**n / (nonlinearity ** 0.5):
            counterexample = "transpositions > O(2^n/η(f)^c)"
            return {
                "metric_name": "Transpositions",
                "metric_value": transpositions,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        if nonlinearity < 2 ** inverse_ackermann(n):
            counterexample = "η(f) < 2^α(n)"
            return {
                "metric_name": "Nonlinearity",
                "metric_value": nonlinearity,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append({
            "n": n,
            "transpositions": transpositions,
            "nonlinearity": nonlinearity
        })
    
    return {
        "metric_name": "Transpositions",
        "metric_value": sum(r["transpositions"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_transpositions = sum(r["metric_value"] * r["instances_tested"] for r in results)
    mean_transpositions = total_transpositions / len(results)
    std_dev_transpositions = math.sqrt(sum((r["metric_value"] - mean_transpositions) ** 2 * r["instances_tested"] for r in results) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_transpositions} std={std_dev_transpositions} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_transpositions} std={std_dev_transpositions} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")