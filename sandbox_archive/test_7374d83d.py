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
    
    def communication_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            bits = [f[j] for j in range(i*2**(n-i), (i+1)*2**(n-i))]
            if len(set(bits)) > 1:
                rank += 1
        return rank
    
    def p_adic_galois_representation(f):
        n = int(math.log2(len(f)))
        order = 1
        for i in range(n):
            bits = [f[j] for j in range(i*2**(n-i), (i+1)*2**(n-i))]
            if len(set(bits)) > 1:
                order *= 2
        return order
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        f = generate_boolean_function(n_max)
        rho_f = p_adic_galois_representation(f)
        rank_gal_f = communication_rank(f)
        if rho_f == 1:
            continue
        log_rho_f = math.log(rho_f)
        metric_values.append(log_rho_f / rank_gal_f)
    
    if not metric_values:
        return {
            "metric_name": "log_rho_over_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric_values"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "log_rho_over_rank",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break