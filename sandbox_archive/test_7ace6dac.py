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
    
    def compute_characteristic_function(f):
        n = int(math.log2(len(f)))
        char_func = [0] * (2**n)
        for i in range(len(f)):
            char_func[i] = f[i]
        return char_func
    
    def compute_norm(v):
        sum_squares = sum(x**2 for x in v)
        return math.sqrt(sum_squares)
    
    def compute_influence_complexity(f):
        n = int(math.log2(len(f)))
        influence = 0
        for i in range(n):
            for j in range(1 << i):
                f_tilde = [f[j] if (j & (1 << k)) == 0 else 1 - f[j] for k in range(n)]
                diff = sum(abs(f[k] - f_tilde[k]) for k in range(len(f)))
                influence += diff
        return influence / len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_influence_complexity = 0
    total_norm_squared = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            char_func = compute_characteristic_function(f)
            norm = compute_norm(char_func)
            influence_complexity = compute_influence_complexity(f)
            
            if norm == 1:
                total_influence_complexity += influence_complexity
                total_norm_squared += norm ** 2
                instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instance found"
        }
    
    correlation_coefficient = total_influence_complexity / instances_tested
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "Influence complexity less than the square of the norm"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")