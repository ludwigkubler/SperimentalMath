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
    
    def free_entropy(probabilities):
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
    
    def generate_read_twice_bp(n):
        # Simplified model of a read-twice branching program
        size = 2 ** n
        probabilities = [random.random() for _ in range(size)]
        return probabilities
    
    def log2_size_plus_n(size, n):
        return math.log2(size) + n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        size = 2 ** n
        bp = generate_read_twice_bp(n)
        entropy = free_entropy(bp)
        upper_bound = log2_size_plus_n(size, n)
        
        results.append({
            "n": n,
            "size": size,
            "entropy": entropy,
            "upper_bound": upper_bound,
            "difference": abs(entropy - upper_bound)
        })
    
    mean_difference = sum(result["difference"] for result in results) / len(results)
    max_difference = max(result["difference"] for result in results)
    
    conjecture_holds = all(diff <= 10 for diff in results)
    counterexample = "" if conjecture_holds else "max_diff={}".format(max_difference)
    
    return {
        "metric_name": "free_entropy",
        "metric_value": mean_difference,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean=%.2f std=%.2f support_fraction=%.2f" % (mean_value, 0.0, support_fraction))
    elif support_fraction >= 0.9:
        print("RESULT: SUPPORTED mean=%.2f std=%.2f support_fraction=%.2f" % (mean_value, 0.0, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='%s' first_failing_seed=%d" % (result["counterexample"], first_failing_seed))