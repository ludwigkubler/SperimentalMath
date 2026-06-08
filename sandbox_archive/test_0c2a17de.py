# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import Counter

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_rank(f):
        n = int(math.log2(len(f)))
        count = Counter()
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    count[(i, j)] += 1
        return len(count)
    
    def geometric_complexity(f):
        n = int(math.log2(len(f)))
        count = Counter()
        total = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    count[(i, j)] += 1
                    total += 1
        return sum(count[i] * math.log2((count[i]+1)/total) for i in count)
    
    n_values = [5, 10, 15, 20, 30, 40]
    gc_sum = 0
    cr_variance = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        gc = geometric_complexity(f)
        cr = communication_rank(f)
        
        if cr == 0:
            continue
        
        gc_sum += gc
        cr_variance += (cr - gc)**2
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "geometric_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    gc_mean = gc_sum / instances_tested
    cr_variance /= instances_tested
    
    return {
        "metric_name": "geometric_complexity",
        "metric_value": cr_variance,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": cr_variance >= gc_mean**2 * 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "not_enough_support"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")