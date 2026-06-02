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
    
    def geometric_entropy(f):
        n = len(f)
        p = sum(1 for x in f if x == 1) / n
        q = 1 - p
        if p == 0 or q == 0:
            return 0
        return -p * math.log2(p) - q * math.log2(q)
    
    def circuit_monotone_width(f):
        # Simplified version of monotone circuit width calculation
        n = len(f)
        max_width = 0
        for i in range(1, 1 << n):
            if all(f[j] == f[i ^ j] for j in range(n) if (i & (1 << j)) != 0):
                max_width = max(max_width, bin(i).count('1'))
        return max_width
    
    def correlation_analysis(data):
        n = len(data)
        x_sum = sum(x for x, y in data)
        y_sum = sum(y for x, y in data)
        xy_sum = sum(x * y for x, y in data)
        x2_sum = sum(x**2 for x, y in data)
        y2_sum = sum(y**2 for x, y in data)
        
        if n == 0:
            return 0
        
        numerator = n * xy_sum - x_sum * y_sum
        denominator = math.sqrt((n * x2_sum - x_sum**2) * (n * y2_sum - y_sum**2))
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    def property_P(f):
        # Placeholder for property P check
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    data = []
    
    for n in n_values:
        for _ in range(30):
            f = generate_boolean_function(n)
            gamma_f = geometric_entropy(f)
            w_mon_f = circuit_monotone_width(f)
            data.append((gamma_f, w_mon_f))
    
    correlation_coefficient = correlation_analysis(data)
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(data),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.8")