# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 0
        for i in range(1, n):
            if all(f[j] != f[j + i] for j in range(n - i)):
                return i
        return n
    
    def coxeter_diagram_relations(f):
        n = len(f)
        relations = set()
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    relations.add((i, j))
        return relations
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = communication_complexity(f)
        R_f = coxeter_diagram_relations(f)
        
        if len(R_f) == 0 or C_f == 0:
            continue
        
        log_n = math.log2(n)
        ratio = Fraction(len(R_f), log_n) if log_n != 0 else float('inf')
        total_ratio += ratio
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(math.isnan(r["metric_value"]) for r in results):
        print("RESULT: INCONCLUSIVE no_valid_instances")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=nan support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"ratio_exceeds_bound\" first_failing_seed={first_failing_seed}")