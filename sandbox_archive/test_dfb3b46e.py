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
        if n == 0:
            return 0
        k = 1
        while True:
            new_f = [f[i] ^ f[i + 2**(k-1)] for i in range(2**(n-k))]
            if all(x == y for x, y in zip(f[:2**(n-k)], new_f)):
                return k
            k += 1
    
    def minimal_local_cohomology_degree(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        h = 1
        while True:
            new_f = [f[i] ^ f[i + 2**(h-1)] for i in range(2**(n-h))]
            if all(x == y for x, y in zip(f[:2**(n-h)], new_f)):
                return h
            h += 1
    
    n_values = [10, 15, 20, 25]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        h = minimal_local_cohomology_degree(f)
        results.append({"n": n, "cc": cc, "h": h})
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    cc_values = [r["cc"] for r in results]
    h_values = [r["h"] for r in results]
    
    mean_cc = sum(cc_values) / len(cc_values)
    mean_h = sum(h_values) / len(h_values)
    std_cc = math.sqrt(sum((x - mean_cc)**2 for x in cc_values) / len(cc_values))
    std_h = math.sqrt(sum((x - mean_h)**2 for x in h_values) / len(h_values))
    
    correlation_coefficient = sum((cc_values[i] - mean_cc) * (h_values[i] - mean_h) for i in range(len(results))) / (len(results) * std_cc * std_h)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 prime numbers
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")