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

def calculate_entanglement_complexity(f):
    n = int(math.log2(len(f)))
    complexity = 0
    for i in range(n):
        if f[2**i] != f[2**(i+1)]:
            complexity += 1
    return complexity

def calculate_lid(f):
    n = int(math.log2(len(f)))
    lid = 0
    for i in range(1, n):
        count = 0
        for j in range(2**n):
            if f[j] != f[j ^ (2**i)]:
                count += 1
        lid += Fraction(count, 2**n)
    return lid

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        entanglement_complexity = calculate_entanglement_complexity(f)
        lid = calculate_lid(f)
        
        if len(f) != 2**n or entanglement_complexity < 0 or lid < 0:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "invalid_function"
            }
        
        results.append((entanglement_complexity, lid))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    entanglement_complexities = [r[0] for r in results]
    lids = [r[1] for r in results]
    
    mean_entanglement = sum(entanglement_complexities) / len(entanglement_complexities)
    mean_lid = sum(lids) / len(lids)
    
    correlation_coefficient = 0
    for i in range(len(results)):
        correlation_coefficient += (entanglement_complexities[i] - mean_entanglement) * (lids[i] - mean_lid)
    correlation_coefficient /= len(results) * math.sqrt(sum((x - mean_entanglement)**2 for x in entanglement_complexities)) * math.sqrt(sum((y - mean_lid)**2 for y in lids))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_support\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support support_fraction={support_fraction}")