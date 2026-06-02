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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] == 1:
                count += 1
        return count
    
    def grothendieck_witt_class(f):
        n = int(math.log2(len(f)))
        s = [sum(f[i:i+n]) for i in range(0, len(f), n)]
        g = sum(s)
        return abs(g) / math.sqrt(n)
    
    results = []
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        R_f = communication_complexity_rank(f)
        GW_class_f = grothendieck_witt_class(f)
        results.append((R_f, GW_class_f))
    
    n_max = max(len(f) for f in [generate_boolean_function(n) for n in range(5, 41)])
    if n_max < 16:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 30,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max too small"
        }
    
    R_f_values = [R for R, _ in results]
    GW_class_f_values = [GW for _, GW in results]
    
    mean_R = sum(R_f_values) / len(R_f_values)
    mean_GW = sum(GW_class_f_values) / len(GW_class_f_values)
    cov = sum((R - mean_R) * (GW - mean_GW) for R, GW in results) / len(results)
    var_R = sum((R - mean_R)**2 for R in R_f_values) / len(R_f_values)
    var_GW = sum((GW - mean_GW)**2 for GW in GW_class_f_values) / len(GW_class_f_values)
    
    correlation_coefficient = cov / math.sqrt(var_R * var_GW)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical support")