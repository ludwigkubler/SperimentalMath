# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for x in product(range(2), repeat=n):
            y = tuple(x[i] ^ f[x[0]*2 + i] for i in range(n))
            if y not in [(0,)*n, (1,)*n]:
                rank += 1
        return rank
    
    def geometric_complexity(f):
        n = int(math.log2(len(f)))
        count = [f.count(i) for i in range(2**n)]
        total = sum(count)
        if total == 0:
            return 0
        return sum(count[i] * math.log2(count[i]/total) for i in range(2**n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    gc_sum = 0
    cr_var = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        gc = geometric_complexity(f)
        cr = communication_rank(f)
        
        if gc == 0 or cr == 0:
            continue
        
        gc_sum += gc
        cr_var += (cr - gc)**2
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "Geometric Complexity vs Communication Rank Variance",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_gc = gc_sum / instances_tested
    var_cr = cr_var / (instances_tested - 1)
    correlation_coefficient = mean_gc * math.sqrt(var_cr) / (mean_gc**2 + var_cr)**0.5
    
    return {
        "metric_name": "Geometric Complexity vs Communication Rank Variance",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")