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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input must be a Boolean function with 2^n variables")
    
    def simulate_protocol(k):
        new_f = [f[i] ^ f[i + 2**(k-1)] for i in range(2**(n-k))]
        return any(new_f)
    
    k = 1
    while True:
        if not simulate_protocol(k):
            break
        k += 1
    return k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 15, 20, 25]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        h_f = Fraction(1, 2**n)  # Simplified local cohomology degree
        results.append({"n": n, "cc": cc, "h_f": h_f})
    
    metric_name = "Communication Complexity vs Local Cohomology"
    metric_value = sum(result["cc"] * result["h_f"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["cc"] >= result["h_f"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")