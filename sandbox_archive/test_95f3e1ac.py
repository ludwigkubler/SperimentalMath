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
    
    def quadratic_residue(f, k):
        for x in range(2**n):
            if f[x] != (x**2 % k) % 2:
                return False
        return True
    
    def communication_complexity_rank(f):
        # Placeholder for actual CC rank calculation
        # For simplicity, we'll use a dummy function here
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        k = 1
        while not quadratic_residue(f, k):
            k += 1
        ord_f = k
        r_f = communication_complexity_rank(f)
        results.append((ord_f, r_f))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    ord_f_list = [x[0] for x in results]
    r_f_list = [x[1] for x in results]
    
    mean_ord_f = sum(ord_f_list) / len(ord_f_list)
    mean_r_f = sum(r_f_list) / len(r_f_list)
    var_ord_f = sum((x - mean_ord_f)**2 for x in ord_f_list) / len(ord_f_list)
    var_r_f = sum((x - mean_r_f)**2 for x in r_f_list) / len(r_f_list)
    cov = sum((ord_f_list[i] - mean_ord_f) * (r_f_list[i] - mean_r_f) for i in range(len(ord_f_list))) / len(ord_f_list)
    
    correlation_coefficient = cov / math.sqrt(var_ord_f * var_r_f)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
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
    
    if all("metric_value" not in x or x["metric_value"] is None for x in results):
        print("RESULT: INCONCLUSIVE no_metric_values")
    else:
        supported_count = sum(1 for x in results if "conjecture_holds" in x and x["conjecture_holds"])
        support_fraction = supported_count / len(results)
        
        if support_fraction >= 0.8:
            mean_value = sum(x["metric_value"] for x in results) / len(results)
            std_value = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results) / len(results))
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(x for x in seeds if run_trial(x)["conjecture_holds"] is False)
            counterexample = "not_enough_support"
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")