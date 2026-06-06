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
    
    def affine_group_order(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        order = 1
        while True:
            found = False
            for i in range(1, 2**n):
                if all((f[i ^ j] == f[j]) for j in range(2**n)):
                    order += 1
                    found = True
                    break
            if not found:
                return order
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank_var = 0
        for i in range(1, 2**n):
            count = sum(1 for j in range(2**n) if f[i ^ j] == f[j])
            rank_var += (count / len(f)) ** 2
        return rank_var
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            f = generate_boolean_function(n)
            order = affine_group_order(f)
            if order is None:
                continue
            
            rank_var = communication_complexity_rank_variance(f)
            instances_tested += 1
            total_metric_value += abs(order - rank_var)
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in range(instances_tested)) / instances_tested) ** 0.5
    
    if any(abs(order - rank_var) > 3 * std_metric_value or abs(order - rank_var) > 10 for n in n_values for _ in range(5)):
        conjecture_holds = False
        counterexample = "order and rank variance not within 3 std deviations"
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_metric_value = (sum((x["metric_value"] - mean_metric_value) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order and rank variance not within 3 std deviations\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")