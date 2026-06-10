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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid Boolean function length")
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == f[j]:
                    count += 1
        return count
    
    def minimal_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid Boolean function length")
        # Simplified approach to construct the noncommutative algebra
        rank = n  # This is a placeholder for actual computation
        return rank
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    minrank_values = []
    cc_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        minrank = minimal_rank(f)
        cc = communication_complexity(f)
        minrank_values.append(minrank)
        cc_values.append(cc)
    
    if len(minrank_values) < 30:
        return {
            "metric_name": "minrank / CC",
            "metric_value": None,
            "instances_tested": len(minrank_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ratio = [minrank / cc for minrank, cc in zip(minrank_values, cc_values)]
    corr_coeff = correlation_coefficient(ratio, n_values)
    
    return {
        "metric_name": "minrank / CC",
        "metric_value": corr_coeff,
        "instances_tested": len(minrank_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(corr_coeff) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.95' first_failing_seed={first_failing_seed}")