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
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def eta_invariant(f):
        n = len(f)
        count_1 = f.count(1)
        count_0 = n - count_1
        return Fraction(count_1, count_0) if count_0 != 0 else None
    
    instances_tested = 0
    correlation_sum = 0.0
    n_max = 5
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        eta_f = eta_invariant(f)
        
        if eta_f is not None:
            correlation_sum += (eta_f - Fraction(r_f, 2)) * (r_f - Fraction(r_f, 2))
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    correlation_coefficient = math.sqrt(correlation_sum / instances_tested)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "correlation_coefficient < 0.7"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)