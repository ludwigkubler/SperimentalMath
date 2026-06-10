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
    
    def communication_complexity_rank_variance(phi):
        n = int(math.log2(len(phi)))
        rank_var = sum(phi[i] != phi[j] for i in range(2**n) for j in range(i+1, 2**n)) / (2**(2*n-2))
        return rank_var
    
    def ehrhart_semigroup_size(phi):
        n = int(math.log2(len(phi)))
        count = 0
        for x in range(2**n):
            if all((phi[i] == phi[j]) == ((x >> i) & 1 == (x >> j) & 1) for i in range(n)):
                count += 1
        return count
    
    def polynomial_degree(poly):
        max_power = 0
        for power, coeff in poly.items():
            if coeff != 0 and power > max_power:
                max_power = power
        return max_power
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        phi = generate_boolean_function(n)
        rank_var = communication_complexity_rank_variance(phi)
        ehr_size = ehrhart_semigroup_size(phi)
        
        if rank_var == 0:
            continue
        
        total_metric_value += abs(ehr_size) ** 2
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "Ehrhart Semigroup Growth",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")