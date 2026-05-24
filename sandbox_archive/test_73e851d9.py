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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def evaluate_function(f, x):
    if len(x) != len(f):
        raise ValueError("Input length must match function length")
    result = f[0]
    for i in range(1, len(f)):
        result ^= x[i-1] * f[i]
    return result

def p_adic_log(value, base):
    if value <= 0:
        return float('-inf')
    exponent = 0
    while value >= base:
        value /= base
        exponent += 1
    return exponent

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        instances_tested = 0
        total_log_value = 0
        
        while instances_tested < 30:
            x = [random.choice([0, 1]) for _ in range(2**n)]
            value = evaluate_function(f, x)
            if value != 0:
                log_value = p_adic_log(value, 2)  # Assuming base 2 for simplicity
                total_log_value += log_value
                instances_tested += 1
        
        avg_log_value = Fraction(total_log_value, instances_tested)
        results.append(avg_log_value * n)
    
    metric_name = "avg_p_adic_log_times_circuit_size"
    metric_value = sum(results) / len(results)
    conjecture_holds = all(result <= seed for result in results)
    counterexample = "" if conjecture_holds else "circuit_size_too_large"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(metric_value),
        "instances_tested": sum(len(results) for _ in n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= seed) / len(results)
    
    if all(r <= seed for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r > seed for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r > seed)
        print(f"RESULT: FALSIFIED counterexample=\"circuit_size_too_large\" first_failing_seed={first_failing_seed + 1}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")