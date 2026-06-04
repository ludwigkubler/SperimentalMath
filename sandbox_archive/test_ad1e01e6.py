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
    
    def circuit_monotone_width(f):
        n = int(math.log2(len(f)))
        width = 0
        for i in range(n):
            count = sum(1 for x in f if x & (1 << i) == 0)
            width = max(width, count)
        return width
    
    def modular_symmetry_group(f):
        n = int(math.log2(len(f)))
        symmetries = set()
        for perm in itertools.permutations(range(n)):
            g = [f[perm[i]] for i in range(n)]
            if g not in symmetries:
                symmetries.add(tuple(g))
        return symmetries
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        w_f = circuit_monotone_width(f)
        M_f = modular_symmetry_group(f)
        min_w_g = min(circuit_monotone_width(g) for g in M_f)
        
        if len(M_f) == 0 or min_w_g == 0:
            continue
        
        results.append({
            "n": n,
            "w_f": w_f,
            "min_w_g": min_w_g
        })
    
    if not results:
        return {
            "metric_name": "min_w_g_over_w_f",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_w_g_over_w_f = sum(result["min_w_g"] / result["w_f"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    return {
        "metric_name": "min_w_g_over_w_f",
        "metric_value": min_w_g_over_w_f,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= min_w_g_over_w_f <= 2.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("metric_value" not in result or result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean_metric = sum(result["metric_value"] for result in results) / len(results)
        std_metric = math.sqrt(sum((result["metric_value"] - mean_metric)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if 0.5 <= result["metric_value"] <= 2.0) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.5 <= result["metric_value"] <= 2.0))
            print(f"RESULT: FALSIFIED counterexample=\"min_w_g_over_w_f out of range\" first_failing_seed={first_failing_seed}")