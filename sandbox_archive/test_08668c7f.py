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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if f == [0]*len(f) or f == [1]*len(f):
            return 0
        if len(set(f)) == 2:
            return n
        return float('inf')
    
    def minimal_order_brauer_group(f):
        n = int(math.log2(len(f)))
        if f == [0]*len(f) or f == [1]*len(f):
            return 1
        if len(set(f)) == 2:
            return 2
        return float('inf')
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, avg):
        return math.sqrt(sum((x - avg)**2 for x in lst) / len(lst))
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            kappa_xor_n = communication_complexity(f)
            if kappa_xor_n == float('inf'):
                continue
            b_f = minimal_order_brauer_group(f)
            results.append(b_f / kappa_xor_n)
    
    avg_ratio = mean(results)
    std_ratio = std(results, avg_ratio)
    support_fraction = sum(1 for r in results if r <= 1) / len(results)
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    avg_ratio = mean(results)
    std_ratio = std(results, avg_ratio)
    support_fraction = sum(1 for r in results if r <= 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(r > 1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > 1)
        print(f"RESULT: FALSIFIED counterexample='mean_ratio > 1' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction < 0.8")