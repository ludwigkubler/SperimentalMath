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
        max_linear_approximation_error = float('-inf')
        for j in range(n):
            linear_approximation = sum(f[i:i+n] for i in range(j, len(f), n))
            error = abs(linear_approximation - f[j])
            if error > max_linear_approximation_error:
                max_linear_approximation_error = error
        return 2**n - max_linear_approximation_error
    
    def compute_coxeter_group_action(f):
        n = int(math.log2(len(f)))
        transpositions = set()
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    transpositions.add((i, j))
        return len(transpositions)
    
    def inverse_ackermann(n):
        a = [0, 1]
        for i in range(2, n + 1):
            a.append(a[-1] + 1)
        return a[n]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        nonlinearity = compute_nonlinearity(f)
        transpositions = compute_coxeter_group_action(f)
        
        if transpositions > 2**n / nonlinearity**2:
            counterexample = "Number of distinct simple transpositions exceeds O(2^n/η(f)^2)"
            return {
                "metric_name": "Transpositions",
                "metric_value": transpositions,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        if transpositions > 2**n / inverse_ackermann(n):
            counterexample = "Nonlinearity too low for number of distinct simple transpositions"
            return {
                "metric_name": "Transpositions",
                "metric_value": transpositions,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append(transpositions)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = len([r for r in results if r <= 2**n_values[-1] / inverse_ackermann(n_values[-1])]) / len(results)
    
    return {
        "metric_name": "Transpositions",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Number of distinct simple transpositions exceeds O(2^n/η(f)^c)"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")