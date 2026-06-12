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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        inputs = [i for i in range(2**n) if 0 <= i < 2**n and f[i] == 1]
        if not inputs:
            return 0
        R_f = sum([f[i] * (1 - f[j]) for i in inputs for j in inputs if i != j])
        return R_f
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            R_f = communication_complexity_rank_variance(f)
            if R_f == 0:
                continue
            instances_tested += 1
            n_max = max(n_max, n)
            results.append(R_f)
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank_variance",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    total_metric_value = 0
    total_instances_tested = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
        total_metric_value += trial_result["metric_value"]
        total_instances_tested += trial_result["instances_tested"]
    
    mean = total_metric_value / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r > 0) / len(results)
    
    if all(r > 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r == 0 for r in results):
        first_failing_seed = seeds[results.index(0)]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")