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
    
    def circuit_monotone_width(f):
        n = int(math.log2(len(f)))
        width = 0
        for i in range(2**n):
            if f[i] == 1:
                ones = [j for j in range(n) if (i & (1 << j)) != 0]
                width = max(width, len(ones))
        return width
    
    def grothendieck_group_order(f):
        n = int(math.log2(len(f)))
        G = {0: 1}
        for i in range(2**n):
            if f[i] == 1:
                for j in range(n):
                    if (i & (1 << j)) != 0:
                        G[i ^ (1 << j)] += 1
        return max(G.values())
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_order = 0
        total_width = 0
        
        while instances_tested < 30:
            f = generate_boolean_function(n)
            width = circuit_monotone_width(f)
            order = grothendieck_group_order(f)
            
            if width > 0 and order > 0:
                total_order += math.log(order, 2)
                total_width += width
                instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        mean_order = total_order / instances_tested
        mean_width = total_width / instances_tested
        correlation_coefficient = (instances_tested * total_order * total_width - 
                                   sum(math.log(order, 2) * width for order, width in zip(results, results))) / \
                                  math.sqrt((instances_tested * total_order**2 - sum(math.log(order, 2)**2 for order in results)) *
                                            (instances_tested * total_width**2 - sum(width**2 for width in results)))
        
        results.append(correlation_coefficient)
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_correlation = sum(results) / len(results)
    std_correlation = math.sqrt(sum((x - mean_correlation)**2 for x in results) / len(results))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_correlation,
        "instances_tested": 180,  # 30 instances per n * 6 n values
        "n_max": 40,
        "conjecture_holds": abs(mean_correlation) >= 0.95 and std_correlation <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if trial_result["conjecture_holds"]:
            results.append(trial_result["metric_value"])
    
    mean_metric = sum(results) / len(results)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in results) / len(results))
    support_fraction = len(results) / len(seeds)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")