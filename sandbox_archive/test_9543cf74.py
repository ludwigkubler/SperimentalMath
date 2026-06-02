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
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] != f[0]:
                rank += 1
        return rank
    
    def galois_group_order(f):
        n = len(f)
        field = [i for i in range(2**n)]
        elements = set(field)
        automorphisms = []
        
        for perm in itertools.permutations(elements):
            if all((perm[i] ^ f[i]) == (perm[j] ^ f[j]) for i, j in combinations(range(n), 2)):
                automorphisms.append(perm)
        
        return len(automorphisms)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        order = galois_group_order(f)
        
        if order > 2**(n * math.log2(n)):
            return {
                "metric_name": "Galois Group Order",
                "metric_value": order,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Order {order} exceeds 2^(n * log2(n)) for n={n}"
            }
        
        results.append((rank, order))
    
    if not results:
        return {
            "metric_name": "Galois Group Order",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    ranks, orders = zip(*results)
    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (orders[i] - mean(orders)) for i in range(len(ranks))) / (len(ranks) * math.sqrt(variance(ranks)) * math.sqrt(variance(orders)))
    
    return {
        "metric_name": "Galois Group Order",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9 and p_value <= 0.05,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

def variance(lst):
    avg = mean(lst)
    return sum((x - avg) ** 2 for x in lst) / len(lst)

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_value = mean([result["metric_value"] for result in results])
        std_value = math.sqrt(variance([result["metric_value"] for result in results]))
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no data")