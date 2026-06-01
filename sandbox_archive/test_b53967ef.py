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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def morse_function(f):
        n = int(math.log2(len(f)))
        morse_f = []
        for i in range(2**n):
            count_0 = f[i].count(0)
            count_1 = f[i].count(1)
            if count_0 > count_1:
                morse_f.append(0)
            elif count_0 < count_1:
                morse_f.append(1)
            else:
                morse_f.append(f[i][0])
        return morse_f
    
    def topological_entropy(h):
        h = [x for x in h if x != 0]
        total = sum(h)
        entropy = -sum(x / total * math.log2(x / total) for x in h)
        return entropy
    
    def communication_rank(morse_f):
        n = int(math.log2(len(morse_f)))
        rank = 0
        for i in range(n):
            count_0 = morse_f[i].count(0)
            count_1 = morse_f[i].count(1)
            if count_0 > count_1:
                rank += 1
            elif count_0 < count_1:
                rank -= 1
        return abs(rank)
    
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        morse_f = morse_function(f)
        h_morse_f = topological_entropy(morse_f)
        
        if len(h_morse_f) == 0:
            continue
        
        r_f = communication_rank(morse_f)
        correlation_sum += (h_morse_f - r_f) / (2**n / 3)
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_entropy"
        }
    
    correlation_avg = correlation_sum / instances_tested
    return {
        "metric_name": "correlation",
        "metric_value": correlation_avg,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_avg) <= 2**max(n_values) / 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) <= 2**max(n_values) / 3) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_metric")