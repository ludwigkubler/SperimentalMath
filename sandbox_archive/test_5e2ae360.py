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
    return [random.choice([-1, 1]) for _ in range(2**n)]

def conjugacy_class_enumeration(f):
    n = int(math.log2(len(f)))
    classes = set()
    for i in range(n):
        class_set = {j for j in range(2**n) if f[j] == f[j ^ (1 << i)]}
        classes.update(class_set)
    return classes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 20, 40]:
        instances_tested = 0
        n_max = 0
        total_metric_value = 0
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(30):
            f = generate_boolean_function(n)
            classes = conjugacy_class_enumeration(f)
            chi_f = len(classes)
            instances_tested += 1
            n_max = max(n_max, n)
            
            if instances_tested == 1:
                expected_value = 2**n
                tolerance = 0.05 * expected_value
                if abs(chi_f - expected_value) / expected_value > tolerance:
                    conjecture_holds = False
                    counterexample = f"chi(f)={chi_f}, expected={expected_value}"
            
            total_metric_value += chi_f
        
        mean_value = Fraction(total_metric_value, instances_tested)
        
        results.append({
            "metric_name": "chi(f)",
            "metric_value": float(mean_value),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results)
    mean_value = Fraction(total_metric_value, sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - 2**r["n_max"]) / 2**r["n_max"] > 0.1 or not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - 2**result["n_max"]) / 2**result["n_max"] > 0.1 or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")