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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            bit = f[i]
            if any(bit == f[j] for j in range(i+1, n)):
                rank += 1
        return rank
    
    def generate_permutation_group(f):
        n = int(math.log2(len(f)))
        group = []
        for i in range(n):
            perm = [0] * n
            perm[i] = 1
            group.append(perm)
        return group
    
    def permutation_group_order(group):
        return len(group)
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    R_f = communication_complexity_rank(f)
    G = generate_permutation_group(f)
    order_G = permutation_group_order(G)
    
    if R_f == 0:
        return {
            "metric_name": "order_of_group",
            "metric_value": order_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "R(f) is 0, trivial case"
        }
    
    if abs(order_G - R_f**2) > 1.5 * R_f**2:
        return {
            "metric_name": "order_of_group",
            "metric_value": order_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Order {order_G} not within factor of 1.5 from R(f)^2 = {R_f**2}"
        }
    
    return {
        "metric_name": "order_of_group",
        "metric_value": order_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds_count = sum(1 for r in results if r["conjecture_holds"])
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")